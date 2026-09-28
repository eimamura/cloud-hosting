#!/usr/bin/env python3
"""Validate docs/catalog.yaml and keep the views derived from it in sync.

Usage:
  tools/catalog.py check [--max-age DAYS]   Validate the catalog and everything derived from it (exit 1 on errors).
  tools/catalog.py sync                     Regenerate the project table in README.md from the roadmap.

Requires PyYAML (`pip install pyyaml`).
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "docs" / "catalog.yaml"
README = ROOT / "README.md"
TABLE_START, TABLE_END = "<!-- projects:start -->", "<!-- projects:end -->"

# Top-level directories that are not deployment projects.
NON_PROJECT_DIRS = {"docs", "tools", "workloads"}

ROADMAP_KEYS = {"n", "idea", "workload", "hosting", "services", "method", "complexity", "learn",
                "status", "project", "url", "date"}
VENDOR_KEYS = {"name", "api", "cli", "mcp", "iac", "human", "agent_can", "rating", "rating_note", "checked", "sources"}
SERVICE_KEYS = {"id", "name", "category", "vendor", "rec", "complexity", "free_tier", "runtimes", "deploy", "notes",
                "use", "popularity", "commercial", "commercial_notes", "price", "agent_note", "skipped", "checked",
                "pricing"}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def load():
    return yaml.safe_load(CATALOG.read_text(encoding="utf-8"))


def as_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def project_rows(data):
    """Roadmap items that have a project directory, in roadmap order."""
    return [r for r in data["roadmap"] if r.get("project")]


def render_table(data):
    lines = ["| Project | Hosting | Workload | Status | URL |", "| ------- | ------- | -------- | ------ | --- |"]
    labels = data["enums"]["status"]
    for r in project_rows(data):
        lines.append(f"| [{r['project']}](./{r['project']}) | {r['hosting']} | {r['workload']} | "
                     f"{labels[r['status']]['label']} | {r.get('url', '')} |")
    return "\n".join(lines)


def replace_table(text, table):
    pattern = re.compile(re.escape(TABLE_START) + r".*?" + re.escape(TABLE_END), re.S)
    if not pattern.search(text):
        return None
    return pattern.sub(f"{TABLE_START}\n{table}\n{TABLE_END}", text)


def check_fields(rep, where, item, allowed, required):
    for key in item:
        if key not in allowed:
            rep.error(f"{where}: unknown field '{key}'")
    for key in required:
        if item.get(key) in (None, "", []):
            rep.error(f"{where}: missing '{key}'")


def check_enum(rep, where, enums, name, value):
    if value not in enums[name]:
        rep.error(f"{where}: {name} '{value}' is not one of {list(enums[name])}")


def check_links(rep, path):
    """Relative Markdown links must point at files or directories that exist."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        resolved = (path.parent / target.split("#")[0]).resolve()
        if not resolved.exists():
            rep.error(f"{path.relative_to(ROOT)}: broken link '{target}'")


def check(max_age):
    rep = Report()
    data = load()
    enums = data["enums"]
    vendors, services, roadmap = data["vendors"], data["services"], data["roadmap"]
    today = dt.date.today()

    # Vendors
    for vid, v in vendors.items():
        where = f"vendors.{vid}"
        check_fields(rep, where, v, VENDOR_KEYS, ["name", "mcp", "rating", "checked"])
        if not (v.get("api") or v.get("cli")):
            rep.error(f"{where}: needs 'api' or 'cli'")
        check_enum(rep, where, enums, "rating", v.get("rating"))
        check_enum(rep, where, enums, "mcp", (v.get("mcp") or {}).get("status"))
        checked = as_date(v.get("checked"))
        if not checked:
            rep.error(f"{where}: 'checked' must be a YYYY-MM-DD date")
        elif (today - checked).days > max_age:
            rep.warn(f"{where}: last checked {checked} (> {max_age} days ago)")

    # Services
    ids = [s.get("id") for s in services]
    for dup in {i for i in ids if ids.count(i) > 1}:
        rep.error(f"services: duplicate id '{dup}'")
    used_vendors = set()
    for s in services:
        where = f"services.{s.get('id', '?')}"
        required = ["id", "name", "category", "vendor", "rec", "complexity", "use", "popularity", "commercial",
                    "price", "checked"]
        if s.get("category") != "self-hosted":
            required.append("free_tier")
        check_fields(rep, where, s, SERVICE_KEYS, required)
        if s.get("id") and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s["id"]):
            rep.error(f"{where}: id must be kebab-case")
        check_enum(rep, where, enums, "category", s.get("category"))
        check_enum(rep, where, enums, "commercial", s.get("commercial"))
        check_enum(rep, where, enums, "rec", s.get("rec"))
        check_enum(rep, where, enums, "complexity", s.get("complexity"))
        check_enum(rep, where, enums, "popularity", s.get("popularity"))
        if "free_tier" in s:
            check_enum(rep, where, enums, "free_tier", s["free_tier"])
        refs = s.get("vendor") if isinstance(s.get("vendor"), list) else [s.get("vendor")]
        for ref in refs:
            used_vendors.add(ref)
            if ref not in vendors:
                rep.error(f"{where}: unknown vendor '{ref}'")
        checked = as_date(s.get("checked"))
        if not checked:
            rep.error(f"{where}: 'checked' must be a YYYY-MM-DD date")
        elif (today - checked).days > max_age:
            rep.warn(f"{where}: last checked {checked} (> {max_age} days ago)")
    for vid in set(vendors) - used_vendors:
        rep.error(f"vendors.{vid}: not referenced by any service")

    # Roadmap
    service_ids = set(ids)
    for i, r in enumerate(roadmap, start=1):
        where = f"roadmap #{r.get('n', '?')}"
        required = ["n", "idea", "workload", "hosting", "services", "method", "complexity", "learn", "status"]
        if r.get("status") in ("in-progress", "done"):
            required.append("project")
        if r.get("status") == "done":
            required += ["url", "date"]
        check_fields(rep, where, r, ROADMAP_KEYS, required)
        if r.get("n") != i:
            rep.error(f"{where}: expected n={i} (roadmap must be numbered 1..N in order)")
        check_enum(rep, where, enums, "status", r.get("status"))
        check_enum(rep, where, enums, "complexity", r.get("complexity"))
        for ref in r.get("services") or []:
            if ref not in service_ids:
                rep.error(f"{where}: unknown service '{ref}'")
            elif next(s for s in services if s["id"] == ref).get("skipped"):
                rep.error(f"{where}: service '{ref}' is marked skipped")
        if r.get("date") and not as_date(r["date"]):
            rep.error(f"{where}: 'date' must be a YYYY-MM-DD date")
        project = r.get("project")
        if project:
            if not (ROOT / project).is_dir():
                rep.error(f"{where}: project directory '{project}/' does not exist")
            elif not (ROOT / project / "README.md").is_file():
                rep.error(f"{where}: '{project}/README.md' is missing")

    # Every deployment project directory must be on the roadmap.
    projects = {r.get("project") for r in roadmap}
    for d in sorted(p.name for p in ROOT.iterdir() if p.is_dir()):
        if d.startswith(".") or d in NON_PROJECT_DIRS:
            continue
        if d not in projects:
            rep.error(f"'{d}/' looks like a deployment project but no roadmap item has project: {d}")

    # Derived README table
    readme = README.read_text(encoding="utf-8")
    expected = replace_table(readme, render_table(data))
    if expected is None:
        rep.error(f"README.md: missing {TABLE_START} ... {TABLE_END} markers")
    elif expected != readme:
        rep.error("README.md: project table is out of date; run `tools/catalog.py sync`")

    # Links in the Markdown docs
    for path in [README, ROOT / "AGENTS.md", *sorted((ROOT / "docs").glob("*.md")),
                 *(ROOT / p / "README.md" for p in projects if p and (ROOT / p / "README.md").is_file())]:
        check_links(rep, path)

    for w in rep.warnings:
        print(f"warning: {w}")
    for e in rep.errors:
        print(f"error: {e}")
    print(f"catalog: {len(roadmap)} roadmap items, {len(services)} services, {len(vendors)} vendors; "
          f"{len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


def sync():
    data = load()
    readme = README.read_text(encoding="utf-8")
    updated = replace_table(readme, render_table(data))
    if updated is None:
        print(f"README.md: missing {TABLE_START} ... {TABLE_END} markers", file=sys.stderr)
        return 1
    if updated != readme:
        README.write_text(updated, encoding="utf-8")
        print("README.md: project table updated")
    else:
        print("README.md: already up to date")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", default="check", choices=["check", "sync"])
    parser.add_argument("--max-age", type=int, default=180, help="warn when an entry was checked longer ago (days)")
    args = parser.parse_args()
    return check(args.max_age) if args.command == "check" else sync()


if __name__ == "__main__":
    sys.exit(main())
