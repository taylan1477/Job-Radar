# Graph Report - job-radar  (2026-10-30)

## Corpus Check
- Corpus is ~21,287 words - fits in a single context window. You may not need a graph.

## Summary
- 220 nodes · 454 edges · 13 communities (7 shown, 6 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Domain Models and Test Suite
- Data Analysis and NLP Scoring
- Google Sheets and Excel Sync
- Kariyer Scraper Pipeline
- Main CLI Orchestrator and Logging
- Architecture Showcase and Docs
- RSS and Multi-Source Ingestion
- TF-IDF Field Classifier

## God Nodes (most connected - your core abstractions)
1. `ScoringService` - 21 edges
2. `Job` - 16 edges
3. `fix_sheet()` - 14 edges
4. `score_job()` - 12 edges
5. `FieldDetector` - 11 edges
6. `run()` - 10 edges
7. `JobField` - 10 edges
8. `JobLocation` - 10 edges
9. `JobLevel` - 10 edges
10. `normalize_text()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Job Radar Spreadsheet Schema` --implements--> `ScoredJob`  [INFERRED]
  graphify-out/converted/Job Radar1_be49ddb9.md → src/core/models.py
- `Weighted Scoring Formula` --conceptually_related_to--> `calculate_score()`  [INFERRED]
  README.md → src/core/scorer.py
- `Excel Job Listings Dump` --semantically_similar_to--> `Job Radar Spreadsheet (İlanlar)`  [INFERRED] [semantically similar]
  excel_dump.txt → graphify-out/converted/Job Radar1_be49ddb9.md
- `run()` --indirect_call--> `fetch_all_kariyer_jobs()`  [INFERRED]
  main.py → src/clients/kariyer_scraper.py
- `run()` --indirect_call--> `fetch_all_linkedin_jobs()`  [INFERRED]
  main.py → src/clients/linkedin_scraper.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Job Scoring Pipeline Architecture** — readme_nlp_scoring_engine, src_core_nlp_processor, src_core_scorer, src_core_scoring_service, docs_technical_showcase_sezzle_scoring_service_impl [EXTRACTED 0.95]
- **Sezzle Clean Code Application Portfolio** — docs_presentation_guide_document, docs_technical_showcase_sezzle_case_study, docs_technical_showcase_sezzle_pdf_doc, src_core_scoring_service, src_core_models, tests_test_scoring_service [EXTRACTED 0.95]

## Communities (13 total, 6 thin omitted)

### Community 0 - "Domain Models and Test Suite"
Cohesion: 0.09
Nodes (13): Job, JobField, JobLevel, JobLocation, ScoredJob, ScoringService, run_showcase(), service() (+5 more)

### Community 1 - "Data Analysis and NLP Scoring"
Cohesion: 0.09
Nodes (17): NLP-Powered Job Scoring, analyze(), parse_hyperlink(), _extract_url(), analyze_overlap(), parse_hyperlink(), detect_language(), normalize_text() (+9 more)

### Community 2 - "Google Sheets and Excel Sync"
Cohesion: 0.09
Nodes (16): Excel Job Listings Dump, Job Radar Spreadsheet Schema, Job Radar Spreadsheet (İlanlar), Weighted Scoring Formula, append_jobs(), apply_conditional_formatting(), _extract_url(), fix_sheet() (+8 more)

### Community 3 - "Kariyer Scraper Pipeline"
Cohesion: 0.13
Nodes (11): _build_search_url(), _clean_title(), _extract_location(), fetch_all_kariyer_jobs(), fetch_kariyer_search(), _is_relevant(), _parse_cards_from_page(), _build_search_url() (+3 more)

### Community 4 - "Main CLI Orchestrator and Logging"
Cohesion: 0.14
Nodes (8): print_job_summary(), run(), show_menu(), fetch_all_jsearch_jobs(), _parse_jsearch_job(), _search_jobs(), clear_sheet(), setup_logger()

### Community 5 - "Architecture Showcase and Docs"
Cohesion: 0.17
Nodes (11): Clean Code Engineering Decisions, Job Application Presentation Guide, Technical Case Study: Job Radar Scoring Engine, Domain Modeling Specification, Technical Case Study PDF: Job Radar Scoring Engine, Quality Assurance & Unit Testing Showcase, Scoring Service Architecture Showcase, extract_sheet_id() (+3 more)

### Community 6 - "RSS and Multi-Source Ingestion"
Cohesion: 0.19
Nodes (8): Job Radar Project, Multi-Source Job Aggregation, Job Radar Development Roadmap, Smart Google Sheets Integration, Python Dependencies Specification, fetch_all_jobs(), fetch_feed(), _parse_entry()

## Knowledge Gaps
- **3 isolated node(s):** `Job Radar Development Roadmap`, `Clean Code Engineering Decisions`, `Technical Case Study PDF: Job Radar Scoring Engine`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 87 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ScoringService` connect `Domain Models and Test Suite` to `TF-IDF Field Classifier`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ScoringService` (e.g. with `Job` and `JobField`) actually correct?**
  _`ScoringService` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Job Radar Development Roadmap`, `Clean Code Engineering Decisions`, `Technical Case Study PDF: Job Radar Scoring Engine` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Domain Models and Test Suite` be split into smaller, more focused modules?**
  _Cohesion score 0.08521870286576169 - nodes in this community are weakly interconnected._
- **Why does `FieldDetector` connect `TF-IDF Field Classifier` to `Domain Models and Test Suite`, `Data Analysis and NLP Scoring`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Should `Data Analysis and NLP Scoring` be split into smaller, more focused modules?**
  _Cohesion score 0.09175377468060394 - nodes in this community are weakly interconnected._
- **Why does `normalize_text()` connect `Data Analysis and NLP Scoring` to `Domain Models and Test Suite`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._