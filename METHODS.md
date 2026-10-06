# Review methods

## Design and chronology

The work is reported as a PRISMA-ScR-informed scoping review and critical thematic synthesis. It was not prospectively registered and was not independently dual-screened. Accordingly, this repository supports audit of the recorded search and decisions but does not claim that title/abstract false-negative rates have been independently estimated.

An exploratory Google Scholar thematic search first established the interdisciplinary scope. Exact per-record query provenance was not preserved for that exploratory stage and is not reconstructed retrospectively. A structured protocol was finalised on 14 August 2026, followed by documented searches of PubMed, Semantic Scholar Academic Graph, Scopus, ACM Digital Library and IEEE Xplore. Web of Science Core Collection was planned but could not be searched because institutional access was unavailable. OpenAlex and arXiv were used only for validation or pilot work and were excluded from formal identification counts.

Structured searches were completed and frozen on 22 August 2026. An initial 381 retrieved reports were assessed and their eligibility decisions were author-approved on 23 August. A documented recovery audit then revisited the 332 reports that had not been retrieved: 241 complete reports were recovered and assessed, producing 239 additional inclusions and two additional exclusions. The author approved all 332 recovery outcomes on 24 August. The final full-text stage therefore contains 622 assessed reports, 562 inclusions, 60 exclusions and 91 inaccessible reports.

The full structured search log, including exact queries, dates, interfaces, reported results, exported results and export-cap handling, is provided in `methods/search_log.csv`.

## Eligibility

The primary inclusion rule required an explicit fire context and a material contribution to at least one part of the observation-to-action pathway:

1. fire or plume observation and concentration mapping;
2. fire-source, perimeter or state estimation used as a downstream input;
3. smoke, transport, dispersion or concentration forecasting;
4. exposure or health-risk interpretation;
5. protective decision-making, intervention or communication; or
6. fire-specific governance and operational oversight.

Evidence syntheses and explicitly labelled adjacent-domain transfer evidence were retained only where they supported scope positioning, method transfer or governance requirements. They were not treated as direct fire-deployment evidence.

Full-text exclusions were limited to recorded failures of the frozen eligibility rules, including no eligible fire context or pathway contribution, ineligible report type, superseded or duplicate report lineage, and other report-specific scope failures. Reports that could not be retrieved are not exclusions because their eligibility remains unknown.

## Record processing and screening

The database interfaces reported 72,413 per-query results and the exploratory registry contributed 180 records, for 72,593 inputs before within-source processing. PubMed query overlap was collapsed by PMID (4,186 to 2,508 linkages) and Semantic Scholar overlap by work identifier (17,142 to 11,149); ACM, IEEE and Scopus query-result linkages were retained at this stage. This produced 64,922 formal linkages entering cross-source reconciliation. The source-by-source arithmetic and evidence path are in `methods/source_linkage_reconciliation.csv`.

Cross-source reconciliation and duplicate merging removed 37,683 linkages, leaving 27,239 unique records. Title/abstract screening excluded 26,129 records, retained 397 contextual records outside the primary corpus, and advanced 713 reports to retrieval.

A final metadata and duplicate audit was extended on 4 September 2026 to adjudicate every one of the 51 normalised-title collision groups in the provisional title/abstract register. Eight duplicate manifestations were merged where publication identity was supported by a shared source DOI, verified DOI aliases, or concordant title/year/authorship and publication identity. Forty-three groups were retained because the title collision alone did not override distinct year, authorship, DOI, venue, edition, document-type, or known version/co-publication identities. One removed record, R17292, carried an unrelated DOI; R17293 retains the correct article identity. All decisions and rationales are recorded in `methods/residual_duplicate_audit.csv`. This audit changed the identification-stage counts above but did not change the 713 reports sought, the full-text decisions or the 562-report included corpus.

Title/abstract screening was rule-assisted and was not an independently dual-screened process. The public `Human_Verification` field now distinguishes author-approved downstream retrieval/full-text outcomes from rule-assisted title/abstract exclusions and contextual classifications that were not individually author-verified; no record is left with a misleading workflow placeholder such as `Pending author verification`. The released register does not contain abstracts or a completed probability sample of exclusions, so an empirical false-negative estimate cannot be reconstructed from this package. Full-text eligibility assessment was AI-assisted and followed by one-author review of every assessed report. The complete decisions and report-specific reasons are recorded in `data/full_text_decisions.csv`.

For most reports that were successfully retrieved, the author manually visited publisher, repository, institutional, author or library pages to obtain the full text; Zotero-assisted and other recovery routes were used where helpful. Ninety-one reports remained inaccessible. They remain visible in the accountability register, are not counted as full-text exclusions and contribute no findings.

## Data charting

Minimum coding for the 562 included reports covers bibliographic identity, fire type and specificity, task, platform, sensor or data source, method/model, evidence setting, evaluation design, metrics, uncertainty treatment, deployment maturity, evidence role and claim boundary. Missing or unreported detail is left explicit rather than inferred. Eligibility approval is distinct from independent verification of every detailed coding cell.

The companion `data/coding_completeness.csv` reports field-level blanks, explicit unknown/not-reported values, not-applicable values and usable-value coverage. It is the compact audit of coding depth: for example, deployment maturity has a supported value for 374 reports, is not applicable for 64 evidence syntheses or guidance reports, and remains explicitly not fully coded/reported for 124 reports. This avoids converting missing source detail into invented coding and avoids implying that every detailed cell received an independent manual check.

Deployment maturity uses the following descriptive scale:

- `0`: conceptual proposal;
- `1`: simulation or offline proof of concept;
- `2`: retrospective, controlled or field-observational evaluation;
- `3`: pilot or workflow integration;
- `4`: operational deployment; and
- `N/A`: evidence synthesis or guidance.

## Included-study bibliography and metadata checking

After the 562-report included corpus was frozen, a complete corpus bibliography was generated as `data/included_studies.bib`. Bibliographic deduplication used normalised DOI identity and normalised-title checks, with near-title cases reviewed separately so that genuinely distinct reports were not collapsed. Bibliographic metadata were checked separately from eligibility assessment and full-text retrieval: incomplete or suspicious records received targeted verification, while identifiers that could not be established confidently were left absent rather than inferred. The final bibliography contains one stable entry per included `Record_ID` and is intended to make the complete included corpus auditable; inclusion in this bibliography does not imply that every report is individually cited in the narrative manuscript.

## Active manuscript citation verification

The 105 citation keys active in the clean manuscript were reconciled to 208 citation occurrences and checked against underlying source content. The source route and claim-level result are recorded per key in `data/manuscript_source_scope.csv`. Checks used accessible publisher or DOI records, official database abstracts, repository manuscripts, or full text as available; the register states the route rather than implying uniform full-text access. The check evaluated the manuscript's actual use of each source. Where a source supported only a narrower population, task, setting, evidence type, or inference than the initial prose suggested, the wording or attribution was corrected and the retained claim boundary was recorded.

This active-citation audit does not convert all 562 included reports into individually re-verified studies, does not replace the recorded one-author eligibility assessment, and does not establish that a cited component result validates the proposed end-to-end architecture.

## Synthesis

Studies were grouped by evidence role:

1. direct fire-specific evidence;
2. fire-specific interface or source-state evidence;
3. fire-specific evidence synthesis or guidance; and
4. transferred adjacent-domain evidence.

Descriptive evidence-role subtypes may refine these four parent families where useful for auditability; they do not constitute additional top-level evidence classes.

Every included report also carries the controlled `Evidence_Role_Parent` field, and every active manuscript citation is reconciled in `data/manuscript_source_scope.csv`. A citation outside the 562-report primary corpus is explicitly labelled as contextual, excluded-context-only, or external methods/guidance/positioning evidence and is not counted as primary synthesis evidence.

Cross-study performance rankings were not created because tasks, incidents, datasets, metrics and evaluation settings were generally not commensurable. Comparative language is permitted only where the underlying reports use sufficiently comparable tasks, data, metrics and evaluation designs. Component performance is not treated as evidence that an end-to-end observation-to-action architecture has been implemented or validated.

The evidence-coverage matrices use `D` for directly addressed, `P` for partially addressed, `N` for not assessed and `NA` for not applicable. These codes are qualitative coverage judgements, not effect sizes.

The five matrices remain in one normalised machine-readable file rather than five duplicated spreadsheets. `synthesis/matrix_supporting_sources.csv` joins to `synthesis/evidence_coverage_matrices.csv` on `(Matrix, Evidence_or_function)` and supplies representative supporting `Record_ID`s and active citation keys for every matrix row. These anchors make the basis of each row inspectable, but they are deliberately not presented as exhaustive study counts or cell-level effect estimates.

## Limitations

- Exact per-record provenance was not preserved for the exploratory Google Scholar stage.
- The structured protocol was finalised after the exploratory stage and was not prospectively registered.
- Web of Science could not be searched because institutional access was unavailable.
- Title/abstract screening was rule-assisted rather than independently dual-screened.
- The released title/abstract register does not contain abstracts or a completed random sample of exclusions; a false-negative rate has therefore not been established.
- Licensed raw database exports and source-identity manifests are not redistributed, so the documented aggregate linkage transformation is auditable but cannot be replayed independently from raw records using this public package alone.
- One author verified the assessed full-text eligibility decisions.
- Ninety-one reports remained inaccessible and therefore contribute no findings.
- Minimum corpus coding is complete, but some detailed fields remain explicitly unreported or require source-specific verification.
- The active-citation check used the strongest accessible source content for each citation, but access depth varies between full text, repository manuscripts, and official abstracts; the route is explicit in the audit ledger.
- The evidence base is heterogeneous, so qualitative coverage synthesis does not establish comparative algorithm superiority or end-to-end operational viability.

## Public-data boundary

The repository contains sanitised bibliographic metadata, decisions, coding and synthesis artefacts. It excludes article PDFs, licensed raw database exports, institutional access details, author-identifying working files and private correspondence.
