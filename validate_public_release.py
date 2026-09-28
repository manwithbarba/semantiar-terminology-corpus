#!/usr/bin/env python3
"""Validate a SemantIAr public terminology release without modifying it."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator


MANIFEST_NAME = "RELEASE_MANIFEST.json"
IDENTITY_FIELDS = (
    "layer", "surfaceNormalized", "category", "sctid", "term", "polarity",
    "certainty", "temporality", "subject", "normalizedKey", "formType", "senseId",
    "expansion", "correctedForm", "function", "section", "mappingStatus", "inferenceScore",
)
DENIED_KEYS = {
    "clinicaltext", "textoclinico", "caseid", "blindrecordid", "annotatorid",
    "annotator", "anotador", "sourcepair", "patientid", "pacienteid", "dni",
    "email", "phone", "telephone", "telefono", "adjudicationrationale",
    "fundamentoadjudicacion",
}


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationFailure(f"Invalid JSON in {path.name}: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except Exception as exc:
            raise ValidationFailure(f"Invalid JSON in {path.name}:{line_number}: {exc}") from exc
        require(isinstance(value, dict), f"Expected object in {path.name}:{line_number}")
        rows.append(value)
    return rows


def identity(row: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(row.get(field) for field in IDENTITY_FIELDS)


def expected_term_id(row: dict[str, Any]) -> str:
    raw = json.dumps(identity(row), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def walk_keys(value: Any, location: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), f"{location}.{key}"
            yield from walk_keys(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_keys(child, f"{location}[{index}]")


def validate_schema_rows(filename: str, rows: list[dict[str, Any]], schema: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(schema)
    require(schema.get("additionalProperties") is False, f"{filename} schema must reject extra properties")
    validator = Draft202012Validator(schema)
    for index, row in enumerate(rows, start=1):
        errors = sorted(validator.iter_errors(row), key=lambda error: list(error.absolute_path))
        if errors:
            error = errors[0]
            json_path = "$" + "".join(f"[{part!r}]" for part in error.absolute_path)
            raise ValidationFailure(f"Schema error in {filename}:{index} at {json_path}: {error.message}")
        for key, location in walk_keys(row):
            if normalize_key(key) in DENIED_KEYS:
                raise ValidationFailure(f"Sensitive field {key!r} found in {filename}:{index} at {location}")


def duplicate_metrics(rows: list[dict[str, Any]]) -> tuple[int, int, int]:
    canonical = Counter(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for row in rows
    )
    groups = [count for count in canonical.values() if count > 1]
    return sum(count - 1 for count in groups), sum(groups), len(groups)


def validate(release: Path) -> dict[str, Any]:
    require(release.is_dir(), f"Release directory not found: {release}")
    manifest = load_json(release / MANIFEST_NAME)
    files = manifest.get("files")
    require(isinstance(files, list) and all(isinstance(name, str) for name in files), "manifest.files must be a string array")
    require(len(files) == len(set(files)), "manifest.files contains duplicates")
    require(MANIFEST_NAME in files, f"{MANIFEST_NAME} must inventory itself")

    allowlist = [
        line.strip()
        for line in (release / "PUBLIC_RELEASE_ALLOWLIST.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(allowlist == files, "Allowlist and manifest.files differ or have a different order")
    actual_files = sorted(path.name for path in release.iterdir() if path.is_file())
    require(actual_files == sorted(files), "Release folder differs from allowlist/manifest inventory")

    expected_hash_targets = set(files) - {MANIFEST_NAME}
    declared_hashes = manifest.get("sha256")
    require(isinstance(declared_hashes, dict), "manifest.sha256 must be an object")
    require(set(declared_hashes) == expected_hash_targets, "manifest.sha256 must cover every file except itself")
    for name in sorted(expected_hash_targets):
        require(sha256(release / name) == declared_hashes[name], f"SHA-256 mismatch for {name}")
    require(manifest.get("integrityPolicy", {}).get("manifestSelfHashExcluded") is True, "Manifest self-hash policy is not explicit")

    documentation = manifest.get("documentation", {}).get("validatedReadme", {})
    require(documentation.get("file") == "README_ORIGINAL.md", "Validated README provenance is missing")
    readme_hash = sha256(release / "README_ORIGINAL.md")
    require(documentation.get("sha256") == readme_hash, "Validated README provenance hash is stale")

    schema_bundle = load_json(release / "SCHEMA_MAPPING.json")
    terms = load_jsonl(release / "terminology_mapping.jsonl")
    occurrences = load_jsonl(release / "terminology_occurrences.jsonl")
    validate_schema_rows("terminology_mapping.jsonl", terms, schema_bundle["terms"])
    validate_schema_rows("terminology_occurrences.jsonl", occurrences, schema_bundle["occurrences"])

    term_ids = [row["termId"] for row in terms]
    require(len(term_ids) == len(set(term_ids)), "termId values are not unique")
    for index, row in enumerate(terms, start=1):
        require(row["termId"] == expected_term_id(row), f"termId mismatch in terminology_mapping.jsonl:{index}")

    occurrence_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in occurrences:
        occurrence_groups[identity(row)].append(row)
    require(set(occurrence_groups) == {identity(row) for row in terms}, "Term identities do not match occurrence identities")
    for row in terms:
        group = occurrence_groups[identity(row)]
        agreement = sum(item["evidence"] == "agreement" for item in group)
        adjudicated = sum(item["evidence"] == "adjudicated_disagreement" for item in group)
        require(row["occurrenceCount"] == len(group), f"occurrenceCount mismatch for {row['termId']}")
        require(row["agreementOccurrences"] == agreement, f"agreementOccurrences mismatch for {row['termId']}")
        require(row["adjudicatedOccurrences"] == adjudicated, f"adjudicatedOccurrences mismatch for {row['termId']}")
        require(row["noteTypes"] == sorted({item["noteType"] for item in group if item.get("noteType")}), f"noteTypes mismatch for {row['termId']}")
        require(row["specialties"] == sorted({item["specialty"] for item in group if item.get("specialty")}), f"specialties mismatch for {row['termId']}")

    exclusions = load_json(release / "EXCLUSIONS.json")
    counts = manifest.get("counts", {})
    duplicate_excess, duplicate_rows, duplicate_groups = duplicate_metrics(occurrences)
    calculated = {
        "publishedOccurrences": len(occurrences),
        "publishedTerms": len(terms),
        "humanDecisionOccurrences": sum(row["mappingStatus"].startswith("human_") for row in occurrences),
        "faissCandidateOccurrences": sum(row["mappingStatus"].startswith("faiss_") for row in occurrences),
        "faissAtOrAboveThresholdOccurrences": sum(row["mappingStatus"] == "faiss_candidate" for row in occurrences),
        "faissBelowThresholdOccurrences": sum(row["mappingStatus"] == "faiss_candidate_below_threshold" for row in occurrences),
        "exactDuplicateOccurrenceExcessRows": duplicate_excess,
        "exactDuplicateOccurrenceRowsInGroups": duplicate_rows,
        "exactDuplicateOccurrenceGroups": duplicate_groups,
    }
    for key, value in calculated.items():
        require(counts.get(key) == value, f"Manifest count mismatch for {key}: expected {value}, found {counts.get(key)}")
    require(counts.get("inputOccurrences") == counts.get("publishedOccurrences") + counts.get("excludedOccurrences"), "Counts do not balance")
    for key in ("inputOccurrences", "publishedOccurrences", "excludedOccurrences"):
        require(exclusions.get(key) == counts.get(key), f"EXCLUSIONS.json differs for {key}")
    require(sum(row["occurrenceCount"] for row in terms) == len(occurrences), "Aggregation does not sum to occurrences")

    return {
        "release": str(release), "files": len(files), "terms": len(terms),
        "occurrences": len(occurrences), "excluded": counts["excludedOccurrences"],
        "human": calculated["humanDecisionOccurrences"], "faiss": calculated["faissCandidateOccurrences"],
        "faissBelowThreshold": calculated["faissBelowThresholdOccurrences"],
        "exactDuplicateExcessRows": duplicate_excess, "validatedReadmeSha256": readme_hash,
    }


def main() -> int:
    release = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
    try:
        summary = validate(release)
    except ValidationFailure as exc:
        print(f"INVALID RELEASE: {exc}", file=sys.stderr)
        return 1
    print("VALID RELEASE")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
