"""Tests for evidence manifest validation."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from codyssey_c1_3.evidence import validate_manifest  # noqa: E402


class EvidenceValidationTests(unittest.TestCase):
    """Verify manifest consistency rules."""

    def test_repository_manifest_is_consistent(self) -> None:
        self.assertEqual(validate_manifest(REPO_ROOT), [])

    def test_missing_manifest_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            findings = validate_manifest(Path(directory))
        self.assertEqual(findings[0].requirement_id, "manifest")


if __name__ == "__main__":
    unittest.main()
