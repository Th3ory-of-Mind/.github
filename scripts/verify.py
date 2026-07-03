"""Fast, deterministic validation for organization governance files."""

from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
REQUIRED = (
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "GOVERNANCE.md",
    "CODEOWNERS",
    ".github/pull_request_template.md",
)
FORMS = (
    "bug.yml",
    "contract-change.yml",
    "skill-submission.yml",
    "security-design.yml",
    "architecture-decision.yml",
)


def main() -> int:
    errors: list[str] = []
    for relative_path in REQUIRED:
        path = ROOT / relative_path
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            errors.append(f"missing or empty: {relative_path}")

    template_root = ROOT / ".github" / "ISSUE_TEMPLATE"
    config = yaml.safe_load((template_root / "config.yml").read_text(encoding="utf-8"))
    if config.get("blank_issues_enabled") is not False:
        errors.append("blank issues must be disabled")

    for filename in FORMS:
        form = yaml.safe_load((template_root / filename).read_text(encoding="utf-8"))
        missing = {"name", "description", "title", "labels", "body"} - form.keys()
        if missing:
            errors.append(f"{filename}: missing {', '.join(sorted(missing))}")

    if (ROOT / "CODEOWNERS").read_text(encoding="utf-8").splitlines()[0] != (
        "* @Alt3r3dP3rc3ption"
    ):
        errors.append("CODEOWNERS must use the conservative default owner")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(f"Validated {len(REQUIRED)} community files and {len(FORMS)} issue forms.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
