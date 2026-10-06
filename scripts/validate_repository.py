#!/usr/bin/env python3
"""Validate the final public Fire-Plume Review evidence repository."""

from __future__ import annotations

import csv
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]

UNKNOWN_COMPLETENESS_TOKENS = {
    "Not fully coded / not reported",
    "Not recorded",
    "Unknown",
    "Not reported",
}
NOT_APPLICABLE_COMPLETENESS_TOKENS = {"N/A", "Not applicable"}
AMBIGUOUS_COMPLETENESS_TOKENS = {"Not applicable / not recorded"}

FINAL_FIGURE_SOURCES = {
    "figures/source/pipeline_overview.tex",
    "figures/source/prisma_flow.tex",
    "figures/source/risks_section_map.tex",
    "figures/source/risks_requirements.tex",
    "figures/source/autonomous_section_map.tex",
    "figures/source/monitoring_coverage.tex",
    "figures/source/forecasting_section_map.tex",
    "figures/source/forecasting_taxonomy.tex",
    "figures/source/technical_requirements.tex",
    "figures/source/technical_coverage.tex",
    "figures/source/health_section_map.tex",
    "figures/source/health_pipeline.tex",
    "figures/source/health_requirements.tex",
    "figures/source/health_coverage.tex",
    "figures/source/governance_section_map.tex",
    "figures/source/governance_requirements.tex",
    "figures/source/governance_coverage.tex",
    "figures/source/cross_pipeline_synthesis.tex",
    "figures/source/cross_pipeline_coverage.tex",
}
TABLE_SOURCES = {"figures/source/platform_sensor_matrix.tex"}
SOURCE_FILES = FINAL_FIGURE_SOURCES | TABLE_SOURCES

EXPECTED_FILES = {
    ".gitignore",
    "README.md",
    "METHODS.md",
    "LICENSE.md",
    "methods/search_log.csv",
    "methods/source_linkage_reconciliation.csv",
    "methods/residual_duplicate_audit.csv",
    "data/title_abstract_screening.csv",
    "data/full_text_decisions.csv",
    "data/included_studies.csv",
    "data/coding_completeness.csv",
    "data/included_studies.bib",
    "data/prisma_counts.csv",
    "data/codebook.csv",
    "data/manuscript_source_scope.csv",
    "synthesis/closest_reviews.csv",
    "synthesis/evidence_coverage_matrices.csv",
    "synthesis/matrix_supporting_sources.csv",
    "figures/figure_provenance.csv",
    "scripts/validate_repository.py",
} | SOURCE_FILES

EXPECTED_ROWS = {
    "methods/search_log.csv": 36,
    "methods/source_linkage_reconciliation.csv": 7,
    "methods/residual_duplicate_audit.csv": 51,
    "data/title_abstract_screening.csv": 27239,
    "data/full_text_decisions.csv": 713,
    "data/included_studies.csv": 562,
    "data/coding_completeness.csv": 26,
    "data/prisma_counts.csv": 10,
    "data/manuscript_source_scope.csv": 105,
    "synthesis/closest_reviews.csv": 6,
    "synthesis/evidence_coverage_matrices.csv": 140,
    "synthesis/matrix_supporting_sources.csv": 25,
    "figures/figure_provenance.csv": 29,
}

FORBIDDEN_SUFFIXES = {".pdf", ".ris", ".nbib", ".enw", ".xlsx", ".xls"}
ALLOWED_BIB_FILES = {"data/included_studies.bib"}
FORBIDDEN_TEXT = [
    re.compile(r"/" + "workspace" + r"/", re.I),
    re.compile(r"/" + "home" + r"/", re.I),
    re.compile(r"[A-Z]:\\Users\\", re.I),
]
ALLOWED_MATURITY = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "N/A",
    "Not fully coded / not reported",
}
ALLOWED_COVERAGE_CODES = {"D", "P", "N", "NA"}
ALLOWED_ROLE_PARENTS = {
    "Direct fire-specific evidence",
    "Fire-specific interface or background evidence",
    "Evidence synthesis or guidance",
    "Transferred adjacent-domain evidence",
}
ALLOWED_SCOPE_RELATIONS = {
    "Primary included corpus",
    "Contextual outside primary corpus",
    "Full-text excluded; contextual citation only",
    "External review-method guidance",
    "External technical background",
    "External adjacent-review positioning",
    "External fire-specific context",
    "External legal authority",
    "External regulatory guidance",
    "External governance or public-health guidance",
}


def read_csv(rel: str) -> tuple[list[str], list[dict[str, str]]]:
    with (ROOT / rel).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalise_doi(value: str) -> str:
    return re.sub(
        r"^(https?://(dx\.)?doi\.org/|doi:\s*)",
        "",
        (value or "").strip().lower(),
    )


def table_body(tex: str) -> str:
    if "\\midrule" not in tex or "\\bottomrule" not in tex:
        return tex
    return tex.split("\\midrule", 1)[1].split("\\bottomrule", 1)[0]


errors: list[str] = []
actual_files = {
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*")
    if path.is_file() and ".git" not in path.relative_to(ROOT).parts
}
missing = sorted(EXPECTED_FILES - actual_files)
unexpected = sorted(actual_files - EXPECTED_FILES)
if missing:
    errors.append(f"missing required files: {missing}")
if unexpected:
    errors.append(f"unexpected public files: {unexpected}")

for rel, expected in EXPECTED_ROWS.items():
    if not (ROOT / rel).exists():
        continue
    _, rows = read_csv(rel)
    if len(rows) != expected:
        errors.append(f"row count {rel}: {len(rows)} != {expected}")

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.relative_to(ROOT).parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        errors.append(f"forbidden public file type: {path.relative_to(ROOT)}")
    if path.suffix.lower() == ".bib" and rel not in ALLOWED_BIB_FILES:
        errors.append(f"unexpected public bibliography: {path.relative_to(ROOT)}")
    if path.suffix.lower() in {".md", ".csv", ".py", ".bib", ".tex"}:
        if rel == "scripts/validate_repository.py":
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for pattern in FORBIDDEN_TEXT:
            if pattern.search(text):
                errors.append(f"release/local-path pattern in {rel}: {pattern.pattern}")

# Exact final editable-source package: 19 manuscript figures plus one compact table.
actual_sources = {
    p.relative_to(ROOT).as_posix()
    for p in (ROOT / "figures" / "source").glob("*.tex")
}
if actual_sources != SOURCE_FILES:
    errors.append(
        "editable source set differs from the frozen package: "
        f"missing={sorted(SOURCE_FILES - actual_sources)}, "
        f"extra={sorted(actual_sources - SOURCE_FILES)}"
    )

ta_fields, ta_rows = read_csv("data/title_abstract_screening.csv")
ft_fields, ft_rows = read_csv("data/full_text_decisions.csv")
included_fields, included_rows = read_csv("data/included_studies.csv")
_, prisma_rows = read_csv("data/prisma_counts.csv")
_, codebook_rows = read_csv("data/codebook.csv")
_, closest_rows = read_csv("synthesis/closest_reviews.csv")
_, coverage_rows = read_csv("synthesis/evidence_coverage_matrices.csv")
_, matrix_support_rows = read_csv("synthesis/matrix_supporting_sources.csv")
_, coding_completeness_rows = read_csv("data/coding_completeness.csv")
_, provenance_rows = read_csv("figures/figure_provenance.csv")
_, linkage_rows = read_csv("methods/source_linkage_reconciliation.csv")
_, duplicate_audit_rows = read_csv("methods/residual_duplicate_audit.csv")
_, scope_rows = read_csv("data/manuscript_source_scope.csv")

ta_ids = [row["Record_ID"] for row in ta_rows]
ft_ids = [row["Record_ID"] for row in ft_rows]
included_ids = [row["Record_ID"] for row in included_rows]
for label, ids in (("title/abstract", ta_ids), ("full-text", ft_ids), ("included", included_ids)):
    if len(ids) != len(set(ids)):
        errors.append(f"duplicate Record_ID values in {label} register")
if not set(ft_ids).issubset(set(ta_ids)):
    errors.append("some full-text records are absent from the title/abstract register")

if any(not row.get("Title", "").strip() for row in ta_rows):
    errors.append("blank title in title/abstract register")
if any(not row.get("Year", "").strip() for row in ta_rows):
    errors.append("blank year in title/abstract register")
normalised_dois = [
    normalise_doi(row.get("DOI", ""))
    for row in ta_rows
    if row.get("DOI", "").strip()
]
if len(normalised_dois) != len(set(normalised_dois)):
    errors.append("duplicate nonblank DOI in title/abstract register")
if sum(int(row.get("Reports_Merged", "0") or 0) for row in ta_rows) != 64922:
    errors.append("title/abstract source-linkage total is not 64,922")

# Workflow labels must state what actually received author review. No public
# record may remain in a placeholder state that implies an unfinished mass task.
placeholder_status = re.compile(r"^(pending|not yet sampled)", re.I)
for row in ta_rows:
    status = row.get("Human_Verification", "").strip()
    if not status or placeholder_status.search(status):
        errors.append(
            f"unfinished or blank title/abstract verification status for {row['Record_ID']}: {status!r}"
        )
for row in ta_rows:
    rid = row["Record_ID"]
    if rid in set(ft_ids) and "Author-approved downstream" not in row.get("Human_Verification", ""):
        errors.append(f"sought record lacks downstream author-approved status: {rid}")
    if row["TA_Decision"] == "Exclude" and rid not in set(ft_ids) and row.get("Human_Verification") != "Rule-assisted exclusion; not individually author-verified":
        errors.append(f"title/abstract exclusion has misleading verification label: {rid}")

# The 72,593 per-query/source-registry inputs must reconcile explicitly to the
# 64,922 linkages entering cross-source reconciliation.
linkage_by_source = {row["Source"]: row for row in linkage_rows}
total_linkage = linkage_by_source.get("TOTAL", {})
if int(total_linkage.get("Per_Query_Result_Total", 0)) != 72593:
    errors.append("source-linkage input total is not 72,593")
if int(total_linkage.get("Linkages_Entering_Cross_Source_Reconciliation", 0)) != 64922:
    errors.append("source-linkage reconciliation output is not 64,922")
if int(total_linkage.get("Within_Source_Overlap_Removed", 0)) != 7671:
    errors.append("within-source overlap total is not 7,671")
detail_linkages = [row for row in linkage_rows if row["Source"] != "TOTAL"]
for field in (
    "Per_Query_Result_Total",
    "Linkages_Entering_Cross_Source_Reconciliation",
    "Within_Source_Overlap_Removed",
):
    if sum(int(row[field]) for row in detail_linkages) != int(total_linkage.get(field, -1)):
        errors.append(f"source-linkage detail does not sum to TOTAL for {field}")

# Every residual normalised-title collision was adjudicated; eight publication
# manifestations were merged and the 43 remaining collision groups retained.
def normalise_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()

title_groups: dict[str, list[str]] = defaultdict(list)
for row in ta_rows:
    title_groups[normalise_title(row["Title"])].append(row["Record_ID"])
remaining_collisions = {title: ids for title, ids in title_groups.items() if title and len(ids) > 1}
retained_audits = {
    row["Normalised_Title"]: row
    for row in duplicate_audit_rows
    if row["Decision"] == "Retain distinct records"
}
merge_audits = [
    row for row in duplicate_audit_rows
    if row["Decision"] == "Merge confirmed duplicate manifestation"
]
if len(remaining_collisions) != 43:
    errors.append(f"remaining normalised-title collision groups: {len(remaining_collisions)} != 43")
if set(remaining_collisions) != set(retained_audits):
    errors.append("retained normalised-title collisions do not exactly match the adjudication ledger")
if len(merge_audits) != 8:
    errors.append(f"merged duplicate groups: {len(merge_audits)} != 8")
for row in merge_audits:
    canonical = row["Canonical_Record_ID"]
    removed = [part.strip() for part in row["Removed_Record_IDs"].split(";") if part.strip()]
    if canonical not in set(ta_ids):
        errors.append(f"duplicate-audit canonical ID missing from register: {canonical}")
    if set(removed) & set(ta_ids):
        errors.append(f"duplicate-audit removed ID remains in register: {removed}")

decisions = Counter(row["FT_Decision"] for row in ft_rows)
expected_decisions = Counter({"Include": 562, "Exclude": 60, "Not retrieved": 91})
if decisions != expected_decisions:
    errors.append(f"full-text decisions {dict(decisions)} != {dict(expected_decisions)}")
if set(included_ids) != {
    row["Record_ID"] for row in ft_rows if row["FT_Decision"] == "Include"
}:
    errors.append("included-study IDs do not exactly match full-text include decisions")

# Final author-approved decisions must expose a final public status, while
# detailed charting verification remains a separate audit field.
working_rationale = re.compile(
    r"need to decide|currently excluded|may qualify|inconsistent with", re.I
)
for row in ft_rows:
    rid = row.get("Record_ID", "<unknown>")
    if row.get("Author_Decision") == "Approve":
        decision = row.get("FT_Decision", "")
        status = row.get("Current_Inclusion_Status", "")
        expected_status = {
            "Include": "Include",
            "Exclude": "Exclude",
            "Not retrieved": "Not retrieved — inaccessible after documented attempts",
        }.get(decision)
        if expected_status and status != expected_status:
            errors.append(
                f"stale final inclusion status for {rid}: {status!r} != {expected_status!r}"
            )
    if working_rationale.search(row.get("Decision_Rationale", "")):
        errors.append(f"working-language residue in final rationale for {rid}")
    expected_charting_status = {
        "Include": "Eligibility author-approved; detailed coding not independently author-verified; see data/coding_completeness.csv",
        "Exclude": "Not applicable — excluded report",
        "Not retrieved": "Not applicable — report unavailable",
    }.get(row.get("FT_Decision", ""))
    if expected_charting_status and row.get("Author_Charting_Verification") != expected_charting_status:
        errors.append(
            f"stale detailed-charting status for {rid}: "
            f"{row.get('Author_Charting_Verification')!r} != {expected_charting_status!r}"
        )
    for field, value in row.items():
        if re.search(r"&(?:amp|mdash|ndash|quot|apos|lt|gt);", value or "", re.I):
            errors.append(f"HTML entity in full-text metadata for {rid} field {field}")

counts = {row["Measure"]: int(row["Count"]) for row in prisma_rows}
expected_counts = {
    "Formal source linkages": 64922,
    "Duplicate/source-overlap linkages removed": 37683,
    "Unique records screened": 27239,
    "Title/abstract exclusions": 26129,
    "Contextual outside primary corpus": 397,
    "Reports sought": 713,
    "Reports assessed": 622,
    "Primary inclusions": 562,
    "Full-text exclusions": 60,
    "Reports not retrieved": 91,
}
if counts != expected_counts:
    errors.append(f"PRISMA counts differ from the frozen values: {counts}")
if counts.get("Formal source linkages", 0) - counts.get(
    "Duplicate/source-overlap linkages removed", 0
) != counts.get("Unique records screened", -1):
    errors.append("PRISMA identity failed: source linkages")
if counts.get("Unique records screened", 0) != (
    counts.get("Title/abstract exclusions", 0)
    + counts.get("Contextual outside primary corpus", 0)
    + counts.get("Reports sought", 0)
):
    errors.append("PRISMA identity failed: screened records")
if counts.get("Reports sought", 0) != counts.get("Reports assessed", 0) + counts.get(
    "Reports not retrieved", 0
):
    errors.append("PRISMA identity failed: reports sought")
if counts.get("Reports assessed", 0) != counts.get("Primary inclusions", 0) + counts.get(
    "Full-text exclusions", 0
):
    errors.append("PRISMA identity failed: reports assessed")

# Editable PRISMA source must reproduce the authoritative CSV counts.
prisma_tex = (ROOT / "figures/source/prisma_flow.tex").read_text(
    encoding="utf-8", errors="replace"
)
for measure, expected in {
    "Formal source linkages": counts.get("Formal source linkages"),
    "Duplicate/source-overlap linkages removed": counts.get(
        "Duplicate/source-overlap linkages removed"
    ),
    "Unique records screened": counts.get("Unique records screened"),
    "Title/abstract exclusions": counts.get("Title/abstract exclusions"),
    "Contextual outside primary corpus": counts.get("Contextual outside primary corpus"),
    "Reports sought": counts.get("Reports sought"),
    "Reports not retrieved": counts.get("Reports not retrieved"),
    "Reports assessed": counts.get("Reports assessed"),
    "Full-text exclusions": counts.get("Full-text exclusions"),
    "Primary inclusions": counts.get("Primary inclusions"),
}.items():
    if expected is not None and f"{expected:,}" not in prisma_tex:
        errors.append(
            f"PRISMA figure source does not contain final count for {measure}: {expected:,}"
        )

# Included-study row-level consistency.
for row in included_rows:
    rid = row.get("Record_ID", "<unknown>")
    maturity = row.get("Deployment_Maturity_Register_Value", "").strip()
    if maturity and maturity not in ALLOWED_MATURITY:
        errors.append(f"invalid deployment maturity for {rid}: {maturity!r}")
    role_parent = row.get("Evidence_Role_Parent", "").strip()
    if role_parent not in ALLOWED_ROLE_PARENTS:
        errors.append(f"invalid parent evidence role for {rid}: {role_parent!r}")
    specificity = row.get("Fire_Specificity", "").strip().lower()
    if specificity == "not included in primary corpus":
        errors.append(f"included record {rid} is labelled 'Not included in primary corpus'")
    doi_url = row.get("DOI_URL", "").strip()
    if doi_url and not re.fullmatch(r"https://doi\.org/\S+", doi_url, flags=re.I):
        errors.append(f"malformed DOI_URL for {rid}: {doi_url[:80]!r}")
    doi = row.get("DOI", "")
    if doi and any(ord(char) > 127 for char in doi):
        errors.append(f"non-ASCII character in DOI for {rid}: {doi!r}")
    unresolved = re.compile(r"verify subtype|extract exact|full uq coding pending", re.I)
    for field, value in row.items():
        lowered = (value or "").lower()
        if "@article{" in lowered or "@inproceedings{" in lowered:
            errors.append(f"embedded BibTeX detected in {rid} field {field}")
        if unresolved.search(value or ""):
            errors.append(f"unfinished coding token in {rid} field {field}: {(value or '')[:100]!r}")
        if re.search(r"&(?:amp|mdash|ndash|quot|apos|lt|gt);", value or "", re.I):
            errors.append(f"HTML entity in included-study metadata for {rid} field {field}")

    setting_text = " ".join(
        [
            row.get("Evidence_Setting", ""),
            row.get("Field_vs_Simulation", ""),
            row.get("Evidence_Role_Register", ""),
        ]
    ).lower()
    if ("review/synthesis" in setting_text or "evidence synthesis" in setting_text or "guidance" in setting_text) and maturity not in {"N/A", "Not fully coded / not reported"}:
        errors.append(f"evidence-synthesis maturity is not N/A for {rid}: {maturity!r}")
    if maturity == "0" and "simulation/computational" in row.get("Field_vs_Simulation", "").lower():
        errors.append(f"conceptual maturity conflicts with simulation/computational setting for {rid}")
    design_lower = row.get("Evaluation_Design", "").lower()
    field_lower = row.get("Field_vs_Simulation", "").lower().strip()
    setting_lower = row.get("Evidence_Setting", "").lower().strip()
    if maturity == "0" and (
        re.search(r"controlled field|controlled laboratory|case-study retrospective|identical-twin", design_lower)
        or field_lower in {"simulation only", "field observational", "field qualitative study", "field/observational"}
    ):
        errors.append(f"conceptual maturity conflicts with explicit evaluated evidence for {rid}")
    if maturity == "1" and field_lower in {"field observational", "field qualitative study", "field/observational"}:
        errors.append(f"offline/simulation maturity conflicts with explicit field-observational evidence for {rid}")
    if maturity == "3" and setting_lower == "retrospective observational study":
        errors.append(f"pilot/workflow maturity conflicts with retrospective observational setting for {rid}")
    if maturity == "0" and "conceptual" not in setting_lower and "conceptual" not in field_lower:
        errors.append(f"maturity 0 lacks an explicit conceptual setting for {rid}")

# Every DOI_URL should agree with DOI when both are present.
for row in included_rows:
    rid = row.get("Record_ID", "<unknown>")
    doi = normalise_doi(row.get("DOI", ""))
    doi_url = row.get("DOI_URL", "").strip()
    if doi and doi_url and doi_url.lower() != f"https://doi.org/{doi}".lower():
        errors.append(f"DOI/DOI_URL mismatch for {rid}")

defined_fields = {row["Field"] for row in codebook_rows}
missing_definitions = sorted(set(included_fields) - defined_fields)
if missing_definitions:
    errors.append(f"included-study fields missing from codebook: {missing_definitions}")

unexpected_coverage = {row["Code"] for row in coverage_rows} - ALLOWED_COVERAGE_CODES
if unexpected_coverage:
    errors.append(f"unexpected evidence-coverage codes: {sorted(unexpected_coverage)}")

# The compact completeness audit must cover every included-study column and
# be derived exactly from the 562-row register rather than merely adding up.
if {row.get("Field", "") for row in coding_completeness_rows} != set(included_fields):
    errors.append("coding-completeness fields do not exactly match included-study columns")
expected_completeness_header = {
    "Field",
    "Total_Rows",
    "Blank",
    "Explicit_Unknown_or_Not_Reported",
    "Not_Applicable",
    "Usable_Value",
    "Usable_or_NA",
    "Usable_or_NA_Proportion",
    "Interpretation",
}
actual_completeness_header = set(read_csv("data/coding_completeness.csv")[0])
if actual_completeness_header != expected_completeness_header:
    errors.append("coding-completeness header differs from the frozen schema")
for row in coding_completeness_rows:
    field = row.get("Field", "<unknown>")
    try:
        total = int(row["Total_Rows"])
        blank = int(row["Blank"])
        unknown = int(row["Explicit_Unknown_or_Not_Reported"])
        not_applicable = int(row["Not_Applicable"])
        usable = int(row["Usable_Value"])
        usable_or_na = int(row["Usable_or_NA"])
        proportion = float(row["Usable_or_NA_Proportion"])
    except (KeyError, ValueError):
        errors.append(f"non-integer coding-completeness counts for {field}")
        continue
    values = [included_row.get(field, "").strip() for included_row in included_rows]
    ambiguous = [value for value in values if value in AMBIGUOUS_COMPLETENESS_TOKENS]
    if ambiguous:
        errors.append(f"ambiguous missing-value token in included-study field {field}")
    expected_blank = sum(value == "" for value in values)
    expected_unknown = sum(value in UNKNOWN_COMPLETENESS_TOKENS for value in values)
    expected_na = sum(value in NOT_APPLICABLE_COMPLETENESS_TOKENS for value in values)
    expected_usable = len(values) - expected_blank - expected_unknown - expected_na
    expected_usable_or_na = expected_usable + expected_na
    expected_proportion = expected_usable_or_na / len(values)
    reported = (total, blank, unknown, not_applicable, usable, usable_or_na)
    expected = (
        len(values),
        expected_blank,
        expected_unknown,
        expected_na,
        expected_usable,
        expected_usable_or_na,
    )
    if reported != expected:
        errors.append(
            f"coding-completeness source mismatch for {field}: "
            f"reported={reported}, expected={expected}"
        )
    if abs(proportion - expected_proportion) > 1e-12:
        errors.append(
            f"coding-completeness proportion mismatch for {field}: "
            f"reported={proportion}, expected={expected_proportion}"
        )

# One normalised support row covers each distinct matrix/function row. Record
# anchors must resolve to the screened register; citation anchors to the active
# manuscript-source scope ledger.
coverage_pairs = {(row["Matrix"], row["Evidence_or_function"]) for row in coverage_rows}
support_pairs = {(row["Matrix"], row["Evidence_or_function"]) for row in matrix_support_rows}
if len(support_pairs) != len(matrix_support_rows):
    errors.append("duplicate matrix/function pair in matrix supporting-sources table")
if support_pairs != coverage_pairs:
    errors.append("matrix supporting-sources rows do not exactly cover matrix/function pairs")
scope_key_set = {row.get("Citation_Key", "") for row in scope_rows}
ta_id_set = set(ta_ids)
for row in matrix_support_rows:
    pair = f"{row.get('Matrix')} / {row.get('Evidence_or_function')}"
    record_ids = [part.strip() for part in row.get("Supporting_Record_IDs", "").split(";") if part.strip()]
    citation_keys = [part.strip() for part in row.get("Supporting_Citation_Keys", "").split(";") if part.strip()]
    if not record_ids and not citation_keys:
        errors.append(f"matrix support row has no source anchors: {pair}")
    for rid in record_ids:
        if rid not in ta_id_set:
            errors.append(f"matrix support Record_ID not found: {pair} -> {rid}")
    for key in citation_keys:
        if key not in scope_key_set:
            errors.append(f"matrix support citation key not found: {pair} -> {key}")

# Every active citation in the clean manuscript has a one-row scope decision.
scope_keys = [row.get("Citation_Key", "") for row in scope_rows]
if len(scope_keys) != len(set(scope_keys)):
    errors.append("duplicate Citation_Key in manuscript source scope")
unexpected_scope_relations = {row.get("Corpus_Relation", "") for row in scope_rows} - ALLOWED_SCOPE_RELATIONS
if unexpected_scope_relations:
    errors.append(f"unexpected manuscript scope relation: {sorted(unexpected_scope_relations)}")
for row in scope_rows:
    key = row.get("Citation_Key", "<unknown>")
    if not row.get("Title", "").strip() or not row.get("Corpus_Relation", "").strip() or not row.get("Claim_Boundary", "").strip():
        errors.append(f"incomplete manuscript source-scope row: {key}")
    if row.get("Audit_Status", "").strip() != "Source-content checked":
        errors.append(f"active citation is not source-content checked: {key}")
    if not row.get("Audit_Note", "").strip():
        errors.append(f"missing active-citation audit note: {key}")
    for rid in [part.strip() for part in row.get("Record_IDs", "").split(";") if part.strip()]:
        if rid not in set(ta_ids):
            errors.append(f"manuscript source-scope Record_ID not found: {key} -> {rid}")

# Machine-readable evidence matrices must agree with the final rendered-source codes.
matrix_sources = {
    "Operational requirements": "figures/source/monitoring_coverage.tex",
    "Technical evidence": "figures/source/technical_coverage.tex",
    "Health evidence": "figures/source/health_coverage.tex",
    "Governance evidence": "figures/source/governance_coverage.tex",
    "Cross-pipeline gaps": "figures/source/cross_pipeline_coverage.tex",
}
coverage_by_matrix: dict[str, Counter[str]] = defaultdict(Counter)
for row in coverage_rows:
    coverage_by_matrix[row["Matrix"]][row["Code"]] += 1
for matrix, source in matrix_sources.items():
    body = table_body((ROOT / source).read_text(encoding="utf-8", errors="replace"))
    tex_counts = Counter(
        {
            "D": len(re.findall(r"\\covD\b", body)),
            "P": len(re.findall(r"\\covP\b", body)),
            "N": len(re.findall(r"\\covN(?!A)\b", body)),
            "NA": len(re.findall(r"\\covNA\b", body)),
        }
    )
    csv_counts = coverage_by_matrix[matrix]
    for code in ALLOWED_COVERAGE_CODES:
        if tex_counts[code] != csv_counts[code]:
            errors.append(
                f"coverage-source mismatch for {matrix} code {code}: "
                f"TeX={tex_counts[code]} CSV={csv_counts[code]}"
            )
    tex_sequence = re.findall(r"\\cov(NA|D|P|N)\b", body)
    csv_sequence = [row["Code"] for row in coverage_rows if row["Matrix"] == matrix]
    if tex_sequence != csv_sequence:
        errors.append(f"coverage-source cell order mismatch for {matrix}")

for row in closest_rows:
    record_id = row.get("Record_ID", "")
    if record_id and record_id not in set(ta_ids):
        errors.append(f"closest-review Record_ID not found: {record_id}")

# Figure provenance: 10 original/replaced/removed items plus all 19 final figures.
final_rows = [row for row in provenance_rows if row.get("Decision", "").startswith("Final Figure")]
if len(final_rows) != 19:
    errors.append(f"final figure provenance rows: {len(final_rows)} != 19")
final_locations = {row.get("Replacement_or_location", "") for row in final_rows}
if final_locations != FINAL_FIGURE_SOURCES:
    errors.append(
        "final figure provenance/source mismatch: "
        f"missing={sorted(FINAL_FIGURE_SOURCES - final_locations)}, "
        f"extra={sorted(final_locations - FINAL_FIGURE_SOURCES)}"
    )
if any(row.get("Rights_status", "") != "Original source" for row in final_rows):
    errors.append("one or more final figures are not marked as original source")

# Complete included-study bibliography: one stable entry per included Record_ID.
bib_path = ROOT / "data/included_studies.bib"
if bib_path.exists():
    bib_text = bib_path.read_text(encoding="utf-8", errors="replace")
    bib_keys = re.findall(r"(?im)^@[A-Za-z]+\{(fireplume_R\d{5}),", bib_text)
    expected_bib_keys = {f"fireplume_{record_id}" for record_id in included_ids}
    if len(bib_keys) != 562:
        errors.append(f"included-studies BibTeX entry count: {len(bib_keys)} != 562")
    if set(bib_keys) != expected_bib_keys:
        errors.append("included-studies BibTeX keys do not exactly match included Record_ID values")
    if len(bib_keys) != len(set(bib_keys)):
        errors.append("duplicate BibTeX keys in included_studies.bib")
    if re.search(r"&(?:amp|mdash|ndash|quot|apos|lt|gt);", bib_text, re.I):
        errors.append("HTML entity remains in included_studies.bib")
    allowed_preprint_misc = {
        "fireplume_R03305",
        "fireplume_R09530",
        "fireplume_R09714",
        "fireplume_R10844",
        "fireplume_R11159",
        "fireplume_R11355",
        "fireplume_R11841",
    }
    misc_keys = set(re.findall(r"(?im)^@misc\{(fireplume_R\d{5}),", bib_text))
    if misc_keys != allowed_preprint_misc:
        errors.append(
            "unexpected @misc bibliography set: "
            f"missing={sorted(allowed_preprint_misc - misc_keys)}, "
            f"extra={sorted(misc_keys - allowed_preprint_misc)}"
        )

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("VALIDATION PASSED")
print("72,593 inputs -> 64,922 source linkages; 27,239 screened; 713 sought; 622 assessed; 562 included; 60 excluded; 91 not retrieved.")
print("19 final figures + 1 compact platform/sensor table source; 562-entry corpus bibliography.")
print("51 duplicate-collision decisions and 105 active manuscript-source scope records.")
