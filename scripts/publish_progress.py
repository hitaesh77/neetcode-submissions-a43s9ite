"""Publish a validated snapshot with a fast-forward-only, single-file Git tree."""
import json
from pathlib import Path
import subprocess
import sys

from progress import require, validate


def command(*args, input=None):
    return subprocess.check_output(["git", *args], input=input, encoding="utf-8").strip()


def publish(path):
    snapshot = json.loads(Path(path).read_text(encoding="utf-8"))
    validate(snapshot)
    require(snapshot["dataQuality"]["acceptance"] == "configured-accepted-only", "Accepted-only configuration required")
    source = snapshot["sourceCommit"]
    command("fetch", "origin", "main")
    latest = command("rev-parse", "FETCH_HEAD")
    if latest != source:
        print("Main advanced; skipping stale snapshot. Run manually if a newer run is not queued.")
        return
    remote = command("ls-remote", "--heads", "origin", "refs/heads/dashboard-data")
    parent_args = []
    if remote:
        command("fetch", "origin", "dashboard-data")
        parent = command("rev-parse", "FETCH_HEAD")
        old = json.loads(command("show", f"{parent}:progress.json"))
        validate(old)
        subprocess.run(["git", "merge-base", "--is-ancestor", old["sourceCommit"], source], check=True)
        require(not old["summary"]["submissions"] or snapshot["summary"]["submissions"] > 0, "Refusing to replace populated snapshot with empty data")
        parent_args = ["-p", parent]
    blob = command("hash-object", "-w", "--", path)
    tree = command("mktree", "-z", input=f"100644 blob {blob}\tprogress.json\0")
    commit = command("-c", "user.name=github-actions[bot]", "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                     "commit-tree", tree, *parent_args, input=f"Update progress for {source}\n")
    # No force: concurrent external writes or branch creation cause a safe failure.
    command("push", "origin", f"{commit}:refs/heads/dashboard-data")


if __name__ == "__main__":
    publish(sys.argv[1] if len(sys.argv) > 1 else "progress.json")
