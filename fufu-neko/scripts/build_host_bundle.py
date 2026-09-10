#!/usr/bin/env python3
"""Build standalone host bundles from the canonical Fufu Neko skill.

The canonical package keeps standard Agent Skills frontmatter. Some hosts add
their own marketplace metadata, so this script creates a disposable bundle with
that metadata without maintaining a second hand-edited instruction set.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "fufu-neko"
DEFAULT_OUTPUT = ROOT / "dist"
REFERENCE_FILES = (
    "references/persona/core.md",
    "references/persona/voice.md",
    "references/research-protocol.md",
    "references/ask-protocol.md",
    "references/grilling.md",
    "references/docs-protocol.md",
    "references/execution-protocol.md",
    "references/coding-principles.md",
    "references/evidence-policy.md",
    "references/tool-bindings.md",
)


HOSTS = {
    "codex": {
        "author": "avabbbb",
    },
    "workbuddy": {
        "display_name": "Fufu Neko",
        "display_name_en": "Fufu Neko",
        "description_zh": "代码库优先、研究当前现实、拷打重要设计并持续执行验证的猫娘工程搭档。",
        "description_en": "A codebase-first engineering partner that checks current reality, grills important decisions, and executes and verifies after scope approval.",
        "category": "engineering",
        "author": "avabbbb",
    },
    "teleagent": {
        "name_cn": "福福猫娘工程搭档",
        "description_cn": "代码库优先、会核对当前资料、会追问关键决策并在确认范围后持续执行和验证的工程技能。",
        "description_zh": "代码库优先、研究当前现实、拷打重要设计并持续执行验证的猫娘工程搭档。",
        "description_en": "A codebase-first engineering partner that checks current reality, grills important decisions, and executes and verifies after scope approval.",
        "category": "engineering",
        "author": "avabbbb",
    },
}


def yaml_scalar(value: object) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def split_frontmatter(content: str) -> tuple[list[str], str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("canonical SKILL.md has no opening frontmatter delimiter")
    try:
        closing = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise ValueError("canonical SKILL.md has no closing frontmatter delimiter") from exc
    return lines[1:closing], "\n".join(lines[closing + 1 :]).lstrip("\n")


def frontmatter_values(lines: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in lines:
        if not line.strip() or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def host_frontmatter(host: str, canonical: dict[str, str]) -> list[str]:
    description = canonical.get("description", "")
    metadata = HOSTS[host]
    if host == "codex":
        return [
            "name: fufu-neko",
            f"description: {yaml_scalar(description)}",
            "license: MIT",
            "metadata:",
            f"  author: {yaml_scalar(metadata['author'])}",
            '  version: "2.0.0"',
        ]

    lines = [
        "name: fufu-neko",
        f"description: {yaml_scalar(description)}",
    ]
    ordered_keys = (
        "display_name",
        "display_name_en",
        "name_cn",
        "description_zh",
        "description_cn",
        "description_en",
        "category",
    )
    for key in ordered_keys:
        if key in metadata:
            lines.append(f"{key}: {yaml_scalar(metadata[key])}")
    lines.extend(
        [
            'version: "2.0.0"',
            f"author: {yaml_scalar(metadata['author'])}",
            "license: MIT",
        ]
    )
    return lines


def host_loading_note(host: str) -> str:
    lines = [
        "## Host loading note",
        "",
        "This bundle is generated from the canonical Fufu Neko package. Keep its bundled references beside this file.",
        "Load a referenced file only when the current task needs it; do not flatten all references into every response.",
        "",
    ]
    if host == "workbuddy":
        lines.extend(
            [
                "WorkBuddy reference hints:",
                *[f"- @{path}" for path in REFERENCE_FILES],
                "",
                "Use WorkBuddy's native question and permission behavior when available; otherwise use the structured choice fallback in the protocol.",
            ]
        )
    elif host == "teleagent":
        lines.extend(
            [
                "TeleAgent reference hints:",
                *[f"- {path}" for path in REFERENCE_FILES],
                "",
                "Use TeleAgent's native skill invocation, file access, and confirmation behavior. The bundle does not grant extra permissions.",
            ]
        )
    else:
        lines.extend(
            [
                "Codex reference hints:",
                *[f"- {path}" for path in REFERENCE_FILES],
                "",
                "Use Codex's native `$` skill invocation and available tools.",
            ]
        )
    return "\n".join(lines)


def ensure_within(parent: Path, child: Path) -> None:
    parent_resolved = parent.resolve()
    child_resolved = child.resolve()
    try:
        child_resolved.relative_to(parent_resolved)
    except ValueError as exc:
        raise ValueError(f"refusing to write outside {parent_resolved}: {child_resolved}") from exc


def build(host: str, output_root: Path) -> Path:
    if not CANONICAL.is_dir() or not (CANONICAL / "SKILL.md").is_file():
        raise FileNotFoundError(f"canonical skill is missing: {CANONICAL}")

    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    destination = output_root / host / "fufu-neko"
    ensure_within(output_root, destination)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(CANONICAL, destination)

    if host == "workbuddy":
        # WorkBuddy's Open Platform documents templates/ as its conventional
        # output-resource directory. Keep assets/ too so the canonical package
        # remains intact, but expose the same templates under that convention.
        shutil.copytree(destination / "assets", destination / "templates", dirs_exist_ok=True)

    source_content = (CANONICAL / "SKILL.md").read_text(encoding="utf-8")
    source_lines, body = split_frontmatter(source_content)
    canonical_values = frontmatter_values(source_lines)
    generated_body = host_loading_note(host) + "\n\n" + body.rstrip() + "\n"
    generated = "---\n" + "\n".join(host_frontmatter(host, canonical_values)) + "\n---\n\n" + generated_body
    with (destination / "SKILL.md").open("w", encoding="utf-8", newline="\n") as skill_file:
        skill_file.write(generated)

    if host != "codex":
        openai_metadata = destination / "agents" / "openai.yaml"
        if openai_metadata.exists():
            openai_metadata.unlink()
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=sorted(HOSTS), required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        destination = build(args.host, args.output)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Built {args.host} bundle: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
