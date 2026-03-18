# Co-Met Reproducibility Plan v2: Populate, Don't Bypass

> **Strategy Change:** Instead of bypassing widgets with `if is_reproducing` guards, we
> **populate** every widget's `.value` from the loaded JSON config, then let the user
> click through normally — or press a single "Reproduce All" button.
>
> **Scope:** Analytical core (Cells 1-9, 13, 15, 17-18, 21, 24). Excludes Validation/Monte Carlo cells (26-35) and aesthetic plotting variables.

---

## 1. State Dependency Map — `ANALYSIS_CONFIG` Keys That Drive Statistics

_(Unchanged from v1 — included here for completeness.)_

### 1A. Pipeline-Configuration Keys (set by UI widgets, needed for replay)

| Key | Type | Set In | Default | Statistical Role |
|-----|------|--------|---------|-----------------|
| `prefilter_col` | `str` | Cell 3 | `'None'` | Column for global inclusion/exclusion filter |
| `prefilter_values` | `list[str]` | Cell 3 | `[]` | Which values of `prefilter_col` to **keep** |
| `factor1` | `str` | Cell 3 | `'None'` | Legacy alias for `filterCol1` |
| `factor2` | `str` | Cell 3 | `'None'` | Legacy alias for `filterCol2` |
| `min_papers` | `int` | Cell 3 | `1` | Min unique study IDs per subgroup |
| `min_obs` | `int` | Cell 3 | `1` | Min observations per subgroup |
| `sd_missing_strategy` | `str` | Cell 4 | `'median_cv'` | One of: `'nearest'`, `'median_cv'`, `'custom_cv'`, `'drop'` |
| `sd_zero_strategy` | `str` | Cell 4 | `'global_min'` | One of: `'global_min'`, `'same_as_missing'`, `'drop'` |
| `custom_cv` | `float\|None` | Cell 4 | `None` | **NEW** — CV value when `sd_missing_strategy == 'custom_cv'` |
| `effect_size_type` | `str` | Cell 5 | _(user picks)_ | One of: `'lnRR'`, `'hedges_g'`, `'cohen_d'`, `'log_or'` |
| `data_type` | `str` | Cell 5 | `'raw'` | `'raw'` or `'pre_calculated'` |
| `variance_type` | `str` | Cell 5 | `'variance'` | For pre-calc mode: `'variance'`, `'se'`, `'both'` |

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
| `global_settings.alpha` | `float` | `0.05` | Significance level |
| `global_settings.dist_type` | `str` | `'t'` | CI distribution: `'t'` or `'norm'` |
| `global_settings.tau_method` | `str` | `'REML'` | `'REML'`, `'DL'`, or `'ML'` |
| `global_settings.use_kh` | `bool` | `True` | Knapp-Hartung correction |
| `global_settings.model_choice` | `str` | `'Auto-Select (Best AIC)'` | Model selection strategy |
| `global_settings.match_r_ll` | `bool` | `False` | **NEW** — Full log-likelihood for R compat |

### 1D. Subgroup Configuration (set by Cell 8 widgets)

| Key Path | Type | Set In |
|----------|------|--------|
| `subgroup_config.analysis_type` | `str` | Cell 8 — `'single'` or `'two_way'` |
| `subgroup_config.moderator1` | `str` | Cell 8 — column name |
| `subgroup_config.moderator2` | `str\|None` | Cell 8 — column name or `None` |
| `subgroup_config.min_papers` | `int` | Cell 8 |
| `subgroup_config.min_obs` | `int` | Cell 8 |
| `subgroup_config.valid_groups_list` | `list` | Cell 8 — auto-computed |

### 1E. Downstream Cell Settings (**NEW** — surfaced orphans)

| Key Path | Type | Default | Cell | Statistical Role |
|----------|------|---------|------|-----------------|
| `spline_config.moderator_col` | `str` | _(user picks)_ | 15 | Spline moderator variable |
| `spline_config.df_spline` | `int` | `3` | 15 | Spline degrees of freedom (knot count) |
| `regression_config.moderator_col` | `str` | _(user picks)_ | 13 | Regression moderator variable |
| `bias_config.trimfill_estimator` | `str` | `'L0'` | 17 | `'L0'` or `'R0'` |
| `bias_config.trimfill_side` | `str` | `'auto'` | 17 | `'auto'`, `'left'`, `'right'` |
| `bias_config.trimfill_max_iter` | `int` | `100` | 17 | Trim-fill convergence limit |
| `pet_peese_config.p_threshold` | `float` | `0.10` | 18 | PET-PEESE switching p-value |
| `cumulative_config.sort_order` | `str` | `'ascending'` | 24 | `'ascending'` or `'descending'` |
| `cumulative_config.agg_method` | `str` | `'study'` | 24 | `'study'` or `'obs'` |
| `zero_offset_fraction` | `float` | `0.01` | 6 | Fraction of min non-zero for lnRR zeros |
| `zero_offset_fallback` | `float` | `0.001` | 6 | Fallback when all values are zero |

### 1F. Result/Output Keys (written by engines, **not** serialized)

| Key | Type | Written By |
|-----|------|-----------|
| `analysis_data` | `pd.DataFrame` | Cell 6 |
| `vcv_matrices` | `dict[str, np.ndarray]` | Cell 6 |
| `removed_records` | `pd.DataFrame` | Cell 4 |
| `overall_results` | `dict` | Cell 7 |
| `three_level_results` | `dict` | Cell 7 |
| `subgroup_results` | `dict` (with `results_df`) | Cell 9 |
| `meta_regression_RVE_results` | `dict` | Cell 13 |
| `spline_model_results` | `dict` | Cell 15 |
| `funnel_results` | `dict` | Cell 17 |
| `trimfill_results` | `dict` | Cell 17 |
| `pet_peese_results` | `dict` | Cell 18 |
| `cumulative_results` | `pd.DataFrame` | Cell 24 |
| `loo_results` | `dict` | Cell 21 |
| `clean_dataframe` | `pd.DataFrame` | Cell 3 |
| `sd_log` | `list[str]` | Cell 4 |
| Publication text keys | `str` | Cells 7, 9, 13, 17, 24 |

---

## 2. Analytical Orphans — Variables Trapped Outside `ANALYSIS_CONFIG`

### 2A. High Priority (directly affect numerical results)

| Orphan Variable | Current Value | Location | Resolution |
|----------------|---------------|----------|------------|
| `custom_cv` | User float / fallback `0.1` | Cell 4, `custom_cv_input` widget | **Add to root** `ANALYSIS_CONFIG['custom_cv']` |
| `zero_offset_fraction` | `0.01` (hardcoded) | Cell 6, `run_calculation()` ~L252 | **Add to root** `ANALYSIS_CONFIG['zero_offset_fraction']` |
| `zero_offset_fallback` | `0.001` (hardcoded) | Cell 6, `run_calculation()` ~L253 | **Add to root** `ANALYSIS_CONFIG['zero_offset_fallback']` |
| `match_r_ll` | `False` (widget) | Cell 7, `match_r_ll_widget` | **Add to** `global_settings.match_r_ll` |
| `df_spline` | User-selected int | Cell 15, `self.df_slider` | **Add to** `spline_config.df_spline` |
| `spline_moderator` | User-selected str | Cell 15, `self.mod_dropdown` | **Add to** `spline_config.moderator_col` |
| `regression_moderator` | User-selected str | Cell 13, `self.moderator_widget` | **Add to** `regression_config.moderator_col` |
| `trimfill_estimator` | `'L0'` (hardcoded) | Cell 17, `run_trimfill_analysis()` | **Add to** `bias_config.trimfill_estimator` |
| `trimfill_side` | `'auto'` (hardcoded) | Cell 17, `run_trimfill_analysis()` | **Add to** `bias_config.trimfill_side` |
| `trimfill_max_iter` | `100` (hardcoded) | Cell 17, `run_trimfill_analysis()` | **Add to** `bias_config.trimfill_max_iter` |
| `p_threshold` | `0.10` (widget) | Cell 18, `self.p_threshold_widget` | **Add to** `pet_peese_config.p_threshold` |
| `sort_order` | `'ascending'` (widget) | Cell 24, `self.sort_order_widget` | **Add to** `cumulative_config.sort_order` |
| `agg_method` | `'study'` (widget) | Cell 24, `self.agg_method_widget` | **Add to** `cumulative_config.agg_method` |

### 2B. Medium Priority (optimizer internals — affect convergence, rarely results)

| Orphan Variable | Current Value | Location |
|----------------|---------------|----------|
| `reml_max_iter` | `100` | Cell 1, `calculate_tau_squared_REML()` |
| `reml_tol` | `1e-8` | Cell 1, `calculate_tau_squared_REML()` |
| `ml_max_iter` / `ml_tol` | `100` / `1e-8` | Cell 1, `calculate_tau_squared_ML()` |
| `pm_max_iter` / `pm_tol` | `100` / `1e-8` | Cell 1, `calculate_tau_squared_PM()` |
| `3level_optimizer_ftol` | `1e-11` to `1e-12` | Cell 1 & 7, L-BFGS-B options |
| `3level_start_points` | `[[0.01,0.01],[0.5,0.1],...]` | Cell 1, `run_python_3level()` |
| `3level_param_bounds` | `[1e-8, 50.0]` / `[1e-8, None]` | Cell 1 & 7 |
| `ridge_jitter` | `1e-6` | Cell 1, Cholesky fallback |

> **Decision:** Medium-priority orphans are documented in the JSON under
> `_optimizer_defaults` for transparency but are NOT connected to widgets.
> They are frozen constants, not user decisions.

### 2C. Low Priority (derived/auto-computed)

| Orphan Variable | Current Value | Location |
|----------------|---------------|----------|
| `min_sd_fallback` | `0.001` | Cell 4, `run_processing()` |
| `DATA_TYPE_SELECTED` | `'raw'` | Cell 2 global |
| `VARIANCE_TYPE_SELECTED` | `'variance'` | Cell 2 global |

---

## 3. Serialization Audit — Data Embedding Strategy

### 3A. Key Change: Embed `clean_dataframe` as CSV String

The v1 plan dropped all DataFrames. The v2 plan **embeds** the `clean_dataframe`
as a CSV string inside the JSON under `embedded_data`. This means reviewers only
need the single `.json` file to reproduce — no separate CSV required.

### 3B. Non-JSON-Serializable Keys

| Key | Type | Resolution |
|-----|------|-----------|
| `clean_dataframe` | `pd.DataFrame` | **Embed** as CSV string under `embedded_data` |
| `analysis_data` | `pd.DataFrame` | Skip — regenerated by Cells 4-6 |
| `removed_records` | `pd.DataFrame` | Skip — regenerated by Cell 4 |
| `vcv_matrices` | `dict[str, np.ndarray]` | Skip — regenerated by Cell 6 |
| `overall_results.timestamp` | `datetime` | Convert to ISO string |
| `subgroup_config.timestamp` | `datetime` | Convert to ISO string |
| `subgroup_results` | `dict` with DataFrame | Skip — regenerated by Cell 9 |
| `cumulative_results` | `pd.DataFrame` | Skip — regenerated by Cell 24 |
| `loo_results` | `dict` with DataFrame | Skip — regenerated by Cell 21 |

### 3C. Export Function (with Data Embedding)

```python
import json
import datetime
import io
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
        return None  # Handled separately via embedded_data
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [make_json_safe(item) for item in obj]
    if isinstance(obj, set):
        return sorted(list(obj))
    try:
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        return str(obj)


def export_config_for_reproducibility(analysis_config):
    """
    Create a JSON-serializable dictionary from ANALYSIS_CONFIG.

    Key difference from v1: clean_dataframe is EMBEDDED as a CSV string
    under 'embedded_data', not dropped.

    Returns:
        dict: JSON-safe config ready for json.dump()
    """
    # Keys that are OUTPUTS (regenerated by the pipeline)
    RESULT_KEYS = {
        'analysis_data', 'removed_records', 'vcv_matrices',
        'overall_results', 'three_level_results', 'subgroup_results',
        'meta_regression_RVE_results', 'spline_model_results',
        'funnel_results', 'trimfill_results', 'pet_peese_results',
        'cumulative_results', 'loo_results', 'loo_3level_results',
        'overall_text', 'subgroup_text', 'regression_text',
        'bias_text', 'cumulative_text', 'cumulative_metadata',
    }

    clean = {}

    # --- 1. Embed the clean_dataframe as CSV ---
    df = analysis_config.get('clean_dataframe')
    if df is not None and isinstance(df, pd.DataFrame):
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        clean['embedded_data'] = csv_buffer.getvalue()

    # --- 2. Copy all INPUT keys (skip results and the raw DataFrame) ---
    SKIP_KEYS = RESULT_KEYS | {'clean_dataframe'}
    for key, value in analysis_config.items():
        if key in SKIP_KEYS:
            continue
        safe_value = make_json_safe(value)
        if safe_value is not None:
            clean[key] = safe_value

    # --- 3. Surface orphans that the current code doesn't store ---
    # These should be written to ANALYSIS_CONFIG BEFORE calling this function.
    # This block sets safe defaults if they were missed.
    clean.setdefault('custom_cv', None)
    clean.setdefault('zero_offset_fraction', 0.01)
    clean.setdefault('zero_offset_fallback', 0.001)

    gs = clean.setdefault('global_settings', {})
    gs.setdefault('match_r_ll', False)

    clean.setdefault('spline_config', {
        'moderator_col': None,
        'df_spline': 3
    })
    clean.setdefault('regression_config', {
        'moderator_col': None
    })
    clean.setdefault('bias_config', {
        'trimfill_estimator': 'L0',
        'trimfill_side': 'auto',
        'trimfill_max_iter': 100
    })
    clean.setdefault('pet_peese_config', {
        'p_threshold': 0.10
    })
    clean.setdefault('cumulative_config', {
        'sort_order': 'ascending',
        'agg_method': 'study'
    })

    # --- 4. Optimizer defaults (documented, not widget-linked) ---
    clean['_optimizer_defaults'] = {
        'reml_max_iter': 100,
        'reml_tol': 1e-8,
        'ml_max_iter': 100,
        'ml_tol': 1e-8,
        'pm_max_iter': 100,
        'pm_tol': 1e-8,
        '3level_optimizer_ftol': 1e-11,
        '3level_start_points': [[0.01,0.01],[0.5,0.1],[0.1,0.5],[0.001,0.001]],
        '3level_param_lower_bound': 1e-8,
        'ridge_jitter': 1e-6
    }

    # --- 5. Reproducibility metadata ---
    clean['_reproducibility'] = {
        'is_reproducing': True,
        'exported_at': datetime.datetime.now().isoformat(),
        'co_met_version': '8.0',
        'strategy': 'populate_widgets',
    }

    return clean


# --- Usage (add to your Export cell) ---
# clean_config = export_config_for_reproducibility(ANALYSIS_CONFIG)
# with open('analysis_settings.json', 'w') as f:
#     json.dump(clean_config, f, indent=2)
# print(f"Exported {len(clean_config)} keys to analysis_settings.json")
```

---

## 4. Auto-Loader — Cell 1 JSON Upload & Data Hydration

Add this block at the **end of Cell 1** (after all function definitions, before
the authentication banner). When a user uploads a JSON settings file, it:
1. Parses the JSON into `ANALYSIS_CONFIG`
2. If `embedded_data` exists, converts the CSV string back to a DataFrame
3. Sets `is_reproducing = True` so downstream populate functions activate

```python
# =============================================================================
# REPRODUCIBILITY: JSON CONFIG LOADER (end of Cell 1)
# =============================================================================

import json
import io

def load_reproducibility_config(json_path_or_bytes):
    """
    Load a previously exported analysis_settings.json.

    Args:
        json_path_or_bytes: File path (str) or bytes from upload widget

    Returns:
        dict: Hydrated ANALYSIS_CONFIG with embedded data restored
    """
    # --- 1. Parse JSON ---
    if isinstance(json_path_or_bytes, bytes):
        config = json.loads(json_path_or_bytes.decode('utf-8'))
    elif isinstance(json_path_or_bytes, str):
        with open(json_path_or_bytes, 'r') as f:
            config = json.load(f)
    else:
        raise TypeError(f"Expected str or bytes, got {type(json_path_or_bytes)}")

    # --- 2. Hydrate embedded_data -> clean_dataframe ---
    if 'embedded_data' in config:
        csv_string = config.pop('embedded_data')
        df = pd.read_csv(io.StringIO(csv_string))
        config['clean_dataframe'] = df

        # Also make it available as the raw_data_standardized global
        # so Cell 3/4 can find it without running Cell 2
        globals()['raw_data_standardized'] = df.copy()
        globals()['DATA_TYPE_SELECTED'] = config.get('data_type', 'raw')

        print(f"  Hydrated embedded data: {len(df)} rows, {len(df.columns)} columns")

    # --- 3. Set the reproducing flag ---
    config['is_reproducing'] = True

    return config


# --- Upload Widget ---
_repro_upload = widgets.FileUpload(
    accept='.json',
    multiple=False,
    description='Load Settings JSON',
    layout=widgets.Layout(width='300px')
)
_repro_output = widgets.Output()

def _on_repro_upload(change):
    with _repro_output:
        clear_output()
        uploaded = change['new']
        if not uploaded:
            return
        # ipywidgets v8+: uploaded is a tuple of dicts
        file_info = uploaded[0] if isinstance(uploaded, (list, tuple)) else list(uploaded.values())[0]
        content = file_info['content'] if isinstance(file_info, dict) else file_info

        try:
            global ANALYSIS_CONFIG
            ANALYSIS_CONFIG = load_reproducibility_config(content)

            meta = ANALYSIS_CONFIG.get('_reproducibility', {})
            print("=" * 60)
            print("REPRODUCIBILITY MODE ACTIVATED")
            print("=" * 60)
            print(f"  Exported at:    {meta.get('exported_at', 'unknown')}")
            print(f"  Co-Met version: {meta.get('co_met_version', 'unknown')}")
            print(f"  Effect size:    {ANALYSIS_CONFIG.get('effect_size_type', 'unknown')}")
            print(f"  Data type:      {ANALYSIS_CONFIG.get('data_type', 'unknown')}")
            print()
            print("All widgets will be pre-populated with the loaded settings.")
            print("Run each cell to verify, or click 'Reproduce All' (Cell 1).")

        except Exception as e:
            print(f"ERROR loading config: {e}")
            import traceback
            traceback.print_exc()

_repro_upload.observe(_on_repro_upload, names='value')

# --- Reproduce All Button ---
_btn_reproduce_all = widgets.Button(
    description='Reproduce All',
    button_style='warning',
    icon='play',
    layout=widgets.Layout(width='300px', height='45px'),
    disabled=True  # Enabled only after successful JSON load
)
_repro_all_output = widgets.Output()

def _on_reproduce_all(b):
    """Execute all analytical cells in sequence."""
    with _repro_all_output:
        clear_output()
        if not ANALYSIS_CONFIG.get('is_reproducing', False):
            print("ERROR: Load a settings JSON first.")
            return

        print("Executing full pipeline...")
        # Uses IPython's run_cell to execute cells by their tag/title.
        # This is a skeleton — actual implementation depends on notebook runner.
        from IPython import get_ipython
        ip = get_ipython()

        cell_sequence = [
            ("Cell 3: Global Filtering", 3),
            ("Cell 4: Data Cleaning", 4),
            ("Cell 5: Effect Size Selection", 5),
            ("Cell 6: Effect Size Calculation", 6),
            ("Cell 7: Overall Meta-Analysis", 7),
            ("Cell 8: Subgroup Config", 8),
            ("Cell 9: Subgroup Analysis", 9),
            ("Cell 13: Meta-Regression", 13),
            ("Cell 15: Spline Analysis", 15),
            ("Cell 17: Publication Bias", 17),
            ("Cell 18: PET-PEESE", 18),
            ("Cell 21: Leave-One-Out", 21),
            ("Cell 24: Cumulative", 24),
        ]

        for name, idx in cell_sequence:
            try:
                print(f"  Running {name}...", end=" ")
                # Execute the cell by index
                ip.run_cell(
                    ip.user_ns.get('In', [''])[idx]
                    if idx < len(ip.user_ns.get('In', []))
                    else ''
                )
                print("Done")
            except Exception as e:
                print(f"FAILED: {e}")
                break

        print("\nPipeline complete.")

_btn_reproduce_all.on_click(_on_reproduce_all)

# Enable the button after a successful upload
def _enable_reproduce_button(*args):
    if ANALYSIS_CONFIG.get('is_reproducing', False):
        _btn_reproduce_all.disabled = False

_repro_upload.observe(_enable_reproduce_button, names='value')

# --- Display ---
display(widgets.HTML("""
<div style='background:#e8f4f8; border-left:5px solid #17a2b8; padding:15px;
     border-radius:5px; margin:15px 0;'>
  <h4 style='margin-top:0; color:#0c5460;'>Reproducibility Mode (Optional)</h4>
  <p style='color:#0c5460; margin-bottom:5px;'>
    Upload a previously exported <code>analysis_settings.json</code> to
    pre-populate all widgets and reproduce the exact analysis.
  </p>
</div>
"""))
display(widgets.HBox([_repro_upload, _btn_reproduce_all]))
display(_repro_output)
display(_repro_all_output)
```

---

## 5. The Populate Strategy — Per-Cell Widget Population Functions

### 5A. Design Principle

Every cell that contains ipywidgets gets a **`_populate_from_config()`** function
injected at the **bottom**, after all widgets are created but before `display()`.
The function:

1. Checks `ANALYSIS_CONFIG.get('is_reproducing', False)`
2. If `True`, sets each widget's `.value` to match the stored config
3. Unobserves → sets value → re-observes (to avoid triggering callbacks during population)
4. The cell still displays normally — the user sees the widgets pre-filled

### 5B. Helper: Safe Widget Setter

```python
# Add to Cell 1, after imports:

def _safe_set_widget(widget, value, observer_fn=None, observer_name='value'):
    """
    Set a widget's value without triggering its observer.

    Args:
        widget: ipywidgets widget instance
        value: Value to set
        observer_fn: Observer function to temporarily detach (optional)
        observer_name: Name of the trait being observed (default 'value')
    """
    if value is None:
        return
    try:
        # Temporarily detach observer
        if observer_fn is not None:
            widget.unobserve(observer_fn, names=observer_name)

        # Set the value
        widget.value = value

        # Reattach observer
        if observer_fn is not None:
            widget.observe(observer_fn, names=observer_name)
    except Exception:
        # If value is not in options, skip silently
        pass
```

### 5C. Cell 3 — Global Filtering

**Widgets:** `dd_prefilter_mod`, checkbox children in `vbox_prefilter_values`, `btn_save_config`

```python
# Insert AFTER widget creation, BEFORE display():

def _populate_cell3():
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    # 1. Set prefilter dropdown
    target_col = ANALYSIS_CONFIG.get('prefilter_col', 'None')
    _safe_set_widget(dd_prefilter_mod, target_col, on_prefilter_change)

    # 2. Trigger checkbox generation (simulates the dropdown change)
    on_prefilter_change({'new': target_col})

    # 3. Set checkbox values to match prefilter_values
    kept = set(ANALYSIS_CONFIG.get('prefilter_values', []))
    if target_col != 'None' and kept:
        for cb in vbox_prefilter_values.children[1:]:  # skip HTML label
            val_name = cb.description.rsplit(' (n=', 1)[0]
            cb.value = (val_name in kept)

    print(f"[Reproduce] Cell 3 populated: prefilter={target_col}")

_populate_cell3()
```

### 5D. Cell 4 — Data Cleaning & Pre-processing

**Widgets:** `dd_missing_strategy`, `dd_zero_strategy`, `custom_cv_input`, `btn_process`

```python
# Insert AFTER widget creation, BEFORE display():

def _populate_cell4():
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    # These widgets only exist if has_missing / has_zeros are True
    # Use try/except since they may not be in scope
    try:
        sd_missing = ANALYSIS_CONFIG.get('sd_missing_strategy', 'median_cv')
        _safe_set_widget(dd_missing_strategy, sd_missing, on_missing_change)

        # If custom_cv strategy, also set the float input
        if sd_missing == 'custom_cv':
            cv_val = ANALYSIS_CONFIG.get('custom_cv', 0.1)
            custom_cv_input.value = cv_val
            custom_cv_input.layout.display = 'block'
    except NameError:
        pass  # No missing SDs in data => widget not created

    try:
        sd_zero = ANALYSIS_CONFIG.get('sd_zero_strategy', 'global_min')
        _safe_set_widget(dd_zero_strategy, sd_zero, on_zero_change)
    except NameError:
        pass  # No zero SDs in data => widget not created

    print(f"[Reproduce] Cell 4 populated: missing={ANALYSIS_CONFIG.get('sd_missing_strategy')}, "
          f"zeros={ANALYSIS_CONFIG.get('sd_zero_strategy')}")

_populate_cell4()
```

### 5E. Cell 5 — Effect Size Selection

**Widgets (raw mode):** `effect_size_widget` (RadioButtons), `proceed_button`
**Widgets (pre-calc mode):** `es_type_dropdown` (Dropdown), `confirm_button`

```python
# Insert AFTER widget creation, BEFORE display():

def _populate_cell5():
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    es_type = ANALYSIS_CONFIG.get('effect_size_type')
    if es_type is None:
        return

    data_mode = ANALYSIS_CONFIG.get('data_type', 'raw')
    if data_mode == 'raw':
        try:
            _safe_set_widget(effect_size_widget, es_type)
        except NameError:
            pass
    else:
        try:
            _safe_set_widget(es_type_dropdown, es_type)
        except NameError:
            pass

    print(f"[Reproduce] Cell 5 populated: effect_size_type={es_type}")

_populate_cell5()
```

### 5F. Cell 6 — Effect Size Calculation

Cell 6 has **no user-facing decision widgets** (it uses output tabs only).
However, we need to consume the new orphan keys:

```python
# Insert at the TOP of run_calculation(), inside the lnRR zero-handling block:

def _populate_cell6():
    """Read orphan constants from ANALYSIS_CONFIG if present."""
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    # These will be read by the lnRR zero-handling code below
    global _zero_offset_fraction, _zero_offset_fallback
    _zero_offset_fraction = ANALYSIS_CONFIG.get('zero_offset_fraction', 0.01)
    _zero_offset_fallback = ANALYSIS_CONFIG.get('zero_offset_fallback', 0.001)

_populate_cell6()

# Then MODIFY the existing zero-handling code (line ~252) to use these:
# BEFORE:  offset = (min_nonzero * 0.01) if pd.notna(min_nonzero) else 0.001
# AFTER:   offset = (min_nonzero * _zero_offset_fraction) if pd.notna(min_nonzero) else _zero_offset_fallback
```

### 5G. Cell 7 — Overall Meta-Analysis (Controller)

**Widgets (on `OverallController` instance):**
`alpha_widget`, `model_selector`, `tau_method_widget`, `use_kh_widget`,
`ci_dist_widget`, `match_r_ll_widget`

The populate must happen **after** the controller is created but **before**
`run_analysis()`. Modify the `run_overall_meta_analysis()` entry point:

```python
# MODIFY run_overall_meta_analysis() — add populate call after controller creation:

def run_overall_meta_analysis():
    try:
        if 'ANALYSIS_CONFIG' not in globals():
            print("ERROR: ANALYSIS_CONFIG not found")
            return

        controller = OverallController(ANALYSIS_CONFIG)

        # --- POPULATE WIDGETS FROM CONFIG ---
        _populate_cell7(controller)

        display(controller.view.tabs)
        controller.run_analysis()
        globals()['_overall_controller'] = controller

    except Exception as e:
        print(f"Fatal Error: {type(e).__name__}: {str(e)}")
        traceback.print_exc()


def _populate_cell7(controller):
    """Pre-fill Overall Meta-Analysis widgets from stored global_settings."""
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    gs = ANALYSIS_CONFIG.get('global_settings', {})

    _safe_set_widget(controller.alpha_widget,
                     gs.get('alpha', 0.05),
                     controller._handle_settings_change)
    _safe_set_widget(controller.tau_method_widget,
                     gs.get('tau_method', 'REML'),
                     controller._handle_settings_change)
    _safe_set_widget(controller.use_kh_widget,
                     gs.get('use_kh', True),
                     controller._handle_settings_change)
    _safe_set_widget(controller.ci_dist_widget,
                     gs.get('dist_type', 't'),
                     controller._handle_settings_change)
    _safe_set_widget(controller.model_selector,
                     gs.get('model_choice', 'Auto-Select (Best AIC)'),
                     controller._handle_settings_change)
    _safe_set_widget(controller.match_r_ll_widget,
                     gs.get('match_r_ll', False),
                     controller._handle_settings_change)

    print(f"[Reproduce] Cell 7 populated: alpha={gs.get('alpha')}, "
          f"tau={gs.get('tau_method')}, KH={gs.get('use_kh')}, "
          f"dist={gs.get('dist_type')}, model={gs.get('model_choice')}")
```

### 5H. Cell 8 — Subgroup Configuration

**Widgets:** `analysis_type_widget`, `moderator1_widget`, `moderator2_widget`,
`min_papers_widget`, `min_obs_widget`, `run_button`

```python
# Insert AFTER initialize_configuration() returns, BEFORE display(tabs):

def _populate_cell8():
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    sc = ANALYSIS_CONFIG.get('subgroup_config', {})
    if not sc:
        return

    # 1. Analysis type
    _safe_set_widget(analysis_type_widget,
                     sc.get('analysis_type', 'single'),
                     update_all_tabs)

    # 2. Moderator 1
    if moderator1_widget is not None:
        _safe_set_widget(moderator1_widget,
                         sc.get('moderator1'),
                         update_all_tabs)

    # 3. Moderator 2
    if moderator2_widget is not None and sc.get('moderator2'):
        _safe_set_widget(moderator2_widget,
                         sc.get('moderator2'),
                         update_all_tabs)

    # 4. Thresholds
    _safe_set_widget(min_papers_widget,
                     sc.get('min_papers', 3),
                     update_thresholds_tab)
    _safe_set_widget(min_obs_widget,
                     sc.get('min_obs', 5),
                     update_thresholds_tab)

    # 5. Refresh tabs with new values
    update_all_tabs()

    print(f"[Reproduce] Cell 8 populated: type={sc.get('analysis_type')}, "
          f"mod1={sc.get('moderator1')}, mod2={sc.get('moderator2')}")

_populate_cell8()
```

### 5I. Cell 9 — Subgroup Analysis Execution

Cell 9 has no user-facing **decision** widgets (only output tabs + run button).
The run button's callback reads from `ANALYSIS_CONFIG['subgroup_config']`, which
was saved by Cell 8's `save_configuration()`. No populate needed — the config
is already loaded from the JSON.

### 5J. Cell 13 — Meta-Regression

**Widgets (on `RegressionController`):** `self.moderator_widget`, `self.run_button`

```python
# Inside the RegressionController class or after its instantiation:

def _populate_cell13(controller):
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    rc = ANALYSIS_CONFIG.get('regression_config', {})
    mod_col = rc.get('moderator_col')
    if mod_col and hasattr(controller, 'moderator_widget'):
        _safe_set_widget(controller.moderator_widget, mod_col)

    print(f"[Reproduce] Cell 13 populated: moderator={mod_col}")
```

### 5K. Cell 15 — Spline Analysis

**Widgets (on Spline View):** `self.mod_dropdown`, `self.df_slider`

```python
def _populate_cell15(view):
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    sc = ANALYSIS_CONFIG.get('spline_config', {})

    if sc.get('moderator_col') and hasattr(view, 'mod_dropdown'):
        _safe_set_widget(view.mod_dropdown, sc['moderator_col'])

    if sc.get('df_spline') and hasattr(view, 'df_slider'):
        _safe_set_widget(view.df_slider, sc['df_spline'])

    print(f"[Reproduce] Cell 15 populated: moderator={sc.get('moderator_col')}, "
          f"df_spline={sc.get('df_spline')}")
```

### 5L. Cell 17 — Publication Bias (Egger's & Trim-Fill)

Cell 17's `run_trimfill_analysis()` takes `estimator`, `side`, and `max_iter`
as **function arguments**, not widget values. The populate strategy here is to
modify the function call site to read from config:

```python
# MODIFY the trim-fill call site in the controller to read from bias_config:

def _get_trimfill_params():
    """Read trim-fill parameters from ANALYSIS_CONFIG if reproducing."""
    bc = ANALYSIS_CONFIG.get('bias_config', {})
    return {
        'estimator': bc.get('trimfill_estimator', 'L0'),
        'side': bc.get('trimfill_side', 'auto'),
        'max_iter': bc.get('trimfill_max_iter', 100),
    }

# Then in the controller's run method, replace:
#   self.run_trimfill_analysis()
# with:
#   params = _get_trimfill_params()
#   self.run_trimfill_analysis(**params)
```

### 5M. Cell 18 — PET-PEESE

**Widget:** `self.p_threshold_widget` (FloatSlider)

```python
def _populate_cell18(controller):
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    pc = ANALYSIS_CONFIG.get('pet_peese_config', {})
    p_thresh = pc.get('p_threshold')
    if p_thresh is not None and hasattr(controller, 'p_threshold_widget'):
        _safe_set_widget(controller.p_threshold_widget, p_thresh)

    print(f"[Reproduce] Cell 18 populated: p_threshold={p_thresh}")
```

### 5N. Cell 21 — Leave-One-Out Sensitivity

Cell 21 has **no decision widgets** — only a run button and progress bar.
No populate needed.

### 5O. Cell 24 — Cumulative Meta-Analysis

**Widgets:** `self.sort_order_widget`, `self.agg_method_widget`

```python
def _populate_cell24(controller):
    if not ANALYSIS_CONFIG.get('is_reproducing', False):
        return

    cc = ANALYSIS_CONFIG.get('cumulative_config', {})

    if hasattr(controller, 'sort_order_widget'):
        _safe_set_widget(controller.sort_order_widget,
                         cc.get('sort_order', 'ascending'))

    if hasattr(controller, 'agg_method_widget'):
        _safe_set_widget(controller.agg_method_widget,
                         cc.get('agg_method', 'study'))

    print(f"[Reproduce] Cell 24 populated: sort={cc.get('sort_order')}, "
          f"agg={cc.get('agg_method')}")
```

---

## 6. Orphan Sync — Surfacing Hardcoded Values to UI

For orphans that have a corresponding text/widget in the UI, we both **store**
them in `ANALYSIS_CONFIG` at export time AND **populate** them at load time.

### 6A. Orphans with Existing Widgets (populate on load)

| Orphan | Widget | Populate Target |
|--------|--------|----------------|
| `custom_cv` | `custom_cv_input` (BoundedFloatText) | Cell 4 `_populate_cell4()` |
| `match_r_ll` | `match_r_ll_widget` (Checkbox) | Cell 7 `_populate_cell7()` |
| `df_spline` | `self.df_slider` (IntSlider) | Cell 15 `_populate_cell15()` |
| `p_threshold` | `self.p_threshold_widget` (FloatSlider) | Cell 18 `_populate_cell18()` |
| `sort_order` | `self.sort_order_widget` (Dropdown) | Cell 24 `_populate_cell24()` |
| `agg_method` | `self.agg_method_widget` (Dropdown) | Cell 24 `_populate_cell24()` |

### 6B. Orphans WITHOUT Widgets (stored in JSON, consumed by code)

| Orphan | JSON Key | Consumed By |
|--------|----------|-------------|
| `zero_offset_fraction` | `ANALYSIS_CONFIG['zero_offset_fraction']` | Cell 6 lnRR zero-handling |
| `zero_offset_fallback` | `ANALYSIS_CONFIG['zero_offset_fallback']` | Cell 6 lnRR zero-handling |
| `trimfill_estimator` | `bias_config.trimfill_estimator` | Cell 17 `run_trimfill_analysis()` |
| `trimfill_side` | `bias_config.trimfill_side` | Cell 17 `run_trimfill_analysis()` |
| `trimfill_max_iter` | `bias_config.trimfill_max_iter` | Cell 17 `run_trimfill_analysis()` |

> These have no UI widgets today. If a reviewer wants to change them, they edit
> the JSON directly or we add widgets in a future version.

### 6C. Required Code Changes to Store Orphans at Export Time

Before calling `export_config_for_reproducibility()`, each cell's "Save" callback
must write its orphans into `ANALYSIS_CONFIG`:

```python
# Cell 4: In on_process_clicked(), after run_processing():
ANALYSIS_CONFIG['custom_cv'] = custom_cv_input.value if has_missing else None

# Cell 6: In run_calculation(), after zero-offset is computed:
ANALYSIS_CONFIG['zero_offset_fraction'] = 0.01  # document the constant used
ANALYSIS_CONFIG['zero_offset_fallback'] = 0.001

# Cell 7: In OverallController.run_analysis(), after reading widget values:
ANALYSIS_CONFIG['global_settings']['match_r_ll'] = self.match_r_ll_widget.value

# Cell 13: After moderator selection:
ANALYSIS_CONFIG['regression_config'] = {'moderator_col': self.moderator_widget.value}

# Cell 15: After run:
ANALYSIS_CONFIG['spline_config'] = {
    'moderator_col': self.view.mod_dropdown.value,
    'df_spline': self.view.df_slider.value
}

# Cell 17: After trim-fill runs (in the controller):
ANALYSIS_CONFIG['bias_config'] = {
    'trimfill_estimator': 'L0',
    'trimfill_side': tf_results.get('side', 'auto'),
    'trimfill_max_iter': 100
}

# Cell 18: After PET-PEESE runs:
ANALYSIS_CONFIG['pet_peese_config'] = {'p_threshold': self.p_threshold_widget.value}

# Cell 24: After cumulative runs:
ANALYSIS_CONFIG['cumulative_config'] = {
    'sort_order': self.sort_order_widget.value,
    'agg_method': self.agg_method_widget.value
}
```

---

## 7. User Flow

### 7A. Normal (Interactive) Flow — No Change

1. User runs Cell 1 (setup) — sees the upload widget but ignores it
2. User proceeds through Cells 2-24 interactively
3. At the end, user clicks "Export Settings" to generate `analysis_settings.json`

### 7B. Reproduce Flow

1. User runs Cell 1 (setup)
2. User uploads `analysis_settings.json` via the file upload widget
3. Auto-loader hydrates `ANALYSIS_CONFIG` + restores the DataFrame
4. A banner confirms: *"Reproducibility Mode Activated — all widgets will be pre-populated"*
5. **Option A (Step-by-Step):** User clicks through each cell normally. Every widget
   is pre-filled. The user can inspect, verify, and optionally tweak before clicking
   the cell's "Run" / "Confirm" button.
6. **Option B (One-Click):** User clicks "Reproduce All" in Cell 1. This
   programmatically executes all analytical cells in sequence. Each cell's widgets
   are populated, buttons are programmatically clicked, and results accumulate.

### 7C. Reproduce All — Button Click Simulation

The "Reproduce All" handler needs to **programmatically click** each cell's
confirm/run button after populating. Here's the pattern:

```python
# Inside _on_reproduce_all(), after running each cell:

# Cell 3: click save
btn_save_config.click()

# Cell 4: click process (if widgets exist)
try:
    btn_process.click()
except NameError:
    pass

# Cell 5: click confirm
try:
    proceed_button.click()  # raw mode
except NameError:
    try:
        confirm_button.click()  # pre-calc mode
    except NameError:
        pass

# Cell 7: controller auto-runs on creation (no explicit click needed)
# Cell 8: click save config
run_button.click()

# Cell 9, 13, 15, 17, 18, 21, 24:
# Their controllers run on creation or have a run_button to click
```

---

## 8. Implementation Checklist

### Phase 1: Infrastructure (Cell 1)
- [ ] Add `_safe_set_widget()` helper function
- [ ] Add `load_reproducibility_config()` function
- [ ] Add upload widget + "Reproduce All" button to Cell 1 UI
- [ ] Add `export_config_for_reproducibility()` to the export cell

### Phase 2: Store Orphans (write to `ANALYSIS_CONFIG`)
- [ ] Cell 4: Store `custom_cv` after processing
- [ ] Cell 6: Store `zero_offset_fraction` and `zero_offset_fallback`
- [ ] Cell 7: Store `match_r_ll` in `global_settings`
- [ ] Cell 13: Store `regression_config.moderator_col`
- [ ] Cell 15: Store `spline_config.moderator_col` and `spline_config.df_spline`
- [ ] Cell 17: Store `bias_config.*` after trim-fill runs
- [ ] Cell 18: Store `pet_peese_config.p_threshold`
- [ ] Cell 24: Store `cumulative_config.sort_order` and `.agg_method`

### Phase 3: Populate Functions (one per cell)
- [ ] Cell 3: `_populate_cell3()` — dropdown + checkboxes
- [ ] Cell 4: `_populate_cell4()` — SD strategy dropdowns + custom CV input
- [ ] Cell 5: `_populate_cell5()` — effect size radio/dropdown
- [ ] Cell 6: `_populate_cell6()` — zero-offset constants
- [ ] Cell 7: `_populate_cell7(controller)` — all 6 settings widgets
- [ ] Cell 8: `_populate_cell8()` — moderators + thresholds
- [ ] Cell 13: `_populate_cell13(controller)` — moderator dropdown
- [ ] Cell 15: `_populate_cell15(view)` — moderator + df_spline slider
- [ ] Cell 17: `_get_trimfill_params()` — inject into function call
- [ ] Cell 18: `_populate_cell18(controller)` — p_threshold slider
- [ ] Cell 24: `_populate_cell24(controller)` — sort + aggregation

### Phase 4: Reproduce All
- [ ] Wire "Reproduce All" to execute cells sequentially
- [ ] Programmatically click confirm/run buttons in each cell
- [ ] Add progress indicator

### Phase 5: Testing
- [ ] Export a settings JSON from a full interactive run
- [ ] Load the JSON in a fresh notebook and verify all widgets are pre-filled
- [ ] Click "Reproduce All" and verify results match the original
- [ ] Verify that editing a pre-filled widget and re-running produces different results
