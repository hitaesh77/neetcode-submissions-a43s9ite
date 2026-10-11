"""Refresh the checked-in problem map from NeetCode's public practice catalog.

Only string fields are parsed; downloaded JavaScript is never executed.
Submission builds use the saved map and do not depend on live website access.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from progress import check_config, require

PAGE = "https://neetcode.io/practice/practice/allNC"
STRING = r'"(?:\\.|[^"\\])*"'


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        source = dict(attrs).get("src", "")
        if tag == "script" and re.fullmatch(r"main\.[a-zA-Z0-9]+\.js", source):
            self.sources.append(urljoin(PAGE, source))


def download(url):
    request = Request(url, headers={"User-Agent": "NeetCodeProgressMetadata/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def parse_catalog(bundle):
    rows = re.findall(r'\{problem:' + STRING + r'[^{}]*\}', bundle)
    require(rows, "No catalog found; review the website format")
    result = {}
    for row in rows:
        fields = dict((key, json.loads(value)) for key, value in
                      re.findall(r'(\w+):(' + STRING + r')', row))
        require(all(fields.get(k) for k in ("problem", "pattern", "link", "difficulty")),
                "Incomplete catalog record")
        slug = fields.get("ncLink", fields["link"]).rstrip("/")
        require(slug not in result, f"Duplicate catalog ID: {slug}")
        links = {"leetcode": "https://leetcode.com/problems/" + fields["link"]}
        if fields.get("ncLink"):
            links["neetcode"] = "https://neetcode.io/problems/" + fields["ncLink"]
        result[slug] = {"title": fields["problem"], "difficulty": fields["difficulty"],
                        "topics": [fields["pattern"]], "links": links}
    check_config({"challengeStartedAt": None, "acceptedOnlyConfirmed": False,
                  "commitPolicies": {}}, result)
    return dict(sorted(result.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-file", help="Parse a previously downloaded bundle offline")
    parser.add_argument("--bundle-url", help="Source URL to record for an offline bundle")
    parser.add_argument("--output", default="dashboard/problems.json")
    parser.add_argument("--provenance", default="dashboard/metadata-source.json")
    args = parser.parse_args()
    if args.bundle_file:
        require(args.bundle_url, "Offline refresh requires --bundle-url for provenance")
        bundle_url = args.bundle_url
        bundle = Path(args.bundle_file).read_text(encoding="utf-8")
    else:
        scripts = Scripts()
        scripts.feed(download(PAGE))
        require(len(scripts.sources) == 1, "Expected one main bundle; review the website format")
        bundle_url = scripts.sources[0]
        bundle = download(bundle_url)
    metadata = parse_catalog(bundle)
    target = Path(args.output)
    if target.exists():
        old = json.loads(target.read_text(encoding="utf-8"))
        require(set(old) <= set(metadata), "Refresh would lose existing problem IDs; review catalog changes")
    provenance = {"sourcePage": PAGE, "sourceBundle": bundle_url,
                  "retrievedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  "problemCount": len(metadata),
                  "difficultyCounts": dict(Counter(m["difficulty"] for m in metadata.values())),
                  "idMapping": "ncLink when present; otherwise the catalog's LeetCode link slug"}
    # Parse and validate everything before replacing the saved map.
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(metadata, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    temporary.replace(target)
    Path(args.provenance).write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(provenance))


if __name__ == "__main__":
    main()
