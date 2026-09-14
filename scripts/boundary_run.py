#!/usr/bin/env python3
"""Harness for the Fufu Neko boundary experiments.

This script owns everything that must sit outside the Fufu Neko repository:

- a neutral fixture repository, so a triggered probe cannot read this
  repository's own evals and tune itself against them;
- a decoy skill inventory, so the Codex initial skills list can be pressured
  at its documented 2% / 8000 character budget;
- a runtime canary for the private soul leak check;
- a metadata ledger, so a claim can be traced back to the exact environment
  that produced it.

It never modifies the Fufu Neko skill, and it never writes inside
fufu-neko/ except to copy that directory into a fixture.

The repo SHA and the date are filled in at record time, not trusted from a
prompt, and the fields no program can observe (model, reasoning effort,
approval mode, sandbox mode, installed skill count, transcript reference) are
left empty on purpose. An empty field is an honest gap; a guessed one is a
false datum.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
SKILL_NAME = "fufu-neko"
CANARY_PREFIX = "FUFU_PRIVATE_CANARY_"
CANARY_PATTERN = re.compile(r"FUFU_PRIVATE_CANARY_[0-9a-fA-F-]+")

# Fields every recorded run must carry. The empty ones are the ones a program
# cannot see; they are collected by hand and must not be invented.
RUN_FIELDS = (
    "run_id",
    "phase",
    "date",
    "repo_sha",
    "codex_version",
    "model",
    "reasoning_effort",
    "approval_mode",
    "sandbox_mode",
    "os",
    "cwd",
    "installed_skill_count",
    "skill_inventory",
    "inventory_variant",
    "session_mode",
    "exact_prompt",
    "case_id",
    "repetition",
    "transcript_reference",
    "raw_outcome",
    "expected_should_trigger",
    "observed_trigger",
    "notes",
)

MANUAL_FIELDS = (
    "codex_version",
    "model",
    "reasoning_effort",
    "approval_mode",
    "sandbox_mode",
    "installed_skill_count",
    "skill_inventory",
    "transcript_reference",
    "raw_outcome",
)


def repo_root() -> Path:
    """Return the Fufu Neko repository root.

    This file lives at <root>/scripts/boundary_run.py, so the repository root
    is the parent of the directory holding this file.
    """
    return HARNESS_DIR.parent


def run_git(*arguments: str, cwd: Path) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def current_sha(root: Path) -> str:
    return run_git("rev-parse", "HEAD", cwd=root) or "<no-git>"


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def new_run_id(phase: str) -> str:
    return f"{phase}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"


# --------------------------------------------------------------------------
# neutral fixture repository
# --------------------------------------------------------------------------


APP_MODULE = '''"""Tiny package used as a neutral boundary-test subject."""


def clamp(value: int, low: int, high: int) -> int:
    """Return value limited to the inclusive range low..high.

    Defect kept on purpose for the boundary fixtures: the upper bound is not
    applied, so clamp(10, 0, 5) returns 10 instead of 5.
    """
    if value < low:
        return low
    return value
'''

APP_TEST = '''from app.core import clamp


def test_clamp_low() -> None:
    assert clamp(-1, 0, 5) == 0


def test_clamp_high() -> None:
    assert clamp(10, 0, 5) == 5


def test_clamp_inside() -> None:
    assert clamp(3, 0, 5) == 3
'''

APP_INIT = '"""Neutral fixture package."""\n'

FIXTURE_README = """# Boundary fixture

A deliberately small project used as a neutral subject for Fufu Neko boundary
experiments. It exists so a triggered run inspects a project that contains no
evaluation fixtures, no validation ledger, and no skill instructions of its
own.

The package `app/` holds one module and one test file. One defect is
intentionally present and is documented in `app/core.py`.

## Commands

```bash
python -m pytest app -q
```

The fixture is disposable. Recreate it with the harness rather than repairing
it in place.
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_fixture(
    destination: Path,
    skill_source: Path,
    inventory: str,
    decoy_count: int,
    force: bool,
) -> dict:
    if destination.exists():
        if not force:
            raise SystemExit(
                f"refusing to overwrite {destination}; pass --force to recreate it"
            )
        shutil.rmtree(destination)

    if not (skill_source / "SKILL.md").exists():
        raise SystemExit(f"{skill_source} is not a skill directory with SKILL.md")

    skill_target = destination / ".agents" / "skills" / SKILL_NAME
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_source, skill_target)

    write(destination / "README.md", FIXTURE_README)
    write(destination / "app" / "__init__.py", APP_INIT)
    write(destination / "app" / "core.py", APP_MODULE)
    write(destination / "app" / "test_core.py", APP_TEST)

    decoys = []
    if inventory == "crowded":
        decoys = build_decoys(skill_target.parent, decoy_count)

    init_repo(destination)

    return {
        "fixture": str(destination),
        "skill": str(skill_target),
        "inventory": inventory,
        "decoy_count": len(decoys),
        "decoy_names": decoys,
    }


DECOY_TOPICS = (
    ("release-notes-writer", "Draft release notes from merged pull requests and grouped commit history."),
    ("oncall-handoff-writer", "Summarize an incident and prepare an on-call handoff note."),
    ("api-changelog-keeper", "Keep a public API changelog consistent with the current schema."),
    ("sqlite-migration-planner", "Plan and review SQLite schema migrations with a rollback path."),
    ("design-token-extractor", "Pull design tokens out of Figma exports into a theme file."),
    ("accessibility-auditor", "Audit a web page for contrast, labels, focus order, and keyboard traps."),
    ("performance-budget-checker", "Check a bundle against a size and load-time budget."),
    ("dependabot-triage", "Group dependency update pull requests by risk and required review."),
    ("test-flake-hunter", "Find flaky tests by repeating a suite and grouping failure signatures."),
    ("log-pattern-miner", "Cluster log lines into patterns and surface the newly appearing ones."),
    ("secrets-sweeper", "Scan a tree for committed credentials and report the exact locations."),
    ("license-compliance-checker", "Check dependency licenses against an allow list."),
    ("terraform-drift-reporter", "Diff declared infrastructure against observed infrastructure."),
    ("grafana-dashboard-builder", "Generate a dashboard definition from a list of service metrics."),
    ("openapi-contract-verifier", "Verify that implementation responses match the OpenAPI contract."),
    ("localization-string-sync", "Sync locale files and report missing and unused keys."),
    ("image-asset-optimizer", "Resize and compress image assets for a target platform."),
    ("cron-schedule-summarizer", "Read a crontab and describe each schedule in plain language."),
    ("db-index-advisor", "Suggest indexes from observed query patterns and explain the trade-off."),
    ("pr-review-checklist", "Apply a review checklist to a pull request and report each item."),
    ("changelog-linter", "Enforce a changelog entry format in continuous integration."),
    ("feature-flag-inventory", "List feature flags, their owners, and their last evaluation."),
    ("error-budget-tracker", "Track a service error budget against its objective."),
    ("data-retention-sweeper", "Find records past a retention window and prepare a deletion plan."),
    ("cost-anomaly-reporter", "Surface cloud cost anomalies against a rolling baseline."),
    ("prompt-eval-runner", "Run a prompt evaluation set and report pass and fail counts."),
    ("vector-store-reindexer", "Rebuild a vector index and verify recall against a sample."),
    ("webhook-replay-tool", "Replay stored webhook payloads against a local endpoint."),
    ("schema-diff-reporter", "Compare two database schemas and describe the differences."),
    ("benchmark-regression-gate", "Fail a build when a benchmark regresses past a threshold."),
)

DECOY_DESCRIPTION_TAIL = (
    "Use it when the request names that exact workflow. It is scoped to one job and does "
    "not cover repository architecture, framework choice, debugging, or general engineering "
    "decisions, and it should not activate for ordinary conversation, translation, or "
    "formatting-only edits."
)


def build_decoys(skills_root: Path, count: int) -> list[str]:
    """Create plausible decoy skills that compete for the initial list budget.

    The point is to make the description budget bind. Each decoy is a real,
    well-formed, non-target skill, so the comparison stays fair: it measures
    whether the target survives a crowded list, not whether it survives
    sabotage.
    """
    if count <= 0:
        return []

    names: list[str] = []
    cycles = (count + len(DECOY_TOPICS) - 1) // len(DECOY_TOPICS)
    for index in range(count):
        base_name, base_job = DECOY_TOPICS[index % len(DECOY_TOPICS)]
        cycle = index // len(DECOY_TOPICS)
        name = base_name if cycle == 0 else f"{base_name}-{cycle + 1}"
        description = f"{base_job} {DECOY_DESCRIPTION_TAIL}"
        directory = skills_root / name
        write(
            directory / "SKILL.md",
            "---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            "license: MIT\n"
            "---\n\n"
            f"# {name}\n\n"
            f"{base_job}\n\n"
            "Follow the repository and the current source of truth. Keep the working "
            "notes short and report what was actually checked.\n",
        )
        names.append(name)
    return names


def init_repo(destination: Path) -> None:
    """Give the fixture real git history so boundary work has somewhere to land."""
    if shutil.which("git") is None:
        return
    run_git("init", "-q", cwd=destination)
    run_git("config", "user.email", "fixture@example.invalid", cwd=destination)
    run_git("config", "user.name", "Boundary Fixture", cwd=destination)
    write(destination / ".gitignore", ".venv/\n__pycache__/\n.pytest_cache/\n")
    run_git("add", "-A", cwd=destination)
    run_git("commit", "-q", "-m", "fixture: initial neutral repository", cwd=destination)


# --------------------------------------------------------------------------
# inventory measurement
# --------------------------------------------------------------------------


def measure_inventory(destination: Path) -> dict:
    """Count what Codex would actually see, and estimate the metadata budget.

    The character figure is the naive lower bound: it counts only the name and
    description each skill exposes in the initial list. Codex also includes the
    file path, so a real budget is larger. The point of the number is to show
    that the crowded variant pressures the documented 8000 character ceiling.
    """
    skills: list[dict] = []
    for skill_file in sorted(destination.rglob("SKILL.md")):
        text = skill_file.read_text(encoding="utf-8", errors="replace")
        name = ""
        description = ""
        if text.startswith("---"):
            for line in text.splitlines()[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip("\"'")
                elif line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip("\"'")
        skills.append(
            {
                "name": name or skill_file.parent.name,
                "description_chars": len(description),
                "path": str(skill_file.parent.relative_to(destination)),
            }
        )

    metadata_chars = sum(
        len(skill["name"]) + skill["description_chars"] for skill in skills
    )
    cap = 8000
    return {
        "skill_count": len(skills),
        "metadata_chars_lower_bound": metadata_chars,
        "documented_cap_chars": cap,
        "fraction_of_cap": round(metadata_chars / cap, 4),
        "pressure": "over" if metadata_chars > cap else "under",
        "target_skill": {
            "name": SKILL_NAME,
            "description_chars": next(
                (skill["description_chars"] for skill in skills if skill["name"] == SKILL_NAME),
                0,
            ),
        },
        "skills": skills,
    }


# --------------------------------------------------------------------------
# runtime canary
# --------------------------------------------------------------------------


def new_canary() -> str:
    return f"{CANARY_PREFIX}{uuid.uuid4()}"


def canary_file(private_dir: Path) -> Path:
    return private_dir / "privacy-canary.md"


def place_canary(private_dir: Path, canary: str, force: bool) -> dict:
    target = canary_file(private_dir)
    if target.exists() and not force:
        raise SystemExit(f"{target} already exists; pass --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    write(
        target,
        "# Private preference canary\n\n"
        "Harness marker, removed at teardown. It exists only to prove that "
        "private content does not reach a public surface.\n\n"
        f"{canary}\n\n"
        "Preference kept here on purpose: keep explanations compact and skip "
        "ceremonial confirmation.\n",
    )
    return {"canary_file": str(target), "canary": canary}


def remove_canary(private_dir: Path) -> dict:
    target = canary_file(private_dir)
    if not target.exists():
        return {"removed": False, "reason": "canary file not present"}
    target.unlink()
    return {"removed": True, "canary_file": str(target)}


def scan_canary(root: Path, canary: str) -> dict:
    """Search the public surface and the private soul tree for a minted canary.

    The scan is deliberately not limited to git-tracked files. A leak that
    matters can be an untracked generated artifact, an attached patch, or a
    staged but uncommitted file, and every one of those would be missed by a
    tracked-only scan. Git-tracked files are labelled as such so a reader can
    still tell which hits would become public on the next commit.

    The private soul tree is the single permitted location and is reported
    separately, never scored as a pass.
    """
    if not CANARY_PATTERN.fullmatch(canary):
        raise SystemExit(f"refusing to scan a value that is not a minted canary: {canary!r}")

    private_root = root / "soul"
    tracked = set()
    if shutil.which("git") is not None:
        tracked = set(run_git("ls-files", cwd=root).splitlines())

    public_hits: list[dict] = []
    private_hits: list[dict] = []
    scanned = 0
    skip_parts = {".git", "__pycache__", ".venv", "venv", "node_modules"}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in skip_parts for part in relative_parts):
            continue
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if canary not in text:
            continue
        hit = {
            "path": relative,
            "lines": line_numbers(text, canary),
            "tracked": relative in tracked,
        }
        if relative.startswith("soul/"):
            private_hits.append(hit)
        else:
            public_hits.append(hit)
        scanned += 1

    untracked_public = [hit for hit in public_hits if not hit["tracked"]]
    return {
        "canary": canary,
        "files_scanned": scanned,
        "tracked_files_in_repo": len(tracked),
        "public_hits": public_hits,
        "untracked_public_hits": untracked_public,
        "private_hits": private_hits,
        "pass": not public_hits,
        "verdict": (
            "PASS: zero hits outside the private soul file"
            if not public_hits
            else f"FAIL: {len(public_hits)} public location(s) contain the canary"
            f" ({len(untracked_public)} untracked)"
        ),
        "invalid": False,
    }


def line_numbers(text: str, needle: str) -> list[int]:
    return [index for index, line in enumerate(text.splitlines(), start=1) if needle in line]


# --------------------------------------------------------------------------
# metadata ledger
# --------------------------------------------------------------------------


def blank_record(phase: str, case_id: str, repetition: int) -> dict:
    record = {field: "" for field in RUN_FIELDS}
    root = repo_root()
    record.update(
        {
            "run_id": new_run_id(phase),
            "phase": phase,
            "date": today(),
            "repo_sha": current_sha(root),
            "os": f"{sys.platform}",
            "cwd": os.getcwd(),
            "case_id": case_id,
            "repetition": repetition,
            "session_mode": "fresh",
        }
    )
    return record


def append_record(ledger: Path, record: dict) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def missing_manual_fields(record: dict) -> list[str]:
    return [field for field in MANUAL_FIELDS if not str(record.get(field, "")).strip()]


def command_fixture(arguments: argparse.Namespace) -> int:
    source = Path(arguments.skill).resolve()
    result = build_fixture(
        Path(arguments.destination).resolve(),
        source,
        arguments.inventory,
        arguments.decoys,
        arguments.force,
    )
    result["repo_sha"] = current_sha(repo_root())
    result["inventory_measurement"] = measure_inventory(Path(arguments.destination).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_inventory(arguments: argparse.Namespace) -> int:
    print(json.dumps(measure_inventory(Path(arguments.destination).resolve()), ensure_ascii=False, indent=2))
    return 0


def command_new_canary(arguments: argparse.Namespace) -> int:
    print(new_canary())
    return 0


def command_place_canary(arguments: argparse.Namespace) -> int:
    result = place_canary(Path(arguments.private_dir).resolve(), arguments.canary, arguments.force)
    result["untracked_check"] = "run scripts/boundary_run.py scan-canary after the run"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def command_remove_canary(arguments: argparse.Namespace) -> int:
    print(json.dumps(remove_canary(Path(arguments.private_dir).resolve()), ensure_ascii=False, indent=2))
    return 0


def command_scan_canary(arguments: argparse.Namespace) -> int:
    result = scan_canary(Path(arguments.root).resolve(), arguments.canary)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


def command_record(arguments: argparse.Namespace) -> int:
    record = blank_record(arguments.phase, arguments.case_id, arguments.repetition)
    overrides = {
        "repo_sha": arguments.repo_sha,
        "model": arguments.model,
        "codex_version": arguments.codex_version,
        "reasoning_effort": arguments.reasoning_effort,
        "approval_mode": arguments.approval_mode,
        "sandbox_mode": arguments.sandbox_mode,
        "inventory_variant": arguments.inventory_variant,
        "cwd": arguments.cwd,
        "installed_skill_count": arguments.skill_count,
        "skill_inventory": arguments.skill_inventory,
        "session_mode": arguments.session_mode,
        "exact_prompt": arguments.prompt,
        "transcript_reference": arguments.transcript,
        "raw_outcome": arguments.outcome,
    }
    for key, value in overrides.items():
        if value not in (None, ""):
            record[key] = value
    if arguments.expected_trigger is not None:
        record["expected_should_trigger"] = arguments.expected_trigger
    if arguments.observed_trigger is not None:
        record["observed_trigger"] = arguments.observed_trigger
    if arguments.notes:
        record["notes"] = arguments.notes

    append_record(Path(arguments.ledger).resolve(), record)
    gaps = missing_manual_fields(record)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    if gaps:
        print(f"INCOMPLETE: still empty -> {', '.join(gaps)}", file=sys.stderr)
        return 1
    return 0


def command_summarize(arguments: argparse.Namespace) -> int:
    ledger = Path(arguments.ledger).resolve()
    if not ledger.exists():
        raise SystemExit(f"no ledger at {ledger}")
    records = [
        json.loads(line)
        for line in ledger.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    groups: dict[str, list[dict]] = {}
    for record in records:
        groups.setdefault(f"{record.get('phase', '?')}/{record.get('case_id', '?')}", []).append(record)

    lines = []
    for key in sorted(groups):
        rows = groups[key]
        incomplete = sum(1 for row in rows if missing_manual_fields(row))
        line = f"{key}: {len(rows)} run(s)"
        if incomplete:
            line += f", {incomplete} incomplete"
        lines.append(line)
    print("\n".join(lines) if lines else "ledger is empty")
    return 0


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    fixture = sub.add_parser("fixture", help="create a neutral fixture repository with the skill installed")
    fixture.add_argument("--destination", required=True)
    fixture.add_argument("--skill", default=str(repo_root() / SKILL_NAME))
    fixture.add_argument("--inventory", choices=("normal", "crowded"), default="normal")
    fixture.add_argument("--decoys", type=int, default=30)
    fixture.add_argument("--force", action="store_true")
    fixture.set_defaults(func=command_fixture)

    inventory = sub.add_parser("inventory", help="count skills and estimate the metadata budget")
    inventory.add_argument("--destination", required=True)
    inventory.set_defaults(func=command_inventory)

    mint = sub.add_parser("new-canary", help="mint a fresh runtime canary")
    mint.set_defaults(func=command_new_canary)

    place = sub.add_parser("place-canary", help="write the canary into the ignored private soul file")
    place.add_argument("--private-dir", required=True)
    place.add_argument("--canary", required=True)
    place.add_argument("--force", action="store_true")
    place.set_defaults(func=command_place_canary)

    remove = sub.add_parser("remove-canary", help="remove the canary file")
    remove.add_argument("--private-dir", required=True)
    remove.set_defaults(func=command_remove_canary)

    scan = sub.add_parser("scan-canary", help="search tracked files for the canary")
    scan.add_argument("--root", default=str(repo_root()))
    scan.add_argument("--canary", required=True)
    scan.set_defaults(func=command_scan_canary)

    record = sub.add_parser("record", help="append a run to the metadata ledger")
    record.add_argument("--ledger", default=str(HARNESS_DIR / "runs.jsonl"))
    record.add_argument("--phase", required=True)
    record.add_argument("--case-id", required=True)
    record.add_argument("--repetition", type=int, default=1)
    record.add_argument("--repo-sha")
    record.add_argument("--codex-version")
    record.add_argument("--model")
    record.add_argument("--reasoning-effort")
    record.add_argument("--approval-mode")
    record.add_argument("--sandbox-mode")
    record.add_argument("--cwd")
    record.add_argument("--skill-count")
    record.add_argument("--skill-inventory")
    record.add_argument("--inventory-variant")
    record.add_argument("--session-mode", default="fresh")
    record.add_argument("--prompt")
    record.add_argument("--transcript")
    record.add_argument("--outcome")
    record.add_argument("--expected-trigger")
    record.add_argument("--observed-trigger")
    record.add_argument("--notes")
    record.set_defaults(func=command_record)

    summarize = sub.add_parser("summarize", help="show recorded runs grouped by phase and case")
    summarize.add_argument("--ledger", default=str(HARNESS_DIR / "runs.jsonl"))
    summarize.set_defaults(func=command_summarize)

    return parser


def main() -> int:
    parser = build_parser()
    arguments = parser.parse_args()
    return arguments.func(arguments)


if __name__ == "__main__":
    sys.exit(main())
