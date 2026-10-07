# Fire-Plume Review Evidence

This repository contains the auditable evidence package accompanying the TMLR paper:

**Real-Time Autonomous Systems for Tracking and Responding to Uncontrolled Fires: A Scoping Review of Sensing, Forecasting, Health-Risk Modelling, and Governance**

**Authors:** Damian Marszalski, Shanfeng Hu, Simon D Griffiths, and Nauman Aslam  
**Venue:** Transactions on Machine Learning Research (TMLR), 2026  
**OpenReview:** https://openreview.net/forum?id=70KyPTKcLA

## Citation

If you use this evidence package, please cite the associated TMLR paper:

> Marszalski, D., Hu, S., Griffiths, S. D., and Aslam, N. (2026). *Real-Time Autonomous Systems for Tracking and Responding to Uncontrolled Fires: A Scoping Review of Sensing, Forecasting, Health-Risk Modelling, and Governance*. Transactions on Machine Learning Research. https://openreview.net/forum?id=70KyPTKcLA

This citation will be updated if the final TMLR publication record provides additional bibliographic metadata. The repository state corresponding to the published paper will be preserved with a version tag/release.

The repository supports the paper's PRISMA-ScR-reported scoping review and critical thematic synthesis of fire-plume observation, autonomous sensing and state estimation, forecasting, exposure and health-risk interpretation, and governed human action.

The CSV files are the canonical machine-readable evidence records. Article PDFs and licensed raw database exports are deliberately not redistributed. A duplicated spreadsheet copy is intentionally not included so that there is only one authoritative representation of each register and no risk of a stale workbook diverging from the CSV sources.

## Frozen reconciled evidence map

- 64,922 formal source linkages
- 37,683 duplicate/source-overlap linkages removed
- 27,239 unique records screened
- 26,129 records excluded at title/abstract screening
- 397 contextual records retained outside the primary corpus
- 713 reports sought
- 622 reports assessed
- 562 included reports
- 60 full-text exclusions
- 91 reports not retrieved after documented access attempts

The 91 inaccessible reports are not exclusions and contribute no inferred findings.

## Files

| File | Purpose |
|---|---|
| `METHODS.md` | Review design, chronology, sources, screening, charting, synthesis rules and limitations |
| `methods/search_log.csv` | Exact structured queries, dates, interfaces, result counts and export status |
| `methods/source_linkage_reconciliation.csv` | Explicit bridge from 72,593 per-query/source-registry results to 64,922 linkages entering cross-source reconciliation |
| `methods/residual_duplicate_audit.csv` | Decision and rationale for all 51 normalised-title collision groups; eight confirmed duplicate manifestations merged |
| `data/prisma_counts.csv` | Authoritative review-flow counts and arithmetic reconciliation |
| `data/title_abstract_screening.csv` | All 27,239 unique screened records |
| `data/full_text_decisions.csv` | All 713 sought reports and their retrieval/eligibility outcomes |
| `data/included_studies.csv` | Minimum coding for all 562 included reports |
| `data/coding_completeness.csv` | Field-by-field missingness and usable-value audit for the 562-report coding register |
| `data/included_studies.bib` | Complete BibTeX bibliography for all 562 included reports; inclusion does not imply individual citation in the narrative manuscript |
| `data/manuscript_source_scope.csv` | Reconciliation and claim-level audit of every active manuscript citation, including occurrence counts, source files, evidence role, claim boundary, verification status and source-check note |
| `data/codebook.csv` | Definitions for the included-study fields |
| `synthesis/closest_reviews.csv` | Bounded comparison with the closest prior reviews |
| `synthesis/evidence_coverage_matrices.csv` | Machine-readable sources for the monitoring, technical, health, governance and cross-pipeline evidence-coverage matrices |
| `synthesis/matrix_supporting_sources.csv` | Traceability table linking every matrix row to representative supporting `Record_ID`s and citation keys; the anchors are not effect sizes or exhaustive study counts |
| `figures/figure_provenance.csv` | Replacement, removal, rights status and scientific boundaries for original and final manuscript figures |
| `figures/source/` | Editable LaTeX/TikZ sources for all 19 final manuscript figures plus the compact platform/sensor comparison table |
| `scripts/validate_repository.py` | Reconciles record sets, counts, codebook coverage, figure/source completeness and release constraints |

## Complete included-study bibliography

`data/included_studies.bib` contains one stable BibTeX entry for each of the 562 included reports. The keys preserve the evidence-register identifier (for example, `fireplume_R00166`) so that bibliography entries can be traced back to `data/included_studies.csv` and `data/full_text_decisions.csv`. The file is a corpus bibliography rather than the manuscript reference list: an included report may appear here even if it is not individually cited in the narrative synthesis.

The bibliography was deduplicated against DOI and normalised-title identity and then metadata-checked. Every remaining normalised-title collision is covered by `methods/residual_duplicate_audit.csv`; a title collision alone was not treated as proof that distinct conference, journal, preprint, edition, or co-publication records were one report. Missing bibliographic fields were corrected where they could be verified reliably; unverifiable identifiers, particularly DOIs, were left absent rather than inferred. The repository does not redistribute the corresponding article full texts.

## Active manuscript citation audit

All 105 citation keys active in the clean manuscript were checked against underlying source content. The check route for each key—publisher or DOI page, official record, accessible abstract, repository manuscript, or full text—is recorded in `data/manuscript_source_scope.csv`. This claim-level audit is narrower than certifying every field in the 562-report corpus register: it assesses whether each active manuscript use stays within what the cited source supports. Where the initial wording was broader than the source, the manuscript wording or attribution was corrected and the retained boundary is recorded in the same row.

## Figure and table sources

The final manuscript uses 19 review-authored figures. Their editable sources are retained individually in `figures/source/` and their provenance and scientific boundaries are recorded in `figures/figure_provenance.csv`. The same directory also contains `platform_sensor_matrix.tex`, the compact reviewer-requested platform/sensor comparison table. Superseded or unused draft figure sources are not part of the final package.

## Validation

From the repository root, run:

```bash
python scripts/validate_repository.py
```

The validator checks the reconciled counts and linkage bridge, unique record identifiers, duplicate-adjudication coverage, mutually exclusive full-text outcomes, agreement between included and full-text decisions, controlled evidence roles, field-level coding completeness recomputed from the included-study register, matrix-to-source traceability, the 105-row manuscript-source scope and source-content audit, PRISMA source consistency, synthesis codes, the 562-entry included-study bibliography, final figure/source completeness, required files and prohibited public content.

## Reuse boundary

Repository-authored documentation, scripts and original synthesis data are released under `LICENSE.md`. Bibliographic metadata remains subject to the terms of its source databases. No licence is granted here for article full text or licensed database exports because those materials are not included.
