# Co-Met Reproducibility Audit: Headless Mode Blueprint

> **Scope:** Analytical core only (Cells 1-9, 13, 15, 17). Excludes Validation/Monte Carlo cells (26-35) and all aesthetic plotting variables.

---

## 1. State Dependency Map — `ANALYSIS_CONFIG` Keys That Drive Statistics

### 1A. Pipeline-Configuration Keys (set by UI widgets, needed for headless replay)

| Key | Type | Set In | Default | Statistical Role |
|-----|------|--------|---------|-----------------|
| `prefilter_col` | `str` | Cell 3 | `'None'` | Column name for global data inclusion/exclusion filter |
| `prefilter_values` | `list[str]` | Cell 3 | `[]` | Which values of `prefilter_col` to **keep** |
| `factor1` | `str` | Cell 3 | `'None'` | Legacy alias for `filterCol1` |
| `factor2` | `str` | Cell 3 | `'None'` | Legacy alias for `filterCol2` |
| `min_papers` | `int` | Cell 3 | `1` | Min unique study IDs per subgroup |
| `min_obs` | `int` | Cell 3 | `1` | Min observations per subgroup |
| `sd_missing_strategy` | `str` | Cell 4 | `'median_cv'` | How to impute missing SDs. One of: `'nearest'`, `'median_cv'`, `'custom_cv'`, `'drop'` |
| `sd_zero_strategy` | `str` | Cell 4 | `'global_min'` | How to handle zero SDs. One of: `'global_min'`, `'same_as_missing'`, `'drop'` |
| `effect_size_type` | `str` | Cell 5 | _(user picks)_ | One of: `'lnRR'`, `'hedges_g'`, `'cohen_d'`, `'log_or'` |
| `data_type` | `str` | Cell 5 | `'raw'` | `'raw'` or `'pre_calculated'` |
| `variance_type` | `str` | Cell 5 | `'variance'` | For pre-calc mode: `'variance'`, `'se'`, or `'both'` |

### 1B. Column-Name Keys (derived from `effect_size_type`)

| Key | Example Value | Set In |
|-----|---------------|--------|
| `effect_col` | `'lnRR'`, `'hedges_g'` | Cell 5/6 |
| `var_col` | `'var_lnRR'`, `'Vg'` | Cell 5/6 |
| `se_col` | `'SE_lnRR'`, `'SE_g'` | Cell 5/6 |
| `ci_lower_col` | `'CI_lower_lnRR'` | Cell 6 |
| `ci_upper_col` | `'CI_upper_lnRR'` | Cell 6 |
| `es_config` | `dict` (full config blob) | Cell 5 |

### 1C. Global Analysis Settings (set by Cell 7 widgets)

| Key Path | Type | Default | Statistical Role |
|----------|------|---------|-----------------|
| `global_settings.alpha` | `float` | `0.05` | Significance level for all CIs and p-values |
| `global_settings.dist_type` | `str` | `'t'` | CI distribution: `'t'` (robust) or `'norm'` (z) |
| `global_settings.tau_method` | `str` | `'REML'` | Tau-squared estimator: `'REML'`, `'DL'`, or `'ML'` |
| `global_settings.use_kh` | `bool` | `True` | Knapp-Hartung correction for CIs |
| `global_settings.model_choice` | `str` | `'Auto-Select (Best AIC)'` | `'Auto-Select (Best AIC)'`, `'Force 2-Level'`, `'Force 3-Level'` |

### 1D. Subgroup Configuration (set by Cell 8 widgets)

| Key Path | Type | Set In |
|----------|------|--------|
| `subgroup_config.analysis_type` | `str` | Cell 8 — `'single'` or `'two_way'` |
| `subgroup_config.moderator1` | `str` | Cell 8 — column name |
| `subgroup_config.moderator2` | `str\|None` | Cell 8 — column name or `None` |
| `subgroup_config.min_papers` | `int` | Cell 8 |
| `subgroup_config.min_obs` | `int` | Cell 8 |
| `subgroup_config.valid_groups_list` | `list` | Cell 8 — auto-computed |

### 1E. Result/Output Keys (written by analysis engines, read by downstream cells)

| Key | Type | Written By |
|-----|------|-----------|
| `analysis_data` | `pd.DataFrame` | Cell 6 |
| `vcv_matrices` | `dict[str, np.ndarray]` | Cell 6 |
| `removed_records` | `pd.DataFrame` | Cell 4 |
| `overall_results` | `dict` | Cell 7 (`OverallDataManager`) |
| `three_level_results` | `dict` | Cell 7 (`OverallDataManager`) |
| `subgroup_results` | `dict` (contains `results_df: pd.DataFrame`) | Cell 9 |
| `meta_regression_RVE_results` | `dict` | Cell 13 |
| `spline_model_results` | `dict` | Cell 15 |
| `funnel_results` | `dict` | Cell 17 |
| `trimfill_results` | `dict` | Cell 17 |
| `pet_peese_results` | `dict` | Cell 18 |
| `cumulative_results` | `pd.DataFrame` | Cell 24 |
| `loo_results` | `dict` | Cell 21 |
| `clean_dataframe` | `pd.DataFrame` | Cell 3 |
| `sd_log` | `list[str]` | Cell 4 |
| `n_observations_pre_filter` | `int` | Cell 4 |
| `n_observations_post_filter` | `int` | Cell 4 |
| `n_papers_post_filter` | `int` | Cell 4 |
| `overall_text` | `str` | Cell 7 |
| `subgroup_text` | `str` | Cell 9 |
| `regression_text` | `str` | Cell 13 |
| `bias_text` | `str` | Cell 17 |
| `cumulative_text` | `str` | Cell 24 |

---

## 2. Analytical Orphans — Variables Trapped Outside `ANALYSIS_CONFIG`

These are math-critical values that are currently **hardcoded** inside functions or UI callbacks and would **not** be captured in a JSON settings file.

### 2A. High Priority (directly affect numerical results)

| Orphan Variable | Current Value | Location | Impact |
|----------------|---------------|----------|--------|
| `custom_cv` | User-entered float (fallback: `0.1`) | Cell 4, `run_processing()` param + widget `custom_cv_input` | SD imputation magnitude when `sd_missing_strategy == 'custom_cv'` |
| `zero_offset_fraction` | `0.01` (hardcoded) | Cell 6, `run_calculation()` line ~252 | Fraction of smallest non-zero value used to replace zeros in lnRR: `offset = min_nonzero * 0.01` |
| `zero_offset_fallback` | `0.001` (hardcoded) | Cell 6, `run_calculation()` line ~253 | Fallback offset when all values are zero/NaN |
| `match_r_ll` | `False` (widget default) | Cell 7, `OverallController._create_settings_widgets()` | Toggles full log-likelihood constant term for R compatibility |
| `df_spline` | User-selected int | Cell 15, `SplineAnalysisManager.run_analysis()` | Degrees of freedom for the natural cubic spline (number of knots) |
| `trimfill_estimator` | `'L0'` (hardcoded default) | Cell 17, `run_trimfill_analysis()` | Trim-and-fill estimator: `'L0'` or `'R0'` |
| `trimfill_side` | `'auto'` (hardcoded default) | Cell 17, `run_trimfill_analysis()` | Which side to impute: `'auto'`, `'left'`, `'right'` |
| `trimfill_max_iter` | `100` (hardcoded default) | Cell 17, `run_trimfill_analysis()` | Max iterations for trim-fill convergence |

### 2B. Medium Priority (optimizer internals — affect convergence, rarely affect final results)

| Orphan Variable | Current Value | Location |
|----------------|---------------|----------|
| `reml_max_iter` | `100` | Cell 1, `calculate_tau_squared_REML()` default param |
| `reml_tol` | `1e-8` | Cell 1, `calculate_tau_squared_REML()` default param |
| `ml_max_iter` | `100` | Cell 1, `calculate_tau_squared_ML()` default param |
| `ml_tol` | `1e-8` | Cell 1, `calculate_tau_squared_ML()` default param |
| `pm_max_iter` | `100` | Cell 1, `calculate_tau_squared_PM()` default param |
| `pm_tol` | `1e-8` | Cell 1, `calculate_tau_squared_PM()` default param |
| `3level_optimizer_ftol` | `1e-11` to `1e-12` | Cell 1 & Cell 7, L-BFGS-B options |
| `3level_start_points` | `[[0.01,0.01],[0.5,0.1],[0.1,0.5],[0.001,0.001]]` | Cell 1, `run_python_3level()` |
| `3level_param_lower_bound` | `1e-8` | Cell 1 & Cell 7, optimizer bounds |
| `3level_param_upper_bound` | `50.0` (some) / `None` (some) | Cell 1 & Cell 7 |
| `ridge_jitter` | `1e-6` | Cell 1, `_get_three_level_estimates()` Cholesky fallback |

### 2C. Low Priority (derived/auto-computed, but good to document)

| Orphan Variable | Current Value | Location |
|----------------|---------------|----------|
| `min_sd_fallback` | `0.001` | Cell 4, `run_processing()` — fallback when no positive SDs exist |
| `DATA_TYPE_SELECTED` | `'raw'` (global) | Cell 2 — set during data ingestion |
| `VARIANCE_TYPE_SELECTED` | `'variance'` (global) | Cell 2 — set during data ingestion for pre-calc mode |

---

## 3. Serialization Audit

### 3A. Non-JSON-Serializable Keys

| Key | Type | Issue |
|-----|------|-------|
| `analysis_data` | `pd.DataFrame` | Not JSON-serializable |
| `clean_dataframe` | `pd.DataFrame` | Not JSON-serializable |
| `removed_records` | `pd.DataFrame` | Not JSON-serializable |
| `vcv_matrices` | `dict[str, np.ndarray]` | NumPy arrays not JSON-serializable |
| `overall_results.timestamp` | `datetime.datetime` | Not JSON-serializable |
| `subgroup_config.timestamp` | `datetime.datetime` | Not JSON-serializable |
| `subgroup_results.timestamp` | `datetime.datetime` | Not JSON-serializable |
| `subgroup_results.results_df` | `pd.DataFrame` | Not JSON-serializable |
| `cumulative_results` | `pd.DataFrame` | Not JSON-serializable |
| `loo_results` (nested DataFrames) | `dict` with `pd.DataFrame` | Not JSON-serializable |

### 3B. Clean Export Snippet

```python
import json
import datetime
import numpy as np
import pandas as pd


def make_json_safe(obj):
    """Recursively convert an object to JSON-serializable types."""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, pd.DataFrame):
        return None  # Skip — headless mode regenerates from CSV
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(item) for item in obj]
    if isinstance(obj, set):
        return list(obj)
    # Fallback: try str() for unknown types
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)


def export_config_for_reproducibility(analysis_config):
    """
    Create a clean JSON-serializable dictionary from ANALYSIS_CONFIG.

    Drops DataFrames and VCV matrices (regenerated from raw CSV in headless mode).
    Preserves all statistical decision keys needed to reproduce the analysis.
    """
    # Keys to explicitly drop (regenerated from data)
    DROP_KEYS = {
        'analysis_data', 'clean_dataframe', 'removed_records',
        'vcv_matrices',
        # Result keys (outputs, not inputs)
        'overall_results', 'three_level_results', 'subgroup_results',
        'meta_regression_RVE_results', 'spline_model_results',
        'funnel_results', 'trimfill_results', 'pet_peese_results',
        'cumulative_results', 'loo_results', 'loo_3level_results',
        # Text outputs
        'overall_text', 'subgroup_text', 'regression_text',
        'bias_text', 'cumulative_text',
    }

    clean = {}
    for key, value in analysis_config.items():
        if key in DROP_KEYS:
            continue
        safe_value = make_json_safe(value)
        if safe_value is not None:
            clean[key] = safe_value

    # Inject reproducibility metadata
    clean['_reproducibility'] = {
        'is_reproducing': True,
        'exported_at': datetime.datetime.now().isoformat(),
        'co_met_version': '8.0',
    }

    return clean


# --- Usage ---
# clean_config = export_config_for_reproducibility(ANALYSIS_CONFIG)
# with open('analysis_settings.json', 'w') as f:
#     json.dump(clean_config, f, indent=2)
```

---

## 4. Bypass Blueprints — `if is_reproducing` Skeletons

### 4A. Cell 3: Global Filtering

```python
# At the TOP of Cell 3, after imports:

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Skip widget UI, use config values directly ──
    if 'raw_data_standardized' not in globals():
        raise RuntimeError("Headless mode requires 'raw_data_standardized'. Load CSV first.")

    df_config = raw_data_standardized.copy()

    # Force numeric conversion (same as interactive path)
    for col in ['xe', 'sde', 'ne', 'xc', 'sdc', 'nc']:
        df_config[col] = pd.to_numeric(df_config[col], errors='coerce')

    # ANALYSIS_CONFIG already has prefilter_col, prefilter_values from JSON
    # Just store the clean_dataframe
    ANALYSIS_CONFIG['clean_dataframe'] = df_config

    print(f"[Headless] Cell 3: Loaded {len(df_config)} rows. "
          f"Pre-filter: {ANALYSIS_CONFIG.get('prefilter_col', 'None')}")

else:
    # ── INTERACTIVE: Original widget code (unchanged) ──
    # ... existing Cell 3 widget code ...
    pass
```

### 4B. Cell 4: Data Cleaning & Pre-processing

```python
# At the TOP of Cell 4, after imports and function definitions:

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Run processing with stored strategies ──
    df_config = ANALYSIS_CONFIG['clean_dataframe'].copy()

    # Ensure legacy keys exist
    if 'filterCol1' not in ANALYSIS_CONFIG:
        ANALYSIS_CONFIG['filterCol1'] = ANALYSIS_CONFIG.get('factor1', 'None')
    if 'filterCol2' not in ANALYSIS_CONFIG:
        ANALYSIS_CONFIG['filterCol2'] = ANALYSIS_CONFIG.get('factor2', 'None')

    sd_missing = ANALYSIS_CONFIG.get('sd_missing_strategy', 'median_cv')
    sd_zero = ANALYSIS_CONFIG.get('sd_zero_strategy', 'global_min')
    custom_cv = ANALYSIS_CONFIG.get('custom_cv', None)  # <-- ORPHAN now surfaced

    results = run_processing(
        df_config,
        sd_missing_strategy=sd_missing,
        sd_zero_strategy=sd_zero,
        custom_cv=custom_cv
    )

    data_filtered = results['data']
    display_processing_report(results)

    print(f"[Headless] Cell 4: {len(data_filtered)} rows after cleaning.")

else:
    # ── INTERACTIVE: Original widget code ──
    data_type_mode = globals().get('DATA_TYPE_SELECTED', 'raw')
    if data_type_mode == 'pre_calculated':
        # ... existing pre-calc skip logic ...
        pass
    else:
        # ... existing widget + button code ...
        pass
```

### 4C. Cell 5: Effect Size Selection

```python
# At the TOP of Cell 5, after imports:

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Apply stored effect size type ──
    sel = ANALYSIS_CONFIG['effect_size_type']  # From JSON

    es_configs = {
        'lnRR': {
            'effect_col': 'lnRR', 'var_col': 'var_lnRR', 'se_col': 'SE_lnRR',
            'ci_lower_col': 'CI_lower_lnRR', 'ci_upper_col': 'CI_upper_lnRR',
            'effect_label': 'log Response Ratio', 'effect_label_short': 'lnRR',
            'has_fold_change': True, 'null_value': 0, 'scale': 'log',
            'allows_negative': False
        },
        'hedges_g': {
            'effect_col': 'hedges_g', 'var_col': 'Vg', 'se_col': 'SE_g',
            'ci_lower_col': 'CI_lower_g', 'ci_upper_col': 'CI_upper_g',
            'effect_label': "Hedges' g", 'effect_label_short': 'g',
            'has_fold_change': False, 'null_value': 0, 'scale': 'standardized',
            'allows_negative': True
        },
        'cohen_d': {
            'effect_col': 'cohen_d', 'var_col': 'Vd', 'se_col': 'SE_d',
            'ci_lower_col': 'CI_lower_d', 'ci_upper_col': 'CI_upper_d',
            'effect_label': "Cohen's d", 'effect_label_short': 'd',
            'has_fold_change': False, 'null_value': 0, 'scale': 'standardized',
            'allows_negative': True
        }
    }

    ANALYSIS_CONFIG['es_config'] = es_configs[sel]
    ANALYSIS_CONFIG['data_type'] = ANALYSIS_CONFIG.get('data_type', 'raw')
    ANALYSIS_CONFIG['effect_col'] = es_configs[sel]['effect_col']
    ANALYSIS_CONFIG['var_col'] = es_configs[sel]['var_col']
    ANALYSIS_CONFIG['se_col'] = es_configs[sel]['se_col']

    print(f"[Headless] Cell 5: Effect size = {sel}")

else:
    # ── INTERACTIVE: Original recommendation + radio button UI ──
    data_type_mode = globals().get('DATA_TYPE_SELECTED', 'raw')
    # ... existing Cell 5 code ...
```

### 4D. Cell 6: Effect Size Calculation

```python
# Cell 6 currently has NO widget gate — run_calculation() runs directly.
# The bypass is minimal: just ensure it runs silently.

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Run calculation, suppress tab display ──
    run_calculation()
    # tabs are built but we skip display(tabs)
    print(f"[Headless] Cell 6: Calculated {ANALYSIS_CONFIG['effect_size_type']} "
          f"for {len(ANALYSIS_CONFIG.get('analysis_data', []))} observations.")
else:
    # ── INTERACTIVE: Original ──
    run_calculation()
    display(tabs)
```

### 4E. Cell 7: Overall Meta-Analysis

```python
# At the TOP of Cell 7, after all class definitions:

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Run analysis with stored global_settings ──
    gs = ANALYSIS_CONFIG.get('global_settings', {})

    # Create data manager & engine directly (skip UI controller)
    data_mgr = OverallDataManager(ANALYSIS_CONFIG)
    engine = OverallEngine(data_mgr)

    # Save settings to config (same as controller does)
    data_mgr.save_global_settings(
        alpha=gs.get('alpha', 0.05),
        dist_type=gs.get('dist_type', 't'),
        tau_method=gs.get('tau_method', 'REML'),
        use_kh=gs.get('use_kh', True),
        model_choice=gs.get('model_choice', 'Auto-Select (Best AIC)')
    )

    # Run analysis
    result = engine.run_analysis(
        alpha=gs.get('alpha', 0.05),
        dist_type=gs.get('dist_type', 't'),
        use_kh=gs.get('use_kh', True),
        tau_method=gs.get('tau_method', 'REML'),
        model_choice=gs.get('model_choice', 'Auto-Select (Best AIC)'),
        match_r_ll=gs.get('match_r_ll', False),
        progress_callback=lambda msg: None
    )

    # Save results
    data_mgr.save_overall_results(result)

    print(f"[Headless] Cell 7: Overall pooled effect = {result.mu_random:.4f} "
          f"(95% CI: {result.ci_lower_random:.4f}, {result.ci_upper_random:.4f})")
    print(f"  tau² = {result.tau_squared:.4f}, I² = {result.I2:.1f}%, "
          f"Best model: {result.best_model}")

else:
    # ── INTERACTIVE: Original MVC controller with tabs ──
    run_overall_meta_analysis()
```

### 4F. Cell 8 + 9: Subgroup Analysis Configuration & Execution

```python
# ── Cell 8 bypass ──

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: subgroup_config already loaded from JSON ──
    sc = ANALYSIS_CONFIG.get('subgroup_config', {})
    print(f"[Headless] Cell 8: Subgroup config loaded — "
          f"type={sc.get('analysis_type')}, "
          f"mod1={sc.get('moderator1')}, "
          f"mod2={sc.get('moderator2', 'None')}")

else:
    # ── INTERACTIVE: Original dashboard widgets ──
    # ... existing Cell 8 code ...
    pass


# ── Cell 9 bypass ──

if ANALYSIS_CONFIG.get('is_reproducing', False):
    # ── HEADLESS: Run subgroup engine directly ──
    data_mgr = SubgroupDataManager(ANALYSIS_CONFIG)
    engine = SubgroupEngine(data_mgr)  # assumes engine class exists

    results_df, metadata = engine.run_all_subgroups()
    data_mgr.save_subgroup_results(results_df, metadata)

    print(f"[Headless] Cell 9: {len(results_df)} subgroups analyzed.")

else:
    # ── INTERACTIVE: Original controller with tabs ──
    run_subgroup_analysis()
```

---

## 5. Recommended Additions to `ANALYSIS_CONFIG` for Complete Reproducibility

To eliminate all orphans, add these keys when exporting:

```python
# Add to export_config_for_reproducibility() or to the JSON manually:
ANALYSIS_CONFIG['custom_cv'] = custom_cv_input.value  # if strategy is 'custom_cv'
ANALYSIS_CONFIG['global_settings']['match_r_ll'] = match_r_ll_widget.value
ANALYSIS_CONFIG['global_settings']['zero_offset_fraction'] = 0.01  # document the constant
ANALYSIS_CONFIG['global_settings']['zero_offset_fallback'] = 0.001
ANALYSIS_CONFIG['global_settings']['reml_max_iter'] = 100
ANALYSIS_CONFIG['global_settings']['reml_tol'] = 1e-8
```

---

## 6. Summary Checklist

- [ ] Surface `custom_cv` into `ANALYSIS_CONFIG` when `sd_missing_strategy == 'custom_cv'`
- [ ] Surface `match_r_ll` into `global_settings`
- [ ] Surface `df_spline` into config for spline cell reproducibility
- [ ] Surface `trimfill_estimator`, `trimfill_side`, `trimfill_max_iter` for bias cell
- [ ] Add `is_reproducing` flag and JSON loader cell at notebook top
- [ ] Add `if/else` bypass guards to Cells 3, 4, 5, 6, 7, 8, 9
- [ ] Implement `export_config_for_reproducibility()` in export cell
- [ ] Document `zero_offset_fraction` (0.01) and `zero_offset_fallback` (0.001) as constants
