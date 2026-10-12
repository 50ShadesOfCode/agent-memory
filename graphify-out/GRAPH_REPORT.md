# Graph Report - agent-memory  (2026-10-12)

## Corpus Check
- 201 files · ~102,901 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: .typed 5, (none) 2, .example 1)

## Summary
- 2532 nodes · 6316 edges · 163 communities (106 shown, 57 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 1071 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Executor Grading Runs
- Access Log Storage
- OpenCode Plugin Package
- Harness Verdict Driver
- Index Database
- Capture and Store Core
- Manage Proposal Tests
- LLM Judge Regrading
- Distill Apply Pipeline
- Manage Review Reasoning
- CLI Commands
- MemCore System Harness
- Recall Eligibility
- Executor Negotiation Loop
- Experiment Write Arms
- Core Module Map
- Fixed Exam Harness
- Muse and OpenRouter Bridge
- Provenance Tracking
- Config Surface
- Host Setup Report
- Frontmatter Dialect
- Muse SDK Bootstrap
- Store Locking and Errors
- Executor Launch and Hooks
- Batch Write Validation
- Field Validation
- Manage Decision Core
- Manage Reasoning Tests
- Muse Bridge HTTP Server
- Hook Entry Launcher
- Host Interop Matrix
- Interop Cost Tiers
- Slug and Storage Rules
- Vector Index
- Harness Metrics
- Host Dialects
- Memory System Dialects
- Schema Layout Tests
- Write Trigger Tests
- Decision Ledger
- Endpoint Reasoner
- Design Doc Index
- Embedder
- Progressive Trace Tests
- Muse Integration Tests
- Host CLI Reasoner
- Increment Batching
- Staged Write Reaping
- Batch Write Tests
- OpenCode Host Tests
- Store Layout Paths
- Native Memory System
- Muse Host Tests
- Frontmatter Tests
- Poisoning Red Team
- Credential Minting
- Timestamp Normalization Tests
- Benchmark Datasets
- Muse Session Adapter
- Management Boundary Tests
- Agentic Executor Tests
- SDK Bootstrap Tests
- Doctor Checks
- Archive Sessions
- Record Rendering
- Dream Report Clustering
- Distill Triggers
- Muse Launcher
- Host Invocation Isolation
- Arm Summary Reports
- Simplified Read Manage Tests
- Recall Benchmark Tests
- MCP Management Tools
- Muse Sandbox Probe
- Entry Equivalence Tests
- Coverage Probe
- Trigger Tests
- Rank Fusion Candidates
- OpenCode Plugin Tests
- MCP HTTP Handler
- Vertex Credentials
- Export and Portability Tests
- Projection Indexer Tests
- Read Exposure Gate
- Evidence Read Access
- Interop Check Facts
- Context Disclosure Tests
- Correction Concurrency Tests
- Workspace Isolation
- TypeScript Config
- Muse Executor Isolation Tests
- Muse Code Dialect
- LoCoMo Dataset
- Test Fixtures
- Host Setup Pipeline
- Read Tracks Design
- Host Adapter Plans
- Store Export
- Muse Preflight Probe
- Supersede-On-Write Tests
- Embedder Test Fakes
- Write Scaling Tests
- MCP Framing Errors
- Exposure Gate Tests
- Context Builder
- Hermes Dialect
- Package Workspace
- Soak and Growth Tests
- Raw Material Tests
- Host Hook Tests
- Core Boundary Invariants
- Magic Number Lint
- Secret Redaction
- Unicode JSONL Framing
- T0 Duplicate Management Plans
- Zero-Hit Recall Tests
- Failure Recovery Tests
- Muse Boundary Tests
- Recovery and Stress Plans
- TOML Renderer
- Fixed Recall Experiments
- Release 0.10 Notes
- Release 0.2.0 Notes
- Management Audit Docs
- Experiment Protocol Docs
- T0 Identity Plans
- Injection Track Tests
- CI Pipeline
- MUSE Launcher
- Raw Evidence Docs
- Store Sensitivity TODO
- Frozen Clock Fixtures
- Write Strategy Track
- Recall Scope Plans
- Red Team Test Layers
- Codex Transcript Parsing
- Executor CLI Call Tests
- Offline Recall Track
- Boundary Distill Plan
- Provenance Trace Reads
- Simplify Read Manage Plan
- T0 Duplicate Identity
- Write Scaling Fix Plan

## God Nodes (most connected - your core abstractions)
1. `Store` - 234 edges
2. `ValidationError` - 125 edges
3. `Manage` - 114 edges
4. `Recall` - 103 edges
5. `MemoryRecord` - 83 edges
6. `Config` - 76 edges
7. `FieldError` - 75 edges
8. `StoreLayout` - 67 edges
9. `cli()` - 37 edges
10. `store_lock()` - 36 edges

## Surprising Connections (you probably didn't know these)
- `Three Read Tracks` --semantically_similar_to--> `Injection, Recall and Context Tracks`  [INFERRED] [semantically similar]
  README.md → docs/design/read-paths.md
- `test_archive_module_exposes_no_destructive_interface()` --uses--> `Archive`  [INFERRED]
  tests/unit/test_storage.py → packages/core/src/agent_memory/core/archive.py
- `test_a_single_invalid_weight_uses_the_same_validation_boundary()` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_batch_write.py → packages/core/src/agent_memory/core/errors.py
- `test_malformed_muse_settings_fail_without_overwrite()` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_muse_host.py → packages/core/src/agent_memory/core/errors.py
- `test_muse_host_id_and_alias_are_canonical()` --uses--> `ValidationError`  [INFERRED]
  tests/unit/test_muse_host.py → packages/core/src/agent_memory/core/errors.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Files Are Truth, Indexes Are Caches Invariant System** — agents_markdown_files_single_source_of_truth, docs_design_projection_and_cache_indexes_are_rebuildable_caches, docs_design_projection_and_cache_touched_files_projection, docs_design_read_paths_reads_never_mutate_truth, docs_design_batch_write_boundaries_batch_atomic_rollback [INFERRED 0.85]
- **Host-Borrowed Reasoning Without a Core Model Client** — agents_no_llm_client_in_core, docs_design_executor_reasoning_core_holds_no_model_client, docs_design_executor_reasoning_fixed_grammar_verdicts, docs_design_entry_adapters_zero_algorithm_boundary, docs_design_host_adapters_executor_dialect_boundary [INFERRED 0.85]
- **Reversible Unattended Management** — agents_manage_never_destroys_information, docs_design_sleep_consolidation_t0_t1_authority_tiers, docs_design_sleep_consolidation_reversible_manage_operations, docs_design_management_operation_boundaries_t0_duplicate_supersession, docs_design_management_operation_boundaries_full_list_link_replacement [INFERRED 0.85]
- **Rule-Only Sleep T0 Safety Changes** — docs_plans_t0_exact_duplicate_identity_structured_identity, docs_plans_t0_system_group_boundaries_system_group_protection, docs_plans_memory_management_audit [INFERRED 0.75]
- **Host Adapter Surface Across Hosts** — docs_plans_opencode_host_adapter, docs_plans_opencode_host_adapter_plan, docs_plans_muse_code_host, docs_plans_muse_sdk_managed_backend [INFERRED 0.85]
- **Read Path Simplification and Bounded Evidence** — docs_plans_scoped_recall_before_limit, docs_plans_simplify_recall_manage_memory_only_read_path, docs_plans_raw_evidence_capability_merge_trace_capability [INFERRED 0.75]

## Communities (163 total, 57 thin omitted)

### Community 0 - "Executor Grading Runs"
Cohesion: 0.05
Nodes (50): RunMetadata, RunMetadataSink, cli(), _near_duplicates(), _system_group_records(), test_a_batch_of_memories_is_written_in_one_call(), test_a_malformed_batch_line_names_the_line(), test_a_plain_sleep_asks_the_library_executor() (+42 more)

### Community 1 - "Access Log Storage"
Cohesion: 0.07
Nodes (23): AccessLog, Chunk, chunks(), outline(), OutlineEntry, _sections(), IndexConfig, ManageConfig (+15 more)

### Community 2 - "OpenCode Plugin Package"
Cohesion: 0.06
Nodes (44): description, devDependencies, @opencode/plugin, typescript, exports, name, peerDependencies, @opencode/plugin (+36 more)

### Community 3 - "Harness Verdict Driver"
Cohesion: 0.08
Nodes (36): Verdict, _archived_messages(), _driver(), _instance(), LimitedHost, _memcore_driver(), MemcoreStubHost, StubHost (+28 more)

### Community 4 - "Index Database"
Cohesion: 0.08
Nodes (9): Indexer, IndexReport, content_hash(), Manifest, ManifestDelta, Hit, SearchIndex, to_match_query() (+1 more)

### Community 5 - "Capture and Store Core"
Cohesion: 0.08
Nodes (31): Capture, _capture_locked(), _layout(), _reenter(), test_concurrent_mark_updates_lose_nothing(), test_concurrent_session_appends_keep_contiguous_indices(), test_store_lock_acquires_and_releases(), test_store_lock_reenters_in_the_same_thread() (+23 more)

### Community 6 - "Manage Proposal Tests"
Cohesion: 0.10
Nodes (47): Manage, _find(), _flat_topic(), _kinds(), _proposal_kinds(), test_a_crowded_menu_directory_is_clustered_without_a_ruling(), test_a_crowded_system_directory_keeps_its_fields_paths_and_scope(), test_a_decided_proposal_is_never_proposed_again() (+39 more)

### Community 7 - "LLM Judge Regrading"
Cohesion: 0.08
Nodes (29): Judge, regrade(), _says_yes(), _available(), _calibrate(), _clock_at(), _code_revision(), _coerce() (+21 more)

### Community 8 - "Distill Apply Pipeline"
Cohesion: 0.08
Nodes (22): _apply(), _drop_replays(), pointer_of(), _provenance_key(), check(), _latest_cited_time(), operation_of(), profile_lines() (+14 more)

### Community 9 - "Manage Review Reasoning"
Cohesion: 0.06
Nodes (30): manage_review(), Draft, parse(), Part, _parts(), Reasoner, render(), _string() (+22 more)

### Community 10 - "CLI Commands"
Cohesion: 0.16
Nodes (34): _archived_sessions(), _body(), _confirm_human(), _context(), _correct(), _decide(), _delete(), _distill() (+26 more)

### Community 11 - "MemCore System Harness"
Cohesion: 0.08
Nodes (4): _memcore_binary(), MemcoreSystem, MemorySystem, texts_of()

### Community 12 - "Recall Eligibility"
Cohesion: 0.10
Nodes (22): Recall, _names(), test_a_deleted_record_leaves_the_default_surface_but_not_the_past(), test_a_hit_in_a_long_body_carries_the_section_anchor(), test_adversarial_scopes_agree_and_leak_nothing(), test_as_of_walks_back_up_the_supersede_chain(), test_backslash_inside_scope_matches_nothing(), test_empty_scope_means_unscoped() (+14 more)

### Community 13 - "Executor Negotiation Loop"
Cohesion: 0.08
Nodes (24): _clip(), _extend(), negotiate(), Outcome, _render(), _run(), _split(), WriteConfig (+16 more)

### Community 14 - "Experiment Write Arms"
Cohesion: 0.09
Nodes (13): Arm, parse(), Episode, Turn, _batched(), Driver, ExperiencePhase, IsolationBreach (+5 more)

### Community 15 - "Core Module Map"
Cohesion: 0.07
Nodes (5): Session, _render(), build_context(), build(), test_observation_on_off_preserves_cli_bytes_and_core_returns()

### Community 16 - "Fixed Exam Harness"
Cohesion: 0.08
Nodes (21): fixed_exam(), stocked(), test_recall_still_never_mutates_truth_when_the_harness_drives_it(), test_the_fixed_prompt_carries_the_context_and_the_question(), test_the_isolation_gate_sees_the_shell_and_the_store_fills_it_afterwards(), test_a_speaker_is_carried_into_the_turn_because_two_people_are_talking(), test_an_unanswerable_question_is_marked_as_one(), test_episode_identifiers_are_stable_across_two_conversions() (+13 more)

### Community 17 - "Muse and OpenRouter Bridge"
Cohesion: 0.10
Nodes (18): _muse_provider_checks(), _as_text(), auth_path(), _BridgeServer, OpenRouterBridge, Credential, detect_credential(), ensure_proxy() (+10 more)

### Community 18 - "Provenance Tracking"
Cohesion: 0.11
Nodes (7): Action, _duplicate_key(), _entry_of(), render(), write(), MemoryRecord, validate()

### Community 19 - "Config Surface"
Cohesion: 0.14
Nodes (22): Config, _as_float(), test_the_exam_prompt_never_carries_experience_content(), test_config_round_trips_through_disk(), test_default_recall_fingerprint_matches_memory_only_policy(), test_defaults_are_complete_and_self_consistent(), test_enabling_vector_changes_the_recall_fingerprint_and_so_does_the_model(), test_every_factory_group_field_has_a_source_that_may_name_a_directory() (+14 more)

### Community 20 - "Host Setup Report"
Cohesion: 0.09
Nodes (16): _codes(), _provider_target(), _stub_live_host_reasoner(), test_codex_doctor_flags_disabled_hooks_read_only_sandbox_and_store_failure(), test_codex_doctor_recognizes_a_configured_external_store_root(), test_fresh_and_repeated_setup_share_one_idempotent_pipeline(), test_host_reasoner_failure_prevents_ready(), test_malformed_host_config_is_never_overwritten() (+8 more)

### Community 21 - "Frontmatter Dialect"
Cohesion: 0.12
Nodes (21): StorageConfig, parse(), _parse_mapping(), _parse_scalar(), render(), _render_scalar(), split_document(), _split_items() (+13 more)

### Community 22 - "Muse SDK Bootstrap"
Cohesion: 0.15
Nodes (11): _launcher_path(), _live_preflight(), _node_version(), _required_checks_pass(), run(), _sdk_install_command(), _sdk_version(), _semver() (+3 more)

### Community 23 - "Store Locking and Errors"
Cohesion: 0.09
Nodes (7): LockTimeoutError, MemoryStoreError, store_lock(), bounded(), emit(), invoke(), Pending

### Community 24 - "Executor Launch and Hooks"
Cohesion: 0.18
Nodes (20): launch_distill(), _sibling(), _atomic_write(), canonical_host(), default_settings_path(), detect(), hook_command(), install() (+12 more)

### Community 26 - "Field Validation"
Cohesion: 0.10
Nodes (16): _fields(), _record(), _record_batch(), FieldError, ValidationError, _as_list(), _optional_str(), _known_fields() (+8 more)

### Community 27 - "Manage Decision Core"
Cohesion: 0.12
Nodes (3): Proposal, _similarity(), _tokens()

### Community 28 - "Manage Reasoning Tests"
Cohesion: 0.21
Nodes (19): _open(), Recorder, _siblings(), test_a_cap_of_zero_withholds_a_supersede_and_leaves_it_open(), test_a_merge_without_content_is_withheld_rather_than_applied(), test_a_rejection_closes_the_proposal_without_touching_a_file(), test_a_reply_wrapped_in_a_code_fence_is_still_read(), test_a_verdict_naming_a_target_outside_the_proposal_changes_only_the_proposal() (+11 more)

### Community 29 - "Muse Bridge HTTP Server"
Cohesion: 0.11
Nodes (10): _Bridge, _environment(), _fake_muse(), test_background_exec_gets_a_fresh_owned_bridge(), test_launcher_forwards_shutdown_signal_to_owned_muse(), test_launcher_reports_missing_credential_before_starting_muse(), test_launcher_reports_missing_real_muse_binary(), test_launcher_uses_existing_muse_auth_without_rewriting_it() (+2 more)

### Community 30 - "Hook Entry Launcher"
Cohesion: 0.14
Nodes (13): _arm(), _raise(), _boundary(), cli(), _disarm(), handle(), _inject(), _items() (+5 more)

### Community 31 - "Host Interop Matrix"
Cohesion: 0.11
Nodes (12): HostSpec, StubHost, test_a_memory_written_by_one_host_is_read_by_another(), test_a_reader_that_finds_nothing_fails_rather_than_passing_quietly(), test_each_pair_gets_its_own_store_so_a_pass_cannot_borrow_another_pair_s_write(), test_the_matrix_covers_every_ordered_pair(), test_the_rendered_matrix_names_the_failures(), FakeHost (+4 more)

### Community 32 - "Interop Cost Tiers"
Cohesion: 0.11
Nodes (13): _affordable(), _spec(), test_claude_code_delivers_the_system_prompt_by_flag(), test_codex_is_given_write_access_to_the_store_it_must_reach(), test_codex_without_tools_stays_read_only(), test_every_dialect_builds_a_command_that_starts_with_its_binary(), test_hermes_enables_only_the_toolset_that_reaches_the_mem_cli(), test_hermes_re_adds_the_prefix_it_is_about_to_strip() (+5 more)

### Community 33 - "Slug and Storage Rules"
Cohesion: 0.09
Nodes (7): test_a_derived_name_names_the_cause_and_the_way_out(), test_a_group_that_slugs_to_nothing_names_the_cause(), test_archive_module_exposes_no_destructive_interface(), test_find_rejects_a_parseable_but_invalid_file_loudly(), test_invalid_frontmatter_is_rejected_with_a_structured_error(), test_move_preserves_identity_provenance_and_links(), test_read_serializes_access_log_append()

### Community 34 - "Vector Index"
Cohesion: 0.13
Nodes (17): _candidate(), test_disabled_backend_import_and_truth_are_untouched(), test_disabled_store_never_constructs_or_calls_an_embedder(), forbidden(), test_empty_vector_index_preserves_bm25_results(), test_enabled_store_explains_how_to_install_a_missing_backend(), test_hybrid_recall_excludes_raw_corpus(), test_incremental_updates_offline_catchup_delete_and_model_change() (+9 more)

### Community 35 - "Harness Metrics"
Cohesion: 0.13
Nodes (12): MetricsSink, RunRecord, _record(), test_a_run_that_never_slept_still_summarises_under_its_arm_alone(), test_metrics_records_round_trip_through_the_sink(), test_records_written_before_the_manage_dimension_existed_still_summarise(), test_two_sleeps_of_the_same_arm_are_two_rows_in_the_report(), _record() (+4 more)

### Community 36 - "Host Dialects"
Cohesion: 0.09
Nodes (4): ClaudeCodeDialect, CodexDialect, Dialect, OpencodeDialect

### Community 37 - "Memory System Dialects"
Cohesion: 0.09
Nodes (8): memcore(), native(), test_memcore_reopens_an_existing_store_and_refuses_a_missing_one(), test_native_replay_projects_missing_index_before_retrieval(), test_paths_are_data_not_defaults(), test_the_fixed_exam_is_native_only(), test_the_native_system_archives_the_transcript(), test_the_synthesis_hint_is_a_config_knob_visible_to_the_fingerprint()

### Community 38 - "Schema Layout Tests"
Cohesion: 0.10
Nodes (12): _schema(), test_a_four_domain_store_migrates_into_the_schema_layout(), test_a_group_must_be_one_of_the_key_fields(), test_a_group_must_come_from_a_system_or_menu_field(), test_a_menu_group_must_already_exist_unless_creation_is_requested(), test_a_schema_file_declaring_the_wrong_type_name_is_rejected(), test_an_in_place_write_may_reword_but_not_change_the_fact(), test_as_of_before_the_replacement_returns_the_predecessor() (+4 more)

### Community 39 - "Write Trigger Tests"
Cohesion: 0.11
Nodes (8): _stop_event(), test_a_boundary_hook_prints_nothing_for_the_host_to_parse(), test_a_hook_fired_inside_the_executor_session_does_nothing(), test_a_kill_before_distillation_leaves_the_archived_tail_as_backlog(), test_hook_stays_exit_zero_when_signals_are_unsupported(), test_the_cron_path_reaches_the_same_state_as_the_hook_path(), test_the_hook_takes_its_host_from_the_command_line(), test_the_watermark_never_moves_backwards()

### Community 40 - "Decision Ledger"
Cohesion: 0.14
Nodes (8): Decision, DecisionLedger, _append(), test_concurrent_writers_at_volume_lose_nothing(), _write_batch(), test_two_processes_appending_decisions_lose_nothing(), test_two_processes_recording_at_once_lose_nothing(), _write()

### Community 41 - "Endpoint Reasoner"
Cohesion: 0.16
Nodes (15): ExecutorConfig, distiller(), EndpointReasoner, test_the_distiller_hands_the_configured_project_to_the_minter(), _reply(), test_an_endpoint_reasoner_reads_the_first_message(), fake_urlopen(), test_an_endpoint_reasoner_without_credentials_is_reported() (+7 more)

### Community 42 - "Design Doc Index"
Cohesion: 0.10
Nodes (18): AGENTS.md Invariants and Task Lifecycle, Batch Write Boundaries, Configuration Surface, Entry Adapters, Executor and Reasoning, Experiment and Evidence, Host Adapters, Identity and Placement (+10 more)

### Community 43 - "Embedder"
Cohesion: 0.13
Nodes (7): create_embedder(), Embedder, FastEmbedder, Entry, render_entries(), rows_to_entries(), write_entries()

### Community 44 - "Progressive Trace Tests"
Cohesion: 0.13
Nodes (14): cli(), evidence(), snapshot(), test_agentic_exam_uses_memory_first_and_bound_trace(), test_historical_access_preserves_read_semantics_and_labels_evidence(), test_in_archive_symlinks_cannot_substitute_a_different_session(), test_malformed_pointer_is_rejected(), test_missing_and_inconsistent_raw_fail_explicitly() (+6 more)

### Community 45 - "Muse Integration Tests"
Cohesion: 0.10
Nodes (3): test_muse_hook_capture_distill_and_read(), test_a_fact_dated_after_its_evidence_is_rejected(), test_memory_hits_keep_their_citations_without_raw_search()

### Community 46 - "Host CLI Reasoner"
Cohesion: 0.16
Nodes (12): _live_reasoner_check(), HostResult, HostReasoner, FakeHost, test_a_failed_host_is_reported(), test_a_host_reasoner_asks_for_no_tools(), test_a_host_reasoner_is_named_by_dialect_and_runs_that_dialect_s_binary(), test_a_host_reasoner_marks_its_session_as_the_executor_so_hooks_stand_down() (+4 more)

### Community 47 - "Increment Batching"
Cohesion: 0.21
Nodes (12): batches(), append(), _coerce(), count(), Message, read(), read_file(), resolve() (+4 more)

### Community 48 - "Staged Write Reaping"
Cohesion: 0.15
Nodes (4): MemorySchema, parse(), render(), SchemaRegistry

### Community 49 - "Batch Write Tests"
Cohesion: 0.11
Nodes (6): test_a_batch_leaves_the_same_store_as_records_written_one_by_one(), test_a_single_invalid_weight_uses_the_same_validation_boundary(), test_invalid_event_dates_reject_only_their_own_item(), test_invalid_weights_reject_only_their_own_item(), test_non_object_specs_reject_only_their_own_item(), test_the_batch_path_is_the_same_write_path()

### Community 50 - "OpenCode Host Tests"
Cohesion: 0.11
Nodes (9): _espec(), _fake_opencode(), _stub_live_host_reasoner(), test_doctor_ready_with_binary_settings_and_plugin(), test_doctor_reports_missing_opencode_binary(), test_install_without_plugin_directory_fails_closed(), test_install_without_store_root_fails_naming_the_store(), test_opencode_empty_answer_fails_like_codex_and_muse() (+1 more)

### Community 54 - "Frontmatter Tests"
Cohesion: 0.13
Nodes (8): _round_trip(), test_empty_inline_array(), test_inline_array_of_quoted_strings_round_trips(), test_inline_array_with_quoted_value_containing_other_quote_type(), test_inline_array_with_unquoted_value_containing_apostrophe(), test_parse_rejects_colon_less_line(), test_parse_rejects_duplicate_key(), test_parse_round_trip_preserves_scalar_fields()

### Community 55 - "Poisoning Red Team"
Cohesion: 0.13
Nodes (9): Obedient, test_a_captured_reasoner_is_bounded_by_the_menu_and_the_per_sleep_cap(), test_a_name_that_looks_like_a_path_traversal_is_rejected(), test_a_poisoned_memory_changes_nothing_about_what_manage_does(), test_a_poisoned_memory_is_returned_as_an_ordinary_scored_hit(), test_an_export_of_a_poisoned_store_stays_inert_json(), test_frontmatter_that_tries_to_escape_its_type_is_rejected(), test_malformed_frontmatter_on_disk_is_reported_not_silently_indexed() (+1 more)

### Community 56 - "Credential Minting"
Cohesion: 0.21
Nodes (11): _configure(), Minting, test_a_failed_mint_is_an_explicit_authentication_error(), test_a_stale_token_is_replaced(), test_a_token_is_reused_until_it_is_close_to_stale(), test_an_explicit_key_in_the_environment_is_left_alone(), test_no_project_leaves_host_managed_credentials_alone(), test_only_hermes_carries_credentials() (+3 more)

### Community 57 - "Timestamp Normalization Tests"
Cohesion: 0.18
Nodes (13): test_a_calendar_day_parses_as_utc_midnight(), test_a_calendar_day_valid_from_is_accepted_and_stored_as_utc_midnight(), test_a_canonical_store_gives_manage_nothing_to_normalise(), test_a_legacy_file_on_disk_is_still_indexed_and_upgraded_when_next_written(), test_a_valid_from_without_a_zone_or_without_a_shape_is_rejected(), test_as_of_in_a_foreign_offset_means_the_same_instant(), test_correcting_moves_updated_by_the_clock_not_the_calendar(), test_manage_upgrades_calendar_days_and_foreign_offsets_to_utc_instants() (+5 more)

### Community 58 - "Benchmark Datasets"
Cohesion: 0.17
Nodes (7): load(), session_stamp(), trim(), _trim_entry(), _supersede(), test_replayed_supersede_writes_once(), test_skipped_ops_and_parse_errors_are_reported_not_dropped()

### Community 59 - "Muse Session Adapter"
Cohesion: 0.18
Nodes (8): _conversation_item(), items(), path_for(), _text(), items(), _render(), _render_payload(), _text()

### Community 60 - "Management Boundary Tests"
Cohesion: 0.23
Nodes (11): test_feedback_for_unknown_memory_still_fails_loudly(), memory(), test_all_link_write_paths_validate_before_persisting(), test_existing_historical_links_survive_other_metadata_updates(), test_explicit_replacement_rejects_duplicate_links_without_partial_write(), test_invalid_relationship_additions_are_rejected(), test_missing_successor_does_not_change_source(), test_relationship_replacement_and_invalid_endpoints() (+3 more)

### Community 61 - "Agentic Executor Tests"
Cohesion: 0.40
Nodes (14): _call(), _empty_sheet(), _existing(), _messages(), _scripted(), _supersede(), test_a_handle_nobody_has_seen_is_still_refused(), test_a_long_observation_is_clipped() (+6 more)

### Community 62 - "SDK Bootstrap Tests"
Cohesion: 0.21
Nodes (10): _codes(), _ready_runtime(), test_bootstrap_classifies_sdk_cli_version_skew(), test_bootstrap_fails_before_live_request_when_node_is_not_supported(), test_bootstrap_reports_missing_credentials_without_rendering_auth_paths(), test_bootstrap_reports_the_exact_sdk_install_when_the_project_dependency_is_missing(), test_bootstrap_returns_a_direct_launch_contract_without_persistent_muse_config(), test_live_preflight_passes_the_store_and_redacts_child_output() (+2 more)

### Community 63 - "Doctor Checks"
Cohesion: 0.30
Nodes (10): Check, _codex_checks(), _hook_checks(), _mcp_check(), _plugin_checks(), _reasoner_checks(), Report, run() (+2 more)

### Community 64 - "Archive Sessions"
Cohesion: 0.17
Nodes (4): Archive, Clock, FrozenClock, resolve_store_root()

### Community 65 - "Record Rendering"
Cohesion: 0.20
Nodes (10): _as_instant(), canonicalise_dates(), invalidate(), conversation(), canonical(), days_between(), is_valid(), parse() (+2 more)

### Community 67 - "Distill Triggers"
Cohesion: 0.23
Nodes (4): backlog(), Due, Mark, Watermark

### Community 68 - "Muse Launcher"
Cohesion: 0.24
Nodes (10): _error(), main(), _managed_run(), _model(), _passthrough(), _real_muse(), run(), _state_home() (+2 more)

### Community 70 - "Arm Summary Reports"
Cohesion: 0.24
Nodes (8): _accuracy_of(), arm_of(), ArmSummary, _mean(), _ratio(), Report, summarise(), _system_of()

### Community 71 - "Simplified Read Manage Tests"
Cohesion: 0.14
Nodes (12): test_adapters_reject_deep_and_share_direct_management(), test_direct_merge_preserves_history_and_provenance(), test_failed_merge_rolls_back_all_files(), test_interrupted_merge_resumes_instead_of_failing_forever(), test_legacy_raw_config_knobs_load_as_ignored_compatibility(), test_legacy_status_and_index_load_without_store_reset(), test_memory_only_recall_and_explicit_limit(), test_merge_refuses_a_target_with_different_content() (+4 more)

### Community 72 - "Recall Benchmark Tests"
Cohesion: 0.15
Nodes (5): _seeded_store(), test_recall_benchmark(), test_invalid_external_edit_cannot_keep_old_cached_knowledge(), test_cyrillic_query_retrieves_russian_record(), test_cjk_query_retrieves_cjk_record()

### Community 73 - "MCP Management Tools"
Cohesion: 0.28
Nodes (8): dispatch(), test_cli_and_mcp_correct_text_and_replace_valid_links(), test_cli_and_mcp_preserve_legacy_links_only_when_omitted(), test_cli_and_mcp_reject_same_invalid_corrections(), test_cli_and_mcp_share_relationship_boundaries(), test_malformed_relationship_input_cannot_clear_links(), test_array_items_follow_declared_string_schema(), test_invalid_declared_types_do_not_reach_truth()

### Community 74 - "Muse Sandbox Probe"
Cohesion: 0.29
Nodes (7): _blocked_by_auth(), _error(), _hook_trace(), main(), _mcp_prompt(), _run(), _stage_auth()

### Community 75 - "Entry Equivalence Tests"
Cohesion: 0.19
Nodes (10): _stable(), test_manage_is_not_reachable_through_the_agent_facing_mcp_surface(), test_notifications_get_no_response(), test_record_through_mcp_is_visible_to_the_cli_and_vice_versa(), test_supersede_on_write_behaves_the_same_through_both_entries(), test_the_stdio_loop_answers_initialize_and_lists_tools(), test_the_two_entries_agree_on_the_recall_fingerprint(), test_tool_schemas_are_advertised_and_enforced() (+2 more)

### Community 76 - "Coverage Probe"
Cohesion: 0.24
Nodes (7): as_json(), CoverageRow, covers(), probe(), render(), _words(), _coverage()

### Community 77 - "Trigger Tests"
Cohesion: 0.33
Nodes (11): _backlog(), _mark(), _spec(), _stub_executor(), test_a_boundary_is_always_due_and_an_empty_backlog_never_is(), test_an_idle_session_becomes_due_after_the_configured_silence(), test_the_distill_command_runs_the_executor_over_a_named_session(), test_the_message_threshold_fires_without_any_hook() (+3 more)

### Community 78 - "Rank Fusion Candidates"
Cohesion: 0.24
Nodes (5): fuse_candidates(), Candidate, _cosine(), _pack(), _unpack()

### Community 79 - "OpenCode Plugin Tests"
Cohesion: 0.24
Nodes (7): _archive_text(), _mem(), test_hook_entry_never_fails_loudly(), test_kill_drill_archive_survives_and_dedupes(), test_live_distill_produces_recallable_memory(), test_live_setup_ends_ready(), test_opencode_written_memory_recalled_by_plain_core()

### Community 80 - "MCP HTTP Handler"
Cohesion: 0.29
Nodes (9): _catalog(), _handler(), do_DELETE(), do_GET(), do_PATCH(), do_POST(), _forward(), _send() (+1 more)

### Community 81 - "Vertex Credentials"
Cohesion: 0.23
Nodes (5): ReasonerUnavailableError, VertexCredentials, _first_message(), test_a_reasoner_failure_is_reported_and_leaves_the_backlog_unsettled(), unavailable()

### Community 82 - "Export and Portability Tests"
Cohesion: 0.18
Nodes (3): test_import_allows_valid_relative_paths(), test_import_refuses_absolute_path_outside_store(), test_import_refuses_path_traversal()

### Community 83 - "Projection Indexer Tests"
Cohesion: 0.20
Nodes (3): _names(), test_rebuild_after_deleting_the_index_returns_the_same_recall_set(), test_removing_a_file_drops_it_from_the_projection()

### Community 84 - "Read Exposure Gate"
Cohesion: 0.35
Nodes (8): direct_store_commands(), index_counts(), limited(), main(), observations(), probe_hits(), shell_commands(), stores()

### Community 85 - "Evidence Read Access"
Cohesion: 0.24
Nodes (4): AccessEntry, NotFoundError, ReadResult, test_trace_is_byte_read_only_even_without_an_index()

### Community 86 - "Interop Check Facts"
Cohesion: 0.35
Nodes (6): check(), Fact, InteropResult, matrix(), render(), _interop()

### Community 88 - "Correction Concurrency Tests"
Cohesion: 0.29
Nodes (8): _append_until_deleted(), _correct_abstract(), find_and_pause(), _correct_body(), find_and_signal(), _delete_source(), test_delete_racing_corrections_retains_every_successful_update(), test_independent_process_corrections_keep_both_updates_and_projection()

### Community 89 - "Workspace Isolation"
Cohesion: 0.24
Nodes (5): DisposableWorkspace, for_writing(), test_a_directory_merely_named_worktrees_is_not_a_worktree(), test_a_write_path_in_the_main_tree_is_accepted_and_absolute(), test_a_write_path_inside_a_worktree_is_refused()

### Community 90 - "TypeScript Config"
Cohesion: 0.20
Nodes (9): compilerOptions, allowImportingTsExtensions, module, moduleResolution, noEmit, skipLibCheck, strict, target (+1 more)

### Community 91 - "Muse Executor Isolation Tests"
Cohesion: 0.20
Nodes (6): test_muse_executor_carries_only_provider_routing_into_isolation(), test_muse_executor_isolates_personal_context_but_reuses_explicit_auth(), test_muse_executor_materializes_prompt_and_reads_final_jsonl(), test_muse_executor_uses_hook_pinned_settings_and_sibling_auth(), test_muse_probe_checks_path_and_version(), run()

### Community 93 - "LoCoMo Dataset"
Cohesion: 0.33
Nodes (5): convert(), _entries(), _evidence(), _identifier(), _sessions()

### Community 94 - "Test Fixtures"
Cohesion: 0.33
Nodes (6): clock(), config(), memcore_home(), seeded(), store(), append_all()

### Community 96 - "Read Tracks Design"
Cohesion: 0.25
Nodes (4): TODO: Recall Confidence Gate, TODO: recall --explain Score Breakdown, Three Read Tracks, Optional Vector Recall Index (ADR-003)

### Community 97 - "Host Adapter Plans"
Cohesion: 0.29
Nodes (6): Endpoint Opt-in and Fail-Closed Reasoning Plan, Muse Code Host Adapter Plan, Managed Muse SDK Backend Plan, OpenCode Host Adapter Spec, OpenCode Host Adapter Implementation Plan, agent-memory Skill

### Community 98 - "Store Export"
Cohesion: 0.43
Nodes (5): export_store(), import_into(), read_import(), _sources(), write_export()

### Community 99 - "Muse Preflight Probe"
Cohesion: 0.39
Nodes (3): test_live_muse_shell_hook_and_mcp_preflight(), test_muse_preflight_stages_only_auth_in_isolated_config(), test_muse_preflight_uses_canonical_mcp_tool_name()

### Community 100 - "Supersede-On-Write Tests"
Cohesion: 0.25
Nodes (5): test_a_new_record_can_supersede_an_existing_one_in_a_single_write(), test_a_record_cannot_supersede_itself(), test_a_successor_with_the_same_key_takes_the_next_ordinal_and_the_predecessor_keeps_its_name(), test_superseding_something_that_does_not_exist_is_rejected(), test_the_superseded_value_is_still_reachable_by_time_travel()

### Community 102 - "Write Scaling Tests"
Cohesion: 0.32
Nodes (3): _min_write_ms(), _seed(), test_single_write_cost_is_flat()

### Community 104 - "Exposure Gate Tests"
Cohesion: 0.43
Nodes (4): gate(), make_index(), test_pilot_gate_detects_direct_file_bypass(), test_store_gate_rejects_missing_projection()

### Community 105 - "Context Builder"
Cohesion: 0.43
Nodes (4): _body(), build(), Context, _entry()

### Community 107 - "Package Workspace"
Cohesion: 0.57
Nodes (7): agent-memory-adapters, agent-memory-cli, agent-memory-core, agent-memory-executor, agent-memory-harness, agent-memory-mcp, agent-memory-workspace

### Community 108 - "Soak and Growth Tests"
Cohesion: 0.48
Nodes (4): _percentile(), _probe(), _seed_chunk(), test_soak_recall_p99_vs_size_and_rebuild()

### Community 109 - "Raw Material Tests"
Cohesion: 0.29
Nodes (4): test_explicit_limit_expands_memory_candidates(), test_raw_corpus_is_not_a_recall_surface(), test_raw_survives_rebuild_without_being_indexed(), with_raw()

### Community 110 - "Host Hook Tests"
Cohesion: 0.29
Nodes (5): test_every_host_hook_archives_the_increment_and_launches_the_same_executor_call(), launch(), test_host_dialects_map_onto_the_universal_moments(), test_muse_hook_passes_pinned_settings_to_background_distillation(), test_setup_writes_an_absolute_hook_command_and_installs_the_skill()

### Community 116 - "T0 Duplicate Management Plans"
Cohesion: 0.40
Nodes (3): TODO: Link Proposals from Sleep, TODO: Maintenance Candidate Taxonomy in Sleep Reports, Independent Manage Layer

### Community 117 - "Zero-Hit Recall Tests"
Cohesion: 0.50
Nodes (4): execute(), FakeJudge, test_zero_hit_recall_and_read_levels(), setup()

### Community 118 - "Failure Recovery Tests"
Cohesion: 0.40
Nodes (4): test_failed_batches_restore_all_canonical_changes(), fail_predecessor_once(), test_muse_setup_preserves_settings_hooks_and_mcp_and_is_idempotent(), replace()

### Community 119 - "Muse Boundary Tests"
Cohesion: 0.40
Nodes (3): test_muse_boundaries_use_existing_capture_path(), test_muse_executor_reports_transport_failures(), test_muse_hook_events_normalize_to_existing_moments()

### Community 120 - "Recovery and Stress Plans"
Cohesion: 0.50
Nodes (3): Batch Write Failure Recovery Plan, Stress and Soak Track, Projection Dropout Report

### Community 126 - "Management Audit Docs"
Cohesion: 0.67
Nodes (3): Management Operation Boundaries Design Doc, Management Operation Audit, docs/TODO.md Follow-Ups

### Community 127 - "Experiment Protocol Docs"
Cohesion: 0.67
Nodes (3): Experiment Protocol, Benchmark and Experiment Design Plan, Testing Conventions

## Knowledge Gaps
- **52 isolated node(s):** `agent-memory-mcp`, `typescript`, `AGENTS.md Invariants and Task Lifecycle`, `Three Read Tracks`, `Independent Manage Layer` (+47 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 793 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Store` connect `CLI Commands` to `Executor Grading Runs`, `Injection Track Tests`, `Access Log Storage`, `Harness Verdict Driver`, `Index Database`, `Capture and Store Core`, `Manage Proposal Tests`, `LLM Judge Regrading`, `Distill Apply Pipeline`, `Manage Review Reasoning`, `MemCore System Harness`, `Recall Eligibility`, `Executor Negotiation Loop`, `Core Module Map`, `Fixed Exam Harness`, `Provenance Tracking`, `Config Surface`, `Host Setup Report`, `Frontmatter Dialect`, `Muse SDK Bootstrap`, `Executor Launch and Hooks`, `Batch Write Validation`, `Field Validation`, `Hook Entry Launcher`, `Host Interop Matrix`, `Vector Index`, `Harness Metrics`, `Memory System Dialects`, `Schema Layout Tests`, `Decision Ledger`, `Embedder`, `Host CLI Reasoner`, `Increment Batching`, `Staged Write Reaping`, `Batch Write Tests`, `OpenCode Host Tests`, `Store Layout Paths`, `Native Memory System`, `SDK Bootstrap Tests`, `Doctor Checks`, `Archive Sessions`, `Muse Launcher`, `Simplified Read Manage Tests`, `MCP Management Tools`, `Muse Sandbox Probe`, `Entry Equivalence Tests`, `OpenCode Plugin Tests`, `Evidence Read Access`, `Interop Check Facts`, `Correction Concurrency Tests`, `Test Fixtures`, `Host Setup Pipeline`, `Store Export`, `Embedder Test Fakes`, `Context Builder`, `Zero-Hit Recall Tests`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Are the 181 inferred relationships involving `Store` (e.g. with `_capture_locked()` and `_live_reasoner_check()`) actually correct?**
  _`Store` has 181 INFERRED edges - model-reasoned connections that need verification._
- **What connects `agent-memory-mcp`, `typescript`, `AGENTS.md Invariants and Task Lifecycle` to the rest of the system?**
  _52 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Executor Grading Runs` be split into smaller, more focused modules?**
  _Cohesion score 0.05213089802130898 - nodes in this community are weakly interconnected._
- **Why does `Config` connect `Config Surface` to `Access Log Storage`, `Harness Verdict Driver`, `Capture and Store Core`, `LLM Judge Regrading`, `Distill Apply Pipeline`, `CLI Commands`, `Recall Eligibility`, `Experiment Write Arms`, `Core Module Map`, `Provenance Tracking`, `Frontmatter Dialect`, `Executor Launch and Hooks`, `Vector Index`, `Harness Metrics`, `Memory System Dialects`, `Embedder`, `Store Layout Paths`, `Native Memory System`, `Archive Sessions`, `Test Fixtures`, `Embedder Test Fakes`, `TOML Renderer`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Are the 80 inferred relationships involving `ValidationError` (e.g. with `run()` and `run()`) actually correct?**
  _`ValidationError` has 80 INFERRED edges - model-reasoned connections that need verification._
- **Should `Access Log Storage` be split into smaller, more focused modules?**
  _Cohesion score 0.06559356136820925 - nodes in this community are weakly interconnected._