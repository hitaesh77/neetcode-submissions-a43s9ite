"""Rebuild schema v1 from Git; no solution code is executed or exported."""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import quote, urlparse
from zoneinfo import ZoneInfo

ROOT = "Data Structures & Algorithms/"
PATH = re.compile(re.escape(ROOT) + r"([a-z0-9]+(?:-[a-z0-9]+)*)/submission-(0|[1-9][0-9]*)\.(py|js|ts|java|cpp|cs|go|rs|kt|swift|sql)$")
REPO = "hitaesh77/neetcode-submissions-a43s9ite"
TZ = ZoneInfo("America/New_York")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], encoding="utf-8")


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamp must include an offset")
    return parsed.astimezone(timezone.utc)


def utc(value):
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def check_config(config, metadata):
    require(set(config) == {"challengeStartedAt", "acceptedOnlyConfirmed", "commitPolicies"}, "Unknown/missing config field")
    start = config["challengeStartedAt"]
    if start is not None:
        require(date.fromisoformat(start).isoformat() == start, "Use YYYY-MM-DD challenge start")
    require(type(config["acceptedOnlyConfirmed"]) is bool, "acceptedOnlyConfirmed must be boolean")
    for sha, policy in config["commitPolicies"].items():
        require(re.fullmatch(r"[0-9a-f]{40}", sha), "Policies require full commit SHA")
        require(policy.get("mode") in {"exclude", "undated", "dated"} and policy.get("reason"), "Policy requires mode and reason")
        require(set(policy) <= {"mode", "reason", "timestamps"}, "Unknown policy field")
        if "timestamps" in policy:
            require(policy["mode"] == "dated", "Timestamp overrides require dated mode")
            for timestamp in policy["timestamps"].values():
                instant(timestamp)
    for problem, entry in metadata.items():
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", problem), "Invalid metadata problem ID")
        require(set(entry) <= {"title", "difficulty", "topics", "links"}, "Unknown metadata field")
        require(entry.get("difficulty") in {None, "Easy", "Medium", "Hard"}, "Invalid difficulty")
        require(entry.get("title") is None or isinstance(entry["title"], str) and entry["title"].strip(), "Invalid title")
        topics = entry.get("topics")
        require(topics is None or isinstance(topics, list) and all(isinstance(t, str) and t for t in topics), "Invalid topics")
        for name, link in entry.get("links", {}).items():
            host = {"neetcode": "neetcode.io", "leetcode": "leetcode.com"}.get(name)
            parsed = urlparse(link)
            require(host and parsed.scheme == "https" and parsed.netloc == host and not parsed.query and not parsed.fragment, "Use verified public problem links only")


def reconstruct(repo, revision, config, diagnostics):
    require(git(repo, "rev-parse", "--is-shallow-repository").strip() == "false", "Full Git history is required")
    source = git(repo, "rev-parse", "--verify", revision + "^{commit}").strip()
    commits = git(repo, "rev-list", "--reverse", "--topo-order", source).splitlines()
    policies = config["commitPolicies"]
    require(set(policies) <= set(commits), "Configured policy commit not in source history")
    records, seen = [], set()
    for sha in commits:
        parents = git(repo, "show", "-s", "--format=%P", sha).strip().split()
        # Merges are traversed through their parents, never counted twice.
        if len(parents) > 1:
            # A merge-only solution would otherwise disappear from reconstruction.
            tree = set(git(repo, "ls-tree", "-r", "--name-only", sha).splitlines())
            inherited = set()
            for parent in parents:
                inherited.update(git(repo, "ls-tree", "-r", "--name-only", parent).splitlines())
            require(not any(p.startswith(ROOT) for p in tree - inherited), f"Merge-only submission requires review: {sha}")
            diagnostics.append(f"Ignored merge {sha}")
            continue
        subject, stamp = git(repo, "show", "-s", "--format=%s%n%cI", sha).splitlines()
        tokens = git(repo, "diff-tree", "--root", "--no-commit-id", "-r", "-M", "--name-status", "-z", sha).split("\0")
        additions = []
        i = 0
        while i < len(tokens) and tokens[i]:
            status, path = tokens[i:i + 2]
            i += 2
            if status.startswith(("R", "C")):
                destination = tokens[i]
                i += 1
                match = PATH.fullmatch(destination)
                if match:
                    seen.add(f"{match[1]}/submission-{match[2]}")
                diagnostics.append(f"Ignored rename/copy {sha}: {path}")
                continue
            if not path.startswith(ROOT):
                if "submission-" in path:
                    diagnostics.append(f"Unsupported course: {path}")
                continue
            match = PATH.fullmatch(path)
            require(match is not None, f"Unsupported submission path {sha}: {path}")
            if status == "A":
                additions.append((path, match[1], match[2]))
            else:
                diagnostics.append(f"Ignored {status} {sha}: {path}")
        if not additions:
            continue
        policy = policies.get(sha)
        if policy is None:
            # Multiple records require explicit review, or matching Add lines in body.
            lines = git(repo, "show", "-s", "--format=%B", sha).splitlines()
            expected = {f"Add: {p} - submission-{n}" for _, p, n in additions}
            require(expected <= set(lines), f"Ambiguous additions (including bulk imports): configure commitPolicies for {sha}")
        mode = policy["mode"] if policy else "dated"
        overrides = policy.get("timestamps", {}) if policy else {}
        require(set(overrides) <= {p for p, _, _ in additions}, f"Unused timestamp override in {sha}")
        if subject.lower().startswith("bulk") and mode == "dated":
            require(set(overrides) == {p for p, _, _ in additions}, f"Bulk import requires original timestamps for every file: {sha}")
        if policy:
            diagnostics.append(f"Policy {mode} {sha}: {policy['reason']} ({len(additions)} files)")
        for path, problem, number in additions:
            identity = f"{problem}/submission-{number}"
            if identity in seen:
                diagnostics.append(f"Duplicate identity ignored: {identity} ({sha})")
                continue
            seen.add(identity)
            if mode == "exclude":
                continue
            recorded = utc(instant(overrides.get(path, stamp)))
            records.append({"id": identity, "problemId": problem, "recordedAt": recorded,
                            "localDate": instant(recorded).astimezone(TZ).date().isoformat() if mode == "dated" else None,
                            "timestampBasis": "override" if path in overrides else "git-committer",
                            "sourceUrl": f"https://github.com/{REPO}/blob/{sha}/{quote(path, safe='/')}"})
    return source, records


def summarize(records, start, metadata):
    problems = {r["problemId"] for r in records}
    difficulties = Counter(metadata.get(p, {}).get("difficulty") or "Unknown" for p in problems)
    daily = {}
    for day in sorted({r["localDate"] for r in records if r["localDate"]}):
        group = [r for r in records if r["localDate"] == day]
        daily[day] = {"submissions": len(group), "distinctProblems": len({r["problemId"] for r in group})}
    challenge = None
    if start is not None:
        days = [day for day in daily if day >= start]
        longest = ending = 0
        previous = None
        for day in days:
            current = date.fromisoformat(day)
            ending = ending + 1 if previous and current - previous == timedelta(days=1) else 1
            longest = max(longest, ending)
            previous = current
        challenge = {"completedDays": len(days), "longestStreak": longest,
                     "lastCompletedDate": days[-1] if days else None, "streakEndingOnLastCompletedDate": ending}
    return {"submissions": len(records), "distinctProblems": len(problems),
            "datedSubmissions": sum(v["submissions"] for v in daily.values()),
            "undatedSubmissions": sum(r["localDate"] is None for r in records),
            "activeDays": len(daily), "difficulty": {k: difficulties[k] for k in ("Easy", "Medium", "Hard", "Unknown")}}, daily, challenge


def validate(snapshot):
    """Executable schema v1, including cross-field invariants; raises on invalid data."""
    require(set(snapshot) == {"schemaVersion", "generatedAt", "sourceCommit", "source", "timezone", "challengeStartedAt", "dataQuality", "summary", "dailyActivity", "challenge", "recentSubmissions"}, "Invalid schema fields")
    require(snapshot["schemaVersion"] == 1, "Unsupported schemaVersion")
    require(snapshot["generatedAt"].endswith("Z"), "generatedAt must be UTC")
    instant(snapshot["generatedAt"])
    require(re.fullmatch(r"[0-9a-f]{40}", snapshot["sourceCommit"]), "Invalid sourceCommit")
    require(snapshot["source"] == {"repository": REPO, "branch": "main"} and snapshot["timezone"] == "America/New_York", "Invalid source/timezone")
    summary = snapshot["summary"]
    require(set(summary) == {"submissions", "distinctProblems", "datedSubmissions", "undatedSubmissions", "activeDays", "difficulty"}, "Invalid summary")
    require(all(type(v) is int and v >= 0 for k, v in summary.items() if k != "difficulty"), "Invalid totals")
    require(set(summary["difficulty"]) == {"Easy", "Medium", "Hard", "Unknown"} and all(type(v) is int and v >= 0 for v in summary["difficulty"].values()), "Invalid difficulty totals")
    require(sum(summary["difficulty"].values()) == summary["distinctProblems"] <= summary["submissions"], "Inconsistent problems")
    days = snapshot["dailyActivity"]
    require(list(days) == sorted(days), "Unsorted calendar")
    for day, counts in days.items():
        require(date.fromisoformat(day).isoformat() == day, "Invalid date")
        require(set(counts) == {"submissions", "distinctProblems"} and all(type(v) is int for v in counts.values()), "Invalid daily record")
        require(0 < counts["distinctProblems"] <= counts["submissions"], "Invalid daily counts")
    require(summary["activeDays"] == len(days) and summary["datedSubmissions"] == sum(d["submissions"] for d in days.values()), "Inconsistent calendar")
    require(summary["submissions"] == summary["datedSubmissions"] + summary["undatedSubmissions"], "Inconsistent submission total")
    start = snapshot["challengeStartedAt"]
    if start is not None:
        require(date.fromisoformat(start).isoformat() == start, "Invalid challenge start")
    fake = [{"problemId": "x", "localDate": day} for day in days]
    require(snapshot["challenge"] == summarize(fake, start, {})[2], "Invalid challenge metrics")
    quality = snapshot["dataQuality"]
    require(set(quality) == {"acceptance", "timestampBasis", "limitations", "appliedPolicies"}, "Invalid data quality")
    require(quality["acceptance"] in {"configured-accepted-only", "unconfirmed"} and quality["timestampBasis"] == "git-committer-with-explicit-overrides", "Invalid provenance")
    require(isinstance(quality["limitations"], list) and all(isinstance(v, str) for v in quality["limitations"]), "Invalid limitations")
    require(isinstance(quality["appliedPolicies"], dict), "Invalid policy provenance")
    check_config({"challengeStartedAt": start, "acceptedOnlyConfirmed": quality["acceptance"] == "configured-accepted-only", "commitPolicies": quality["appliedPolicies"]}, {})
    recent = snapshot["recentSubmissions"]
    require(len(recent) == min(10, summary["datedSubmissions"]), "Invalid recent count")
    require(recent == sorted(recent, key=lambda r: (r["recordedAt"], r["id"]), reverse=True), "Unsorted recent records")
    require(len({r["id"] for r in recent}) == len(recent), "Duplicate recent ID")
    for r in recent:
        require(set(r) == {"id", "problemId", "title", "recordedAt", "localDate", "timestampBasis", "difficulty", "topics", "links", "sourceUrl"}, "Invalid recent fields")
        require(re.fullmatch(re.escape(r["problemId"]) + r"/submission-(0|[1-9][0-9]*)", r["id"]), "Invalid record identity")
        require(r["localDate"] == instant(r["recordedAt"]).astimezone(TZ).date().isoformat() and r["localDate"] in days, "Invalid local date")
        require(r["timestampBasis"] in {"git-committer", "override"}, "Invalid timestamp basis")
        require(r["sourceUrl"].startswith(f"https://github.com/{REPO}/blob/"), "Invalid source link")
        check_config({"challengeStartedAt": start, "acceptedOnlyConfirmed": False, "commitPolicies": {}}, {r["problemId"]: {k: r[k] for k in ("title", "difficulty", "topics", "links")}})


def build(repo, revision, config, metadata, generated_at=None):
    check_config(config, metadata)
    diagnostics = []
    source, records = reconstruct(repo, revision, config, diagnostics)
    summary, daily, challenge = summarize(records, config["challengeStartedAt"], metadata)
    recent = []
    for r in sorted((r for r in records if r["localDate"]), key=lambda r: (r["recordedAt"], r["id"]), reverse=True)[:10]:
        m = metadata.get(r["problemId"], {})
        recent.append({**r, "title": m.get("title") or r["problemId"].replace("-", " ").title(),
                       "difficulty": m.get("difficulty"), "topics": m.get("topics"), "links": m.get("links", {})})
    result = {"schemaVersion": 1, "generatedAt": generated_at or utc(datetime.now(timezone.utc)),
              "sourceCommit": source, "source": {"repository": REPO, "branch": "main"},
              "timezone": "America/New_York", "challengeStartedAt": config["challengeStartedAt"],
              "dataQuality": {"acceptance": "configured-accepted-only" if config["acceptedOnlyConfirmed"] else "unconfirmed",
                              "timestampBasis": "git-committer-with-explicit-overrides",
                              "limitations": ["Acceptance is not stored in Git; accepted-only sync is a prerequisite.",
                                              "Git timestamps record sync, not original completion; unmarked imports cannot be detected reliably.",
                                              "Undated imports count toward lifetime totals, never calendar activity or recent practice.",
                                              "Missing metadata stays unknown; fallback titles are derived from repository slugs."],
                              "appliedPolicies": config["commitPolicies"]},
              "summary": summary, "dailyActivity": daily, "challenge": challenge, "recentSubmissions": recent}
    validate(result)
    return result, diagnostics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--config", default="dashboard/config.json")
    parser.add_argument("--metadata", default="dashboard/problems.json")
    parser.add_argument("--output", default="progress.json")
    parser.add_argument("--require-accepted-only", action="store_true")
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    require(not args.require_accepted_only or config["acceptedOnlyConfirmed"], "Confirm accepted-only NeetCode sync in dashboard/config.json before publishing")
    result, diagnostics = build(args.repo, args.revision, config, json.loads(Path(args.metadata).read_text(encoding="utf-8")))
    for message in diagnostics:
        print(message, file=sys.stderr)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(result, separators=(",", ":"), ensure_ascii=True) + "\n", encoding="utf-8")
    temporary.replace(target)
    print(json.dumps(result["summary"]), file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, subprocess.CalledProcessError, KeyError, TypeError) as error:
        sys.exit(f"Snapshot failed: {error}")
