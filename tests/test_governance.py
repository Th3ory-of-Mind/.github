from pathlib import Path
import subprocess
import sys

import yaml


ROOT = Path(__file__).parents[1]
POLICIES = {
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORT.md",
    "GOVERNANCE.md",
}
FORMS = {
    "bug.yml",
    "contract-change.yml",
    "skill-submission.yml",
    "security-design.yml",
    "architecture-decision.yml",
}


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_required_community_files_exist_and_have_no_placeholders() -> None:
    for filename in POLICIES:
        content = read(filename)
        assert len(content.splitlines()) >= 8
        lowered = content.lower()
        assert "todo" not in lowered
        assert "tbd" not in lowered
        assert "example.com" not in lowered


def test_security_policy_uses_private_advisories_and_prohibits_sensitive_data() -> None:
    content = read("SECURITY.md")
    assert "Security Advisories" in content
    assert "https://github.com/Th3ory-of-Mind/.github/security/advisories/new" in content
    assert "do not include secrets" in content.lower()
    assert "production data" in content.lower()
    assert "@" not in content


def test_governance_defines_contract_gates_and_human_authority() -> None:
    content = read("GOVERNANCE.md").lower()
    for phrase in (
        "migration plan",
        "architecture decision record",
        "human",
        "sign",
    ):
        assert phrase in content


def test_pull_request_template_covers_review_evidence() -> None:
    content = read(".github/pull_request_template.md").lower()
    for heading in (
        "summary",
        "contract impact",
        "security impact",
        "provenance",
        "tests",
        "migration",
        "rollback",
        "checklist",
    ):
        assert f"## {heading}" in content


def test_codeowners_has_conservative_default() -> None:
    assert read("CODEOWNERS").strip().splitlines()[0] == "* @Alt3r3dP3rc3ption"


def test_issue_template_configuration_disables_blank_issues() -> None:
    config = yaml.safe_load(read(".github/ISSUE_TEMPLATE/config.yml"))
    assert config["blank_issues_enabled"] is False


def test_issue_forms_are_valid_and_require_structured_input() -> None:
    for filename in FORMS:
        form = yaml.safe_load(read(f".github/ISSUE_TEMPLATE/{filename}"))
        assert form["name"]
        assert form["description"]
        assert form["title"]
        assert isinstance(form["labels"], list)
        assert form["body"]
        required_inputs = [
            item
            for item in form["body"]
            if item.get("type") in {"input", "textarea", "dropdown", "checkboxes"}
            and item.get("validations", {}).get("required") is True
        ]
        assert required_inputs
        rendered = read(f".github/ISSUE_TEMPLATE/{filename}").lower()
        assert "secret" in rendered
        assert "production data" in rendered


def test_vulnerability_intake_routes_to_security_policy() -> None:
    content = read(".github/ISSUE_TEMPLATE/security-design.yml").lower()
    assert "security.md" in content
    assert "vulnerabilit" in content
    assert "@" not in content


def test_readme_links_only_to_current_public_organization_repository() -> None:
    content = read("README.md")
    github_links = [
        token.rstrip(").,")
        for token in content.split()
        if token.startswith("https://github.com/Th3ory-of-Mind/")
    ]
    assert github_links
    assert set(github_links) == {"https://github.com/Th3ory-of-Mind/.github"}
    assert "Ingestion foundation | Merged" in content
    assert "Registry milestone | In progress" in content


def test_verifier_entrypoint_completes_successfully() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/verify.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
