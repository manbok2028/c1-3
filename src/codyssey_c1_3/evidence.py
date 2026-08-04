"""Validate the mission evidence manifest."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


ALLOWED_STATUSES = {"complete", "pending"}


@dataclass(frozen=True)
class ValidationResult:
    """A single manifest validation finding."""

    requirement_id: str
    message: str


def load_manifest(path: Path) -> dict[str, object]:
    """Load a TOML evidence manifest."""

    with path.open("rb") as manifest_file:
        return tomllib.load(manifest_file)


def validate_manifest(repo_root: Path) -> list[ValidationResult]:
    """Return all consistency and missing-file findings."""

    manifest_path = repo_root / "evidence" / "manifest.toml"
    if not manifest_path.is_file():
        return [ValidationResult("manifest", "evidence/manifest.toml is missing")]

    manifest = load_manifest(manifest_path)
    requirements = manifest.get("requirements")
    if not isinstance(requirements, list):
        return [ValidationResult("manifest", "requirements must be an array")]

    findings: list[ValidationResult] = []
    seen_ids: set[str] = set()

    for item in requirements:
        if not isinstance(item, dict):
            findings.append(ValidationResult("manifest", "requirement must be a table"))
            continue

        requirement_id = str(item.get("id", "")).strip()
        status = str(item.get("status", "")).strip()
        files = item.get("files", [])

        if not requirement_id:
            findings.append(ValidationResult("manifest", "requirement id is empty"))
            continue
        if requirement_id in seen_ids:
            findings.append(ValidationResult(requirement_id, "duplicate requirement id"))
        seen_ids.add(requirement_id)

        if status not in ALLOWED_STATUSES:
            findings.append(ValidationResult(requirement_id, f"invalid status: {status}"))
        if not isinstance(files, list) or not all(isinstance(value, str) for value in files):
            findings.append(ValidationResult(requirement_id, "files must be a string array"))
            continue
        if status == "complete" and not files:
            findings.append(ValidationResult(requirement_id, "complete item has no evidence"))

        for relative_path in files:
            evidence_path = repo_root / relative_path
            if not evidence_path.is_file():
                findings.append(ValidationResult(requirement_id, f"missing: {relative_path}"))
            elif evidence_path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".pdf", ".md"}:
                findings.append(ValidationResult(requirement_id, f"unsupported evidence: {relative_path}"))

    return findings
