# Portfolio progress snapshot

This repository produces a compact, versioned snapshot for a browser to fetch at:

`https://raw.githubusercontent.com/hitaesh77/neetcode-submissions-a43s9ite/dashboard-data/progress.json`

No database, server, schedule, portfolio hook, or frontend code is involved. The
workflow publishes only `progress.json` to `dashboard-data`. The example in this
directory is a local build, not evidence that the public branch has been published.

The checked-in example contains **107 submission identities across 56 problems**:
37 dated submissions on 10 New York dates and 70 undated imported submissions.
No identities were excluded entirely. All 56 problems have difficulty metadata
from the NeetCode All catalog. With the configured September start, challenge completed days
and both streak lengths are zero, and the last completed challenge date is null.

## Inspection and configuration

Inspection of all 39 commits through `99f7028ee327320f5fb31d0485ba68b0ba5b44d4`
found one initialization commit, one `Bulk sync: 70 submissions` commit, and 37
`Add: <problem> - submission-<n>` commits. All submission changes were additions;
there were no historical edits, renames, deletions, or merges. The bulk commit
demonstrates that a commit can contain multiple submission files. Source files
contain solutions, without acceptance status or original submission timestamps.
The existing README describes both accepted/all syncing and manual/bulk sync.

The owner confirmed accepted-only syncing and a **2026-09-16** challenge start in
America/New_York. These values are recorded in `config.json`. Keep NeetCode GitHub
Sync's status filter set to **accepted only**, with automatic commits enabled.
The code cannot independently verify acceptance, including acceptance of old
imported files. If historical sync settings differed, review and exclude affected
commits before publication. Setting `acceptedOnlyConfirmed` to false blocks the
publishing command but allows diagnostic local builds.

`challengeStartedAt` is an inclusive New York date, not an instant. Set it to a
chosen `YYYY-MM-DD`, or explicitly null to leave challenge metrics unavailable.
It never defaults to the first observed commit. The checked-out history ends in
April 2026, so the configured September challenge has zero completed days.

## Local use and workflow setup

Use Git and Python 3.11+ with the IANA timezone database. Ubuntu Actions runners
provide both; there are no runtime packages to install there. On Windows, if
`ZoneInfoNotFoundError` occurs, install timezone data with `python -m pip install tzdata`.

```sh
python -m unittest discover -s tests -v
python scripts/progress.py --require-accepted-only --output dashboard/progress.example.json
```

The default revision is the current `HEAD`; run on main for a deployable snapshot.
`--repo`, `--revision`, `--config`, `--metadata`, and `--output` support isolated
local checks. History must not be shallow. Output is validated before an atomic
file replacement. Errors leave any previous output intact.

Commit these implementation files to main to install the workflow. In GitHub,
open **Actions → Publish NeetCode progress → Run workflow**, selecting main, for
initialization or recovery. Relevant submission, script, test, config, metadata,
and workflow pushes to main also trigger it. There is no scheduled job.

The workflow requests only `contents: write` and uses the built-in token.
Repository/organization rules must permit Actions and permit that token to create
and update `dashboard-data`. No personal token is required by this implementation.
Keep branch protection on main; allow normal bot commits to the data branch.
The data branch is created on the first successful publish. Never put hand-edited
files there: each publication's tree intentionally contains only `progress.json`.

Runs share one concurrency group and do not cancel an in-flight publish. Each run
checks out the latest main with full history, rather than its potentially stale
event revision. Immediately before publishing it fetches main again and skips if
the source changed. Existing snapshots must validate and their source revision
must be an ancestor of the new source. Publishing creates a child of the current
data-branch tip and uses a normal push; a competing writer causes rejection, not
an overwrite. Tests/generation failures preserve the last published snapshot.
An existing nonempty snapshot cannot be replaced with an empty one.

**Test an actual NeetCode submission push after installing.** GitHub documents
that most events created with another workflow's built-in `GITHUB_TOKEN` do not
start another workflow ([GitHub token documentation](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)).
No existing workflow was found here, and the sync credential mechanism could not
be established from Git history. If the real push does not trigger this workflow,
inspect its integration/authentication first; use manual dispatch to recover.
Do not introduce a personal access token merely on speculation.

## Counting and history policies

Only `Data Structures & Algorithms/<slug>/submission-<nonnegative-integer>.<ext>`
is supported. Extensions match the repository README: py, js, ts, java, cpp, cs,
go, rs, kt, swift, sql. Other course folders are ignored with diagnostics. An
unrecognized file under the supported root fails closed, so new sync formats
require deliberate review.

An addition must have a matching `Add: <slug> - submission-<n>` line in its commit
message, or an explicit reviewed commit policy. Multiple matching lines support
multiple files in one commit. An unexplained addition or bulk import stops the
build. Commits are visited in reverse topological order across all reachable
parents. Merge commits themselves do not produce events; parent submissions are
counted once. A merge introducing a new supported path absent from all parents
fails for review. Conflict-resolution edits are not fresh submissions.

Stable identity is `<problem-slug>/submission-<number>` within this one course,
independent of extension and commit hash. The first observed identity wins;
re-added backups, another language for the same numbered slot, and duplicates
do not count again. Ordinary modifications, deletions, and detected renames do
not create submissions. Rename destinations reserve their identities to avoid
counting a later re-addition. Git rename detection is heuristic; an undetected
rename with a housekeeping message fails as an ambiguous addition. Deleting a
backup never erases historical practice. If NeetCode begins overwriting numbered
slots for genuinely new submissions, history cannot distinguish them from edits:
review the parser rather than silently treating edits as solves.

Distinct problems are counted across all included history, including undated
imports and deleted backups. Re-solving with a new submission number on a new
date counts as practice again; any number of submissions on one date creates
only one completed day. Difficulty totals count distinct problems, not attempts.

Ordinary activity uses **Git committer time**, normalized to UTC and converted
with Python `zoneinfo` to New York (including DST). Git author time is not used.
Sync time may differ from completion time. Manual imports that masquerade as
ordinary Add commits cannot reliably be detected. Review suspicious batches.

`commitPolicies` keys are full reachable commit SHAs; each value has `mode` and
a public, non-sensitive `reason`:

- `undated`: include identities in lifetime totals, omit calendar/recent activity.
- `exclude`: omit identities entirely, reserving them to prevent later re-adds.
- `dated`: explicitly approve additions; optional `timestamps` maps exact paths
  to offset-bearing original timestamps. Bulk commits require timestamps for
  every file. Use this only with trustworthy evidence, never invented dates.

The known 70-file import has an `undated` policy. It is not counted as 70 April 1
completions. Policies are published as provenance; never put secrets in them.
Unused policy SHAs and timestamp paths fail validation to catch typos or rewritten
history. For an ambiguous commit inspect `git show <sha>`, then add a justified
policy or extend parsing with a focused fixture and rerun.

## Schema version 1

`scripts/progress.py:validate` is the executable contract, called by both generator
and publisher and tested against invalid values and inconsistent totals. Breaking
field or semantic changes require a schema version bump. JSON is compact, ordered,
and deterministic for the same history/config/metadata except `generatedAt`.

| Field | Meaning |
| --- | --- |
| `schemaVersion` | Integer 1. |
| `generatedAt` | UTC build instant, ISO 8601 with `Z`. |
| `sourceCommit` | Full processed submission-history revision, not data-branch commit. |
| `source` | Public repository name and submission branch `main`. |
| `timezone` | `America/New_York`. |
| `challengeStartedAt` | Inclusive calendar date, or null if unconfigured. |
| `dataQuality` | Acceptance prerequisite, timestamp basis, limitations, applied policies. |
| `summary.submissions` | All included identities, accepted only by configured prerequisite. |
| `summary.distinctProblems` | All-history unique problems, including undated imports. |
| `summary.datedSubmissions` / `undatedSubmissions` | Partition of included identities. |
| `summary.activeDays` | All-history dated calendar days. |
| `summary.difficulty` | Unique problem counts by Easy/Medium/Hard/Unknown. |
| `dailyActivity` | All-history dated activity keyed by ascending `YYYY-MM-DD`; omitted dates have zero activity. |
| Daily `submissions` / `distinctProblems` | Included dated submission identities vs distinct problems on that date. Acceptance is conditional on the stated sync prerequisite. |
| `challenge` | Null if unconfigured; otherwise metrics restricted to dates on/after start. |
| `challenge.completedDays` | Distinct completed challenge dates. |
| `challenge.longestStreak` | Longest consecutive run within the challenge. |
| `challenge.lastCompletedDate` | Last completed challenge date, or null. |
| `challenge.streakEndingOnLastCompletedDate` | Consecutive run ending on that date; zero when no completed date. This is not a time-dependent current streak. |
| `recentSubmissions` | Latest up to 10 **dated** records across all history, descending recordedAt then ID. Undated imports are excluded. |

Each recent record has `id`, `problemId` (repository slug), `title`, `recordedAt`
(UTC), `localDate`, `timestampBasis` (`git-committer` or `override`), nullable
`difficulty`, nullable `topics`, `links`, and immutable `sourceUrl` pointing to its
creation commit. There are no authoritative missed-today/current-streak fields.

## Metadata

Edit `problems.json` keyed by the exact repository slug. Entries can supply
`title`, `difficulty` (Easy/Medium/Hard or null), `topics` (string array or null),
and `links` with separately verified `neetcode`/`leetcode` HTTPS URLs. Missing
difficulty/topics remain null and unknown problems count under Unknown. Fallback
titles are readable transformations of slugs, not verified official names.

The saved map contains all 973 problems from the public
[NeetCode All page](https://neetcode.io/practice/practice/allNC), as retrieved on
October 10, 2026 (New York). Titles, difficulties, categories, and links are parsed
from the page's main JavaScript bundle. `metadata-source.json` records its source,
retrieval time, and catalog totals. Categories become a one-element `topics` list.
The parser uses the catalog's `ncLink` slug when available, matching sync folder
names such as `two-integer-sum`; otherwise it uses the catalog's LeetCode link slug.
LeetCode links come from the catalog's explicit `link` field, and NeetCode links
are included only when `ncLink` is present. These are catalog-supplied links,
not separate checks of every destination. All 56 current repository slugs match.

Refresh the map deliberately when new problems are added or metadata changes:

```sh
python scripts/refresh_metadata.py
python -m unittest discover -s tests -v
python scripts/progress.py --require-accepted-only --output dashboard/progress.example.json
```

Review and commit `problems.json` and `metadata-source.json`. Pushing the map to
main triggers snapshot regeneration, updating metadata for past submissions too.
Submission workflows only read this saved map; they never scrape the website.
An unseen problem stays Unknown until the map is refreshed. The refresh script
does not execute downloaded JavaScript and rejects missing fields, duplicate IDs,
invalid difficulty values, or removal of existing map IDs. If the website changes
its bundle format, review the parser rather than replacing the map with guessed
data. Offline parsing is supported with `--bundle-file` and `--bundle-url`.

## Browser consumption, verification, and recovery

After the workflow publishes, check the endpoint returns HTTP 200 and parseable
JSON with `schemaVersion: 1`. Check its `Access-Control-Allow-Origin` header
permits the portfolio's origin (normally `*` for public raw files) and test an
actual browser fetch from the portfolio. These live checks have not been performed
by the local build; the endpoint depends on publication and public read access.
For example, inspect headers with `curl -I <endpoint>` and download/validate the
response using `validate(json.loads(...))` from the generator module.

The portfolio should fetch the public URL without credentials, validate the
version/required fields, and retain its last valid cached copy if the request or
validation fails. Show freshness using `generatedAt`; a successful fetch may
still return a cached snapshot. GitHub workflow queues take time and raw-file/CDN
caching can delay visibility by minutes; inspect response cache headers rather
than assuming an instant update or an exact TTL. Revalidate at a reasonable rate.

Compute today's New York date using an explicit `America/New_York` timezone.
Before challenge start show not-started. If today's date is completed, the streak
ending there is current. If yesterday is last completed, its ending streak is
still live while today is pending. If the last completed date is older, current
streak is zero. A day is only missed once its New York calendar date has ended;
use calendar-date arithmetic rather than subtracting 24 hours across DST. Refresh
derived status at the New York date boundary even without a new snapshot.

For failures, open the Actions run logs: tests, parsing diagnostics, configuration
errors, or a rejected push identify the failing stage. Fix on main and dispatch
again. A stale-source skip can be recovered with manual dispatch. If history was
rewritten, the ancestor check deliberately blocks publication; review/reconcile
the history before proceeding. Existing malformed published data likewise needs
explicit review, not an automatic destructive reset. No failure path deletes the
previous remote snapshot.
