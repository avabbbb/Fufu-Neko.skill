#!/usr/bin/env python3
"""Validate the public Fufu Neko package and its evaluation fixtures."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "fufu-neko"
SKILL_FILE = SKILL_DIR / "SKILL.md"
EVAL_DIR = ROOT / "evals"
EXPECTED_REFERENCES = (
    "references/persona/core.md",
    "references/persona/voice.md",
    "references/research-protocol.md",
    "references/ask-protocol.md",
    "references/agency-protocol.md",
    "references/collaboration-protocol.md",
    "references/grilling.md",
    "references/docs-protocol.md",
    "references/execution-protocol.md",
    "references/coding-principles.md",
    "references/evidence-policy.md",
    "references/response-style.md",
    "references/skill-conflict-protocol.md",
    "references/tool-bindings.md",
)
EXPECTED_ASSETS = (
    "assets/CONTEXT.template.md",
    "assets/ADR.template.md",
    "assets/private-soul.example.md",
)
EXPECTED_SCRIPTS = (
    "scripts/build_host_bundle.py",
    "scripts/validate_skill.py",
)
EXPECTED_EVALS = (
    "trigger.json",
    "negative-trigger.json",
    "research.json",
    "persona.json",
    "ask.json",
    "grill.json",
    "docs.json",
    "execution.json",
    "regression.json",
    "host-compatibility.json",
    "agency.json",
)
ALLOWED_FRONTMATTER = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKIP_DIRS = {".git", "soul", "node_modules", ".venv", "__pycache__", "dist", "build"}
TEXT_EXTENSIONS = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".toml", ".ini", ".gitignore", ""}


def legacy_tokens() -> tuple[str, ...]:
    return (
        "".join(("t", "r", "u", "m", "a", "n")),
        "".join(("d", "a", "r", "i", "o")),
        "".join(("楚", "门")),
        "".join(("t", "h", "e", " ", "t", "r", "u", "m", "a", "n", " ", "s", "h", "o", "w")),
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def public_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in relative_parts):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != ".gitignore":
            continue
        files.append(path)
    return files


def parse_frontmatter(content: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not content.startswith("---\n"):
        return {}, content, ["SKILL.md must start with YAML frontmatter"]

    lines = content.splitlines()
    closing = next((index for index in range(1, len(lines)) if lines[index].strip() == "---"), None)
    if closing is None:
        return {}, content, ["SKILL.md frontmatter has no closing delimiter"]

    frontmatter: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            continue
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not match:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = match.groups()
        frontmatter[key] = value.strip().strip("'\"")

    body = "\n".join(lines[closing + 1 :])
    return frontmatter, body, errors


def check_skill(errors: list[str]) -> None:
    if (ROOT / "SKILL.md").exists():
        errors.append("legacy root SKILL.md remains; the public entrypoint must be fufu-neko/SKILL.md")
    if not SKILL_FILE.exists():
        errors.append("fufu-neko/SKILL.md is missing")
        return

    content = read_text(SKILL_FILE)
    frontmatter, body, parse_errors = parse_frontmatter(content)
    errors.extend(parse_errors)
    unexpected = set(frontmatter) - ALLOWED_FRONTMATTER
    if unexpected:
        errors.append(f"unexpected frontmatter key(s): {', '.join(sorted(unexpected))}")
    if frontmatter.get("name") != "fufu-neko":
        errors.append("frontmatter name must be fufu-neko")
    if not frontmatter.get("description"):
        errors.append("frontmatter description is required")
    if len(frontmatter.get("description", "")) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")
    if len(content.splitlines()) >= 500:
        errors.append("fufu-neko/SKILL.md must stay under 500 lines")

    for relative in EXPECTED_REFERENCES + EXPECTED_ASSETS + EXPECTED_SCRIPTS:
        if not (SKILL_DIR / relative).exists():
            errors.append(f"missing bundled resource: {relative}")

    openai_metadata = SKILL_DIR / "agents" / "openai.yaml"
    if openai_metadata.exists():
        metadata = read_text(openai_metadata)
        for required in ("interface:", "short_description:", "policy:", "allow_implicit_invocation:"):
            if required not in metadata:
                errors.append(f"agents/openai.yaml is missing expected Codex metadata: {required}")



def check_relative_links(errors: list[str]) -> None:
    for path in public_files():
        if path.suffix.lower() != ".md":
            continue
        content = read_text(path)
        for match in re.finditer(r"\]\(([^)]+)\)", content):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken relative link in {path.relative_to(ROOT)}: {target}")


def check_public_brand(errors: list[str]) -> None:
    offenders: list[str] = []
    tokens = legacy_tokens()
    for path in public_files():
        if path == Path(__file__).resolve():
            continue
        try:
            content = read_text(path).lower()
        except UnicodeDecodeError:
            continue
        if any(token.lower() in content for token in tokens):
            offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        errors.append("former branding remains in public files: " + ", ".join(sorted(offenders)))


def check_goal_semantics(errors: list[str]) -> None:
    goal = "/" + "goal"
    exit_words = ("ex" + "it", "退出", "st" + "op", "o" + "ff")
    bad_patterns = (
        re.compile(rf"{re.escape(goal)}\s*(?:=|:|→|->)\s*(?:exit|stop|off|退出)", re.IGNORECASE),
        re.compile(rf"(?:use|run|输入|使用)\s+{re.escape(goal)}.{{0,30}}(?:exit|stop|off|退出)", re.IGNORECASE),
    )
    for path in public_files():
        if path == Path(__file__).resolve():
            continue
        content = read_text(path)
        if any(pattern.search(content) for pattern in bad_patterns):
            errors.append(f"host completion command is given an opt-out meaning in {path.relative_to(ROOT)}")
        if goal in content and any(word in content for word in exit_words):
            suspicious = [word for word in exit_words if word in content]
            if suspicious and "completion" not in content.lower():
                errors.append(f"review /goal wording in {path.relative_to(ROOT)}: {', '.join(suspicious)}")


def check_agency_contract(errors: list[str]) -> None:
    if not SKILL_FILE.exists():
        return
    skill_content = read_text(SKILL_FILE)
    required = (
        "## Working state",
        "task_intent_resolved",
        "authorization_scope",
        "open_human_decisions",
        "execution_state",
        "Do reversible, in-scope work without redundant confirmation.",
        "Continue through failures and regression checks",
        "Explicit user instructions override Fufu defaults",
    )
    for phrase in required:
        if phrase not in skill_content:
            errors.append(f"SKILL.md is missing Agency invariant: {phrase}")

    stale_patterns = {
        "legacy scope state": re.compile(r"\b(?:scope_locked|execution_authorized)\b"),
        "legacy approval-before-implementation gate": re.compile(
            r"before\s+substantial\s+(?:mutation|implementation).{0,120}(?:approval|approve)",
            re.IGNORECASE | re.DOTALL,
        ),
        "legacy scope-lock phrase": re.compile(r"\bscope\s+lock\b", re.IGNORECASE),
    }
    current_validator = Path(__file__).resolve()
    for path in public_files():
        if path == current_validator:
            continue
        content = read_text(path)
        for label, pattern in stale_patterns.items():
            if pattern.search(content):
                errors.append(f"{label} remains in public file {path.relative_to(ROOT)}")


def check_duplicate_paragraphs(errors: list[str]) -> None:
    seen: dict[str, list[str]] = defaultdict(list)
    for path in public_files():
        if path.suffix.lower() != ".md":
            continue
        paragraphs = re.split(r"\n\s*\n", read_text(path))
        for paragraph in paragraphs:
            normalized = re.sub(r"\s+", " ", paragraph).strip().lower()
            if len(normalized) >= 120 and not normalized.startswith("```"):
                seen[normalized].append(str(path.relative_to(ROOT)))
    duplicates = [paths for paths in seen.values() if len(paths) > 1]
    if duplicates:
        errors.append("duplicate long instruction paragraphs found: " + "; ".join(", ".join(paths) for paths in duplicates))


def check_evals(errors: list[str]) -> None:
    for filename in EXPECTED_EVALS:
        path = EVAL_DIR / filename
        if not path.exists():
            errors.append(f"missing evaluation suite: evals/{filename}")
            continue
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON in evals/{filename}: {exc}")
            continue
        if not isinstance(data, dict) or not isinstance(data.get("cases"), list) or not data["cases"]:
            errors.append(f"evals/{filename} must contain a non-empty cases array")
            continue
        for case in data["cases"]:
            if not isinstance(case, dict):
                errors.append(f"evals/{filename} contains a non-object case")
                continue
            for key in ("id", "prompt", "must", "must_not"):
                if key not in case:
                    errors.append(f"evals/{filename} case is missing {key}")
            if not isinstance(case.get("must", []), list) or not isinstance(case.get("must_not", []), list):
                errors.append(f"evals/{filename} case {case.get('id', '<unknown>')} has invalid assertions")


def check_readme(errors: list[str]) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        errors.append("README.md is missing")
        return
    content = read_text(path)
    for required in (
        "fufu-neko/SKILL.md",
        "/fufu-neko",
        "soul/",
        "Codex",
        "WorkBuddy",
        "TeleAgent",
        "build_host_bundle.py",
        "agency-protocol.md",
        "collaboration-protocol.md",
        "response-style.md",
        "skill-conflict-protocol.md",
    ):
        if required not in content:
            errors.append(f"README.md is missing required installation or privacy text: {required}")


def check_private_soul(errors: list[str], warnings: list[str]) -> None:
    private_dir = ROOT / "soul"
    if not private_dir.exists():
        warnings.append("no local soul/ directory is present; only the public persona is being validated")
        return

    ignore_file = ROOT / ".gitignore"
    ignored = ignore_file.exists() and re.search(r"(?m)^/?soul/?$", read_text(ignore_file))
    if not ignored:
        errors.append("local soul/ exists but is not protected by .gitignore")

    try:
        result = subprocess.run(
            ["git", "ls-files", "--", "soul"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        tracked = [line for line in result.stdout.splitlines() if line.strip()]
    except OSError:
        tracked = []
        warnings.append("git is unavailable; tracked/private soul status could not be checked")
    if tracked:
        errors.append("private soul files are still tracked: " + ", ".join(tracked))

    patterns = {
        "credential-like fields": re.compile(r"(?i)\b(?:api[_-]?key|token|secret|password)\b\s*[:=]"),
        "machine paths": re.compile(r"(?i)(?:[a-z]:\\|/users/|/home/|\\\\[a-z0-9_.-]+\\)"),
        "private profile labels": re.compile(r"(?i)\b(?:user profile|personal profile|private memory)\b"),
    }
    counts = defaultdict(int)
    for path in private_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            content = read_text(path)
        except UnicodeDecodeError:
            continue
        for label, pattern in patterns.items():
            if pattern.search(content):
                counts[label] += 1
    if counts:
        warnings.append("private soul audit found sensitive-looking content kept under ignored soul/: " + ", ".join(sorted(counts)))
    else:
        warnings.append("private soul audit found no configured sensitive-looking patterns")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    check_skill(errors)
    check_relative_links(errors)
    check_public_brand(errors)
    check_goal_semantics(errors)
    check_agency_contract(errors)
    check_duplicate_paragraphs(errors)
    check_evals(errors)
    check_readme(errors)
    check_private_soul(errors, warnings)

    if errors:
        print("FAIL Fufu Neko validation")
        for error in errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"WARN - {warning}")
        return 1

    print("PASS Fufu Neko validation")
    for warning in warnings:
        print(f"WARN - {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
