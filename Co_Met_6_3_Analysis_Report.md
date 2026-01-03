# Comprehensive Analysis Report: Co_Met_6_3.ipynb

**Generated:** 2026-01-03
**Notebook Version:** Co_Met_6_3.ipynb
**Total Size:** 976.2 KB

---

## 1. Overall Structure

### Cell Composition
- **Total Cells:** 26
  - Code Cells: 25 (96%)
  - Markdown Cells: 1 (4% - Colab badge only)
- **Total Lines of Code:** ~24,940
- **Total Characters:** ~964,111
- **Average Cell Size:** ~997 lines per cell (⚠️ **Very Large**)

### Logical Sections/Workflow Stages

The notebook follows a **layered MVC architecture** with 24 distinct analytical components:

#### **Phase 1: Setup & Data Ingestion (Cells 1-4)**
1. ⚙️ Environment Setup & Core Functions
2. ⚙️ Data Ingestion & Column Mapping
3. ⚙️ Global Filtering
4. ⚙️ Data Cleaning & Pre-processing

#### **Phase 2: Effect Size Computation (Cells 5-6)**
5. 🔬 Effect Size Selection & Diagnostics
6. 🧮 Effect Size Calculation

#### **Phase 3: Meta-Analysis Models (Cells 7-9)**
7. 📊 Overall Meta-Analysis (3 parts: Data/Analysis/Presentation)
8. ⚙️ Subgroup Analysis Configuration
9. 🔬 Subgroup Analysis (3 parts: Data/Analysis/Presentation)

#### **Phase 4: Visualization & Diagnostics (Cells 10-24)**
10. 📊 Forest Plot
11. 🍎 Orchard Plot
12. 📊 Linear Meta-Regression (Data Layer)
13. 📈 Meta-Regression (Data Layer)
14. 📈 Meta-Regression Plot
15. 🌊 Non-Linear Spline Models
16. 📊 Spline Plot
17. 📉 Publication Bias Diagnostics (Egger's & Trim-Fill)
18. 📊 PET-PEESE Analysis
19. 📊 Funnel Plot
20. 📊 Trim-and-Fill Plot
21. 🧪 Sensitivity Analysis: Leave-One-Out
22. 📊 Sensitivity Plot
23. 📊 Baujat Plot (Diagnostics)
24. 📈 Cumulative Meta-Analysis
25. 📊 Cumulative Trends Visualization

### Main Research Purpose

**Co-Met** is a comprehensive meta-analysis toolkit designed for **ecological and evolutionary biology** research. It provides:

- **Multi-level modeling** (2-level and 3-level random effects)
- **Shared control handling** (variance-covariance matrices)
- **Publication bias assessment** (Egger's, Trim-Fill, PET-PEESE)
- **Sensitivity analyses** (Leave-One-Out, Baujat)
- **Advanced regression** (Linear, spline, robust variance estimation)
- **Publication-ready outputs** (Forest plots, funnel plots, orchard plots)

---

## 2. Code Organization

### Libraries and Dependencies

#### **Core Scientific Computing**
```python
numpy, pandas, scipy (stats, optimize, special, linalg)
```

#### **Statistical Modeling**
```python
statsmodels.api, patsy
```

#### **Visualization**
```python
matplotlib.pyplot, seaborn
```

#### **Google Colab Integration**
```python
google.colab.auth, google.auth, gspread
ipywidgets, IPython.display
```

#### **Utilities**
```python
warnings, datetime, sys, io, base64, traceback
```

#### **Export**
```python
xlsxwriter
```

⚠️ **Issue:** No explicit version pinning - versions are not documented

### Key Functions Defined

**Total Functions:** 70
**Total Classes:** 91

#### **Statistical Core Functions**

| Function | Purpose |
|----------|---------|
| `calculate_tau_squared_DL()` | DerSimonian-Laird tau² estimator |
| `calculate_tau_squared_REML()` | REML tau² estimator |
| `calculate_tau_squared_ML()` | Maximum likelihood tau² estimator |
| `calculate_tau_squared_PM()` | Paule-Mandel estimator |
| `calculate_tau_squared_SJ()` | Sidik-Jonkman estimator |
| `calculate_tau_squared()` | Unified wrapper for all methods |
| `calculate_re_pooled()` | Random-effects pooled estimate |
| `calculate_knapp_hartung_ci()` | Knapp-Hartung adjusted CI |
| `calculate_hedges_g_python()` | Hedges' g with exact gamma correction |
| `compare_tau_estimators()` | Sensitivity comparison of tau² methods |

#### **Three-Level Model Functions**

| Function | Purpose |
|----------|---------|
| `_get_three_level_estimates()` | Core 3-level REML estimation with VCV matrices |
| `_negative_log_likelihood_reml()` | Optimization wrapper |
| `_get_three_level_estimates_loo()` | Leave-one-out version |
| `_neg_log_lik_reml()` | Simplified likelihood for Sherman-Morrison |
| `run_python_3level()` | Multi-start optimization with polishing |
| `_get_three_level_regression_estimates_v2()` | Meta-regression with moderators |
| `_get_gls_estimates()` | Generalized Least Squares estimation |

#### **Data Management Classes (MVC Pattern)**

**Data Layer (Models):**
- `OverallDataManager`
- `SubgroupDataManager`
- `OverallConfig`
- `SubgroupConfig`
- `GlobalSettings`

**Analysis Layer (Business Logic):**
- `OverallEngine`
- `FixedEffectEngine`
- `HeterogeneityEngine`
- `TwoLevelEngine`
- `ThreeLevelEngine`
- `SubgroupAnalyzer`
- `SubgroupAnalysisEngine`

**Presentation Layer (Views):**
- `OverallResultsView`
- `OverallHTMLTemplates`
- `OverallPublicationTextGenerator`

**Controller Layer:**
- `OverallController`

### Data Inputs and Outputs

#### **Input Methods**
1. **Google Sheets** (via `gspread` with OAuth)
2. **Local CSV** (`.csv`)
3. **Excel files** (`.xlsx`, `.xls`)

#### **Required Input Columns**
```python
# Raw data mode
['xe', 'sde', 'ne', 'xc', 'sdc', 'nc', 'id']

# Pre-calculated mode
[effect_size_column, variance_column, study_id]
```

#### **Output Files**
- **Excel Reports** (`.xlsx`):
  - Overall Results
  - Subgroup Results
  - Regression Results
  - Sensitivity Results
  - Cumulative Results
  - Processed Data
  - Protocol & Settings
  - Publication Text

- **Figures** (PDF & PNG):
  - Forest plots
  - Funnel plots
  - Orchard plots
  - Regression plots
  - Sensitivity plots
  - Baujat plots
  - Cumulative plots

### Main Analysis Pipeline

```
1. Data Loading → Column Mapping → Validation
2. Global Filtering → Type Conversion → Missing Data Handling
3. Effect Size Calculation (lnRR, Hedges' g, Cohen's d, log-OR)
4. Shared Control Detection → VCV Matrix Construction
5. Overall Meta-Analysis (2-level or 3-level model selection)
6. Subgroup Analysis (categorical moderators)
7. Meta-Regression (continuous moderators, splines)
8. Publication Bias Assessment (Egger's, Trim-Fill, PET-PEESE)
9. Sensitivity Analysis (Leave-One-Out, Baujat)
10. Cumulative Meta-Analysis (temporal trends)
11. Export (Excel + Figures + Publication Text)
```

### Visualization Approaches

- **Forest Plots:** Customizable (horizontal/vertical, color schemes, PI/CI intervals)
- **Orchard Plots:** Grouped effect sizes with scaled bubbles
- **Funnel Plots:** Publication bias detection with trim-fill overlay
- **Regression Plots:** Bubble plots with fitted lines
- **Spline Plots:** Non-linear trend visualization
- **Baujat Plots:** Influence vs. heterogeneity contribution
- **Cumulative Plots:** Dual-axis (effect size + I²) temporal trends

**Customization Options:**
- Color schemes (grayscale, viridis, plasma, etc.)
- Size (width, height)
- DPI (publication quality)
- Transparency
- Font sizes
- Export formats (PDF, PNG)

---

## 3. Technical Assessment

### Code Quality Observations

#### **Strengths:**
✅ **Well-documented:** ~1,172 docstring markers (extensive inline documentation)
✅ **Error handling:** 252 try/except blocks (robust fault tolerance)
✅ **Modular architecture:** Clear MVC separation
✅ **Reproducibility:** Random seeds set (`np.random.seed(42)`)
✅ **Numerical stability:** Sherman-Morrison optimization, Cholesky decomposition with fallbacks
✅ **Multiple estimators:** 5+ tau² methods for sensitivity analysis

#### **Weaknesses:**
⚠️ **Cell size:** Average 997 lines/cell is excessive (should be <200)
⚠️ **Global state:** Heavy reliance on `ANALYSIS_CONFIG` dictionary
⚠️ **Redundancy:** Multiple similar functions (e.g., 3 tau² DL implementations)
⚠️ **Complexity:** Some functions exceed 200 lines (difficult to test/maintain)
⚠️ **No unit tests:** No testing infrastructure visible
⚠️ **Magic numbers:** Some hardcoded constants (e.g., `1e-10`, `1e-6`)

### Documentation Level

#### **What's Well-Documented:**
- Function docstrings with parameters, returns, and descriptions
- Cell-level headers with Purpose/Dependencies/Outputs
- Inline comments explaining statistical formulas
- Algorithm advantages/disadvantages in docstrings

#### **What's Missing:**
- **No README** or usage guide within notebook
- **No version history** or changelog
- **No validation examples** with known results
- **Limited markdown explanations** (only 1 markdown cell)
- **No references** to statistical papers/methods

### Reproducibility Considerations

#### ✅ **Good Practices:**
- Random seeds set (`np.random.seed(42)`)
- No hardcoded file paths detected
- Configurable via constants (`REQUIRED_COLUMNS`, `SUPPORTED_EFFECT_SIZES`)
- Suppresses non-critical warnings

#### ⚠️ **Issues:**
- **No package version tracking**
  ```python
  # Missing:
  # numpy==1.24.0
  # pandas==2.0.0
  # scipy==1.11.0
  ```
- **No environment.yml or requirements.txt**
- **Google Colab-specific dependencies** (not portable to other platforms)
- **Global state mutations** make cell execution order critical
- **No data provenance tracking** (where did input data come from?)

### Computational Efficiency Concerns

#### **Potential Bottlenecks:**

1. **Large cell execution:**
   - Cells with 1000+ lines may cause memory issues
   - Difficult to debug when errors occur

2. **Matrix operations:**
   - Proper use of Sherman-Morrison for diagonal cases ✅
   - Cholesky decomposition with fallbacks ✅
   - Potential slowdown with many shared controls (full matrix inversion)

3. **Multiple optimization starts:**
   ```python
   start_points = [[0.01, 0.01], [0.5, 0.1], [0.1, 0.5], [0.001, 0.001]]
   # 4 L-BFGS-B runs + 1 Nelder-Mead polish
   ```
   This is good for robustness but increases runtime

4. **Leave-One-Out analysis:**
   - O(k) model refits where k = number of studies
   - Can be slow for large meta-analyses

#### **Optimizations Present:**
✅ Fast path for diagonal VCV matrices (Sherman-Morrison)
✅ Vectorized operations (NumPy/Pandas)
✅ Efficient matrix decompositions (Cholesky preferred)
✅ Caching of VCV matrices in `ANALYSIS_CONFIG`

---

## 4. Methods in Ecology and Evolution Standards

### ✅ **Reproducibility**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Random seeds set | ✅ Yes | `np.random.seed(42)` in multiple locations |
| File paths hardcoded | ✅ No | Uses upload widgets & config |
| Data versioning | ⚠️ Partial | No explicit data provenance |
| Code versioning | ❌ No | No Git SHA or version tags in output |
| Computational environment | ⚠️ Partial | Google Colab assumed, no `requirements.txt` |

**Recommendation:** Add package version logging to Excel export

### ⚠️ **Documentation**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Step-by-step explanations | ⚠️ Partial | Good cell headers, but no markdown narrative |
| Statistical methods referenced | ❌ No | No citations to DerSimonian-Laird, REML papers, etc. |
| Workflow diagram | ❌ No | Complex pipeline not visually explained |
| Usage examples | ❌ No | No tutorial or vignette |
| Assumptions documented | ⚠️ Partial | Statistical assumptions in docstrings only |

**Recommendation:** Add markdown cells with:
- Study background
- Statistical method citations
- Workflow diagram
- Expected outputs

### ✅ **Code Readability**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Descriptive variable names | ✅ Yes | `tau_sq`, `pooled_effect`, `vcv_matrices` |
| Comments present | ✅ Yes | Extensive inline comments |
| Consistent naming | ✅ Yes | snake_case for functions, PascalCase for classes |
| Magic numbers | ⚠️ Some | `1e-10`, `1e-6` could be named constants |

**Recommendation:** Define constants for numerical tolerances:
```python
EPSILON = 1e-10
MATRIX_JITTER = 1e-6
CONVERGENCE_TOL = 1e-8
```

### ⚠️ **Modularity**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Repeated code blocks | ⚠️ Some | Multiple tau² DL implementations |
| Large functions | ⚠️ Yes | Some functions >200 lines |
| Cell dependencies | ⚠️ High | Global `ANALYSIS_CONFIG` coupling |
| Reusable components | ✅ Yes | Good MVC separation in later cells |

**Issues Found:**

1. **Duplicate tau² DL implementations:**
   - `calculate_tau_squared_DL()` (line ~70)
   - `calculate_tau_squared_dl()` (line ~200, wrapper)
   - Embedded DL logic in cumulative analysis

2. **Monolithic cells:**
   - Cell 1: 3,700+ lines (should be split)
   - Cell 7: 1,500+ lines (Data + Analysis + View in one cell)

**Recommendation:** Extract to separate cells:
```
Cell 1a: Imports & Configuration
Cell 1b: Tau² Estimators
Cell 1c: Three-Level Models
Cell 1d: Utility Functions
```

### ⚠️ **Figures**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Publication-ready quality | ✅ Yes | DPI configurable, PDF export available |
| Proper labels | ✅ Yes | Axis labels, titles, legends present |
| Font sizes | ✅ Yes | Configurable via UI widgets |
| Color schemes | ✅ Yes | Grayscale option for print journals |
| Figure captions | ❌ No | No auto-generated captions |
| Alt text | ❌ No | Accessibility not considered |

**Recommendation:** Auto-generate figure captions:
```python
caption = f"Figure {fig_num}: Forest plot of {es_type} effect sizes (k={n_studies} studies, N={n_total} observations). Error bars represent 95% confidence intervals."
```

### ❌ **Dependencies**

| Criterion | Status | Notes |
|-----------|--------|-------|
| Packages listed | ⚠️ Implicit | In import statements only |
| Versions specified | ❌ No | No version pinning |
| Installation instructions | ❌ No | Assumes Google Colab |
| Conda/pip files | ❌ No | No `requirements.txt` or `environment.yml` |

**Current State:**
```python
# Implicit from imports:
numpy, pandas, scipy, matplotlib, seaborn
statsmodels, patsy, xlsxwriter, gspread
ipywidgets, google-auth, google-auth-oauthlib
```

**Recommendation:** Add to first cell:
```python
# Co-Met Dependencies (tested versions)
# numpy==1.24.3
# pandas==2.0.3
# scipy==1.11.1
# matplotlib==3.7.2
# seaborn==0.12.2
# statsmodels==0.14.0
# xlsxwriter==3.1.2
# gspread==5.10.0

# Log versions
import sys
print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"SciPy: {scipy.__version__}")
```

---

## 5. Potential Issues to Flag

### 🔴 **Critical Issues**

1. **Cell Size (Maintainability Crisis)**
   - Average 997 lines per cell
   - Cell 1 alone: 3,700+ lines
   - **Impact:** Difficult to debug, test, or reuse
   - **Fix:** Split into logical subcells (<200 lines each)

2. **Global State Management**
   ```python
   ANALYSIS_CONFIG = {}  # Mutated across 20+ cells
   ```
   - **Impact:** Cell execution order is critical
   - **Risk:** Hard to track data flow
   - **Fix:** Use explicit function parameters or class instances

3. **No Dependency Versioning**
   - **Impact:** Code may break with future package updates
   - **Risk:** Results not reproducible in 1-2 years
   - **Fix:** Pin versions in requirements.txt

### ⚠️ **Moderate Issues**

4. **Redundant Implementations**
   - 3 versions of DL tau² estimator
   - Similar plotting code repeated across cells
   - **Fix:** Consolidate into single canonical implementation

5. **Long Functions**
   - `_get_three_level_estimates()`: ~250 lines
   - `_get_gls_estimates()`: ~200 lines
   - **Fix:** Extract helper functions:
     ```python
     def _compute_sherman_morrison_inverse(A_diag, tau_sq):
         """Fast inverse for diagonal + low-rank matrices"""
         ...
     ```

6. **Magic Numbers**
   ```python
   if tau_sq < 0: tau_sq = 1e-10
   Sigma_ridged = Sigma_i + 1e-6 * np.eye(k)
   ```
   - **Fix:** Define named constants

7. **Hardcoded Settings**
   ```python
   options={'ftol': 1e-12, 'gtol': 1e-12}
   ```
   - **Fix:** Make optimizer tolerances configurable

### ℹ️ **Minor Issues**

8. **Limited Error Messages**
   - Generic exceptions in try/except blocks
   - **Fix:** Add specific error messages:
     ```python
     except np.linalg.LinAlgError as e:
         raise ValueError(f"VCV matrix is singular for study {study_id}: {e}")
     ```

9. **No Input Validation**
   - Functions assume valid inputs
   - **Fix:** Add assertions:
     ```python
     assert len(yi) == len(vi), "Effect sizes and variances must match"
     assert all(vi > 0), "Variances must be positive"
     ```

10. **Warning Suppression**
    ```python
    warnings.filterwarnings('ignore', category=FutureWarning)
    ```
    - **Risk:** May hide important deprecation warnings
    - **Fix:** Suppress selectively:
      ```python
      with warnings.catch_warnings():
          warnings.filterwarnings('ignore', category=FutureWarning, module='scipy')
          ...
      ```

### 🔍 **Deprecated Functions Check**

✅ **No deprecated functions detected**

- SciPy functions are current (as of 2025)
- Pandas operations use modern API
- No `append()` loops (uses list comprehension + concat)

---

## 6. Refactoring Recommendations

### 🎯 **Priority 1: Code Modularity (High Impact)**

#### **1.1 Split Cell 1 into Logical Units**

**Current:** 3,700 lines in one cell
**Proposed:**

```
Cell 1.1: Imports & Configuration (50 lines)
Cell 1.2: Tau² Estimators (300 lines)
  - calculate_tau_squared_DL
  - calculate_tau_squared_REML
  - calculate_tau_squared_ML
  - calculate_tau_squared_PM
  - calculate_tau_squared_SJ

Cell 1.3: Pooled Effect Calculations (200 lines)
  - calculate_re_pooled
  - calculate_knapp_hartung_ci

Cell 1.4: Three-Level Core Functions (500 lines)
  - _get_three_level_estimates
  - _negative_log_likelihood_reml
  - run_python_3level

Cell 1.5: Three-Level Regression (400 lines)
  - _get_three_level_regression_estimates_v2
  - _get_gls_estimates

Cell 1.6: Export Utilities (300 lines)
  - export_analysis_report
  - _apply_excel_formatting
```

#### **1.2 Eliminate Redundant Functions**

**Consolidate tau² DL implementations:**

```python
# BEFORE: 3 implementations
calculate_tau_squared_DL()
calculate_tau_squared_dl()  # Wrapper version
# Embedded version in cumulative analysis

# AFTER: 1 canonical implementation
def calculate_tau_squared_DL(df, effect_col, var_col):
    """
    DerSimonian-Laird estimator for between-study variance.

    Reference:
        DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials.
        Controlled Clinical Trials, 7(3), 177-188.
    """
    # Single, well-tested implementation
```

#### **1.3 Extract Repeated Code Patterns**

**Plotting code is duplicated across 8 cells:**

```python
# Create reusable plot utilities
def create_publication_figure(width=10, height=6, dpi=300):
    """Standardized figure creation"""
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    return fig, ax

def apply_publication_styling(ax, xlabel, ylabel, title):
    """Consistent plot styling"""
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, weight='bold')
    sns.despine(ax=ax)

def export_figure(fig, filename, formats=['pdf', 'png'], dpi=300):
    """Standardized figure export"""
    for fmt in formats:
        fig.savefig(f"{filename}.{fmt}", dpi=dpi, bbox_inches='tight')
```

### 🎯 **Priority 2: Documentation (Medium Impact)**

#### **2.1 Add Narrative Markdown Cells**

Insert before each phase:

```markdown
## Phase 1: Data Preparation

This section handles data loading from multiple sources (Google Sheets, CSV, Excel)
and maps user columns to standardized names required for meta-analysis.

**Required columns for raw data:**
- `xe`, `xc`: Mean values (experimental vs. control)
- `sde`, `sdc`: Standard deviations
- `ne`, `nc`: Sample sizes
- `id`: Study identifier

**Supported effect sizes:**
- Log Response Ratio (lnRR) - for ratio data
- Hedges' g - for standardized mean differences
- Cohen's d - uncorrected SMD
- Log Odds Ratio - for binary outcomes
```

#### **2.2 Add Statistical Method References**

```python
def calculate_tau_squared_REML(df, effect_col, var_col, max_iter=100, tol=1e-8):
    """
    Restricted Maximum Likelihood (REML) estimator for tau-squared.

    REML is generally preferred over DL and ML methods as it:
    - Accounts for uncertainty in fixed effects
    - Provides less biased estimates in small samples
    - Is the default in metafor::rma() and meta::metagen()

    References:
    -----------
    Viechtbauer, W. (2005). Bias and efficiency of meta-analytic variance
        estimators in the random-effects model. Journal of Educational and
        Behavioral Statistics, 30(3), 261-293.

    Raudenbush, S. W. (2009). Analyzing effect sizes: Random effects models.
        In H. Cooper et al. (Eds.), The handbook of research synthesis and
        meta-analysis (2nd ed., pp. 295-315). Russell Sage Foundation.
    """
```

#### **2.3 Add Workflow Diagram**

```markdown
## Co-Met Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      1. DATA INGESTION                          │
│  Google Sheets / CSV / Excel → Column Mapping → Validation      │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   2. DATA PREPARATION                            │
│  Global Filtering → Type Conversion → Missing Data Handling     │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                3. EFFECT SIZE CALCULATION                        │
│  lnRR / Hedges' g / Cohen's d → VCV Matrix (if shared controls) │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                  4. META-ANALYSIS MODELS                         │
│  2-Level (simple) vs. 3-Level (nested) model selection          │
│  DL / REML / ML tau² estimation → Pooled Effect ± CI            │
└────────────────────────┬────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
┌─────────────▼──────────┐ ┌───────▼──────────────────────────────┐
│  5. SUBGROUP ANALYSIS  │ │   6. META-REGRESSION                 │
│  Categorical moderators│ │   Continuous moderators + Splines    │
└─────────────┬──────────┘ └───────┬──────────────────────────────┘
              │                     │
              └──────────┬──────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              7. DIAGNOSTICS & SENSITIVITY                        │
│  Publication Bias (Egger, Trim-Fill, PET-PEESE)                 │
│  Sensitivity (Leave-One-Out, Baujat)                            │
│  Cumulative Meta-Analysis                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    8. EXPORT & REPORTING                         │
│  Excel Report + Publication Figures (PDF/PNG)                   │
│  Auto-generated Methods & Results Text                          │
└─────────────────────────────────────────────────────────────────┘
```
```

### 🎯 **Priority 3: Reproducibility (High Impact)**

#### **3.1 Add Package Version Logging**

Insert at end of Cell 1:

```python
# =============================================================================
# ENVIRONMENT INFORMATION (for reproducibility)
# =============================================================================

def log_environment_info():
    """
    Logs package versions and system info for reproducibility.
    This information is automatically included in Excel exports.
    """
    import platform

    env_info = {
        'Python Version': sys.version.split()[0],
        'NumPy': np.__version__,
        'Pandas': pd.__version__,
        'SciPy': scipy.__version__,
        'Matplotlib': plt.matplotlib.__version__,
        'Seaborn': sns.__version__,
        'Statsmodels': sm.__version__,
        'Platform': platform.platform(),
        'Timestamp': datetime.datetime.now().isoformat()
    }

    print("\n" + "="*70)
    print("ENVIRONMENT INFORMATION (for reproducibility)")
    print("="*70)
    for key, value in env_info.items():
        print(f"{key:20s}: {value}")
    print("="*70 + "\n")

    # Store in global config for export
    if 'ANALYSIS_CONFIG' not in globals():
        global ANALYSIS_CONFIG
        ANALYSIS_CONFIG = {}
    ANALYSIS_CONFIG['environment_info'] = env_info

    return env_info

# Execute on import
env_info = log_environment_info()
```

#### **3.2 Update Excel Export to Include Metadata**

Modify `export_analysis_report()`:

```python
def export_analysis_report(report_type='overall', filename_prefix="MetaAnalysis"):
    """Export comprehensive Excel report with reproducibility metadata"""

    # ... existing code ...

    # NEW: Add Environment Info sheet
    if 'environment_info' in ANALYSIS_CONFIG:
        env_df = pd.DataFrame([
            {'Parameter': k, 'Value': v}
            for k, v in ANALYSIS_CONFIG['environment_info'].items()
        ])
        env_df.to_excel(writer, sheet_name='Environment', index=False)
        _apply_protocol_sheet_formatting(writer, 'Environment', env_df)
```

#### **3.3 Add Data Provenance Tracking**

```python
# In Cell 2 (Data Ingestion)
def track_data_source(source_type, **kwargs):
    """
    Records data source information for reproducibility.

    Parameters:
    -----------
    source_type : str
        'google_sheets', 'csv', or 'excel'
    **kwargs : dict
        sheet_url, filename, upload_timestamp, etc.
    """
    provenance = {
        'source_type': source_type,
        'timestamp': datetime.datetime.now().isoformat(),
        **kwargs
    }

    if 'ANALYSIS_CONFIG' not in globals():
        global ANALYSIS_CONFIG
        ANALYSIS_CONFIG = {}

    ANALYSIS_CONFIG['data_provenance'] = provenance

    # Display to user
    print(f"\n📊 Data Source: {source_type}")
    for key, value in kwargs.items():
        print(f"   {key}: {value}")
```

### 🎯 **Priority 4: Visualization Improvements (Low Impact)**

#### **4.1 Auto-generate Figure Captions**

```python
def generate_figure_caption(fig_type, **kwargs):
    """
    Auto-generates publication-ready figure captions.

    Parameters:
    -----------
    fig_type : str
        'forest', 'funnel', 'regression', 'orchard', etc.
    **kwargs : dict
        n_studies, n_obs, effect_type, I2, etc.
    """
    captions = {
        'forest': (
            f"Forest plot of {kwargs.get('effect_type', 'effect size')} "
            f"estimates from {kwargs.get('n_studies', 'N')} independent studies "
            f"(total N = {kwargs.get('n_obs', 'X')} observations). "
            f"Error bars represent 95% confidence intervals. "
            f"Diamond indicates pooled random-effects estimate. "
            f"Heterogeneity: I² = {kwargs.get('I2', 'X')}%."
        ),
        'funnel': (
            f"Funnel plot for publication bias assessment. "
            f"Studies (k = {kwargs.get('n_studies', 'N')}) are plotted by "
            f"effect size against standard error. "
            f"Egger's test: p = {kwargs.get('egger_p', 'X')}. "
            f"Trim-and-fill estimated {kwargs.get('k0', 'X')} missing studies."
        ),
        # ... more templates ...
    }

    return captions.get(fig_type, f"Figure: {fig_type}")
```

#### **4.2 Add Accessibility Features**

```python
# Color-blind friendly palettes
COLORBLIND_SAFE = {
    'categorical': ['#0173B2', '#DE8F05', '#029E73', '#CC78BC'],
    'sequential': 'viridis',
    'diverging': 'RdBu'
}

# Alt text for screen readers
def add_alt_text(fig, description):
    """Adds alt text to matplotlib figure for accessibility"""
    fig.text(0, 0, description, fontsize=0, color='white')  # Hidden text
```

### 🎯 **Priority 5: Performance Optimization (Optional)**

#### **5.1 Cache Expensive Computations**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def _cached_vcv_matrix(study_id_tuple, var_tuple, rho):
    """
    Cached VCV matrix construction for shared controls.
    Avoids recomputing identical matrices during LOO analysis.
    """
    # ... matrix construction ...
```

#### **5.2 Parallelize Leave-One-Out**

```python
from multiprocessing import Pool

def run_loo_parallel(yi, vi, study_ids, n_cores=4):
    """
    Parallel leave-one-out sensitivity analysis.

    Parameters:
    -----------
    n_cores : int
        Number of CPU cores to use (default: 4)
    """
    from functools import partial

    def loo_iteration(i):
        # LOO logic here
        pass

    with Pool(n_cores) as pool:
        results = pool.map(loo_iteration, range(len(study_ids)))

    return results
```

---

## 7. File Structure

### Input Data Files Referenced

**Supported Formats:**
- `.csv` (comma-separated values)
- `.xlsx`, `.xls` (Excel workbooks)
- Google Sheets (via URL or worksheet name)

**No hardcoded paths detected** ✅

### Output Files Generated

#### **Excel Reports** (`.xlsx`)

**Filename Pattern:** `{prefix}_{YYYYMMDD_HHMM}.xlsx`

**Sheets Included:**
1. `Overall Results` - Pooled effect size, CI, I², tau²
2. `Subgroup Results` - Moderator analysis (if performed)
3. `Regression Results` - Meta-regression coefficients
4. `Spline Results` - Non-linear trend analysis
5. `Eggers Test` - Publication bias diagnostic
6. `Trim Fill` - Adjusted pooled estimates
7. `Cumulative Results` - Temporal trends
8. `Cumulative Summary` - Trend statistics
9. `Sensitivity Results` - Leave-one-out influence
10. `Influential Studies` - High-influence studies flagged
11. `Processed Data` - Cleaned dataset with effect sizes
12. `Data Exclusions` - Records removed during filtering
13. `Protocol & Settings` - Analysis parameters
14. `Report Text` - Auto-generated methods/results sections
15. `Environment` - Package versions (recommended addition)

#### **Figure Files**

**Formats:** PDF (vector) + PNG (raster)

**Generated Plots:**
- `forest_plot.{pdf,png}` - Main results visualization
- `funnel_plot.{pdf,png}` - Publication bias assessment
- `orchard_plot.{pdf,png}` - Grouped effect sizes
- `regression_plot.{pdf,png}` - Moderator relationships
- `spline_plot.{pdf,png}` - Non-linear trends
- `sensitivity_plot.{pdf,png}` - LOO diagnostics
- `baujat_plot.{pdf,png}` - Influence vs. heterogeneity
- `cumulative_plot.{pdf,png}` - Temporal accumulation
- `trimfill_plot.{pdf,png}` - Adjusted funnel plot

**Export Settings:**
- DPI: Configurable (default 300 for print quality)
- Transparency: Optional (for slide backgrounds)
- Bbox: `tight` (no whitespace cropping)

### External Resources / Dependencies

**Google Colab Specific:**
- `google.colab.auth` - OAuth authentication
- `google.auth.default` - Credential management
- `gspread` - Google Sheets API client
- `ipywidgets` - Interactive UI components
- `IPython.display` - Rich output rendering

**Portability Concern:**
⚠️ Code assumes Google Colab environment. To run locally:
1. Remove `google.colab` imports
2. Replace `ipywidgets` with alternative UI (Streamlit, Dash)
3. Add local file pickers instead of `FileUpload` widget

---

## 8. Summary & Action Items

### Key Findings

| Category | Status | Priority |
|----------|--------|----------|
| **Functionality** | ✅ Excellent | - |
| **Statistical Rigor** | ✅ Excellent | - |
| **Code Organization** | ⚠️ Needs Improvement | HIGH |
| **Documentation** | ⚠️ Needs Improvement | MEDIUM |
| **Reproducibility** | ⚠️ Needs Improvement | HIGH |
| **Visualization** | ✅ Good | LOW |
| **Performance** | ✅ Good | - |

### Action Items for Journal Submission

#### **Before Submission (Critical):**

1. ✅ **Split Cell 1** into 6 logical subcells (<500 lines each)
2. ✅ **Add package version logging** to Excel export
3. ✅ **Create requirements.txt** with pinned versions
4. ✅ **Add markdown narrative** explaining workflow
5. ✅ **Cite statistical methods** (DL, REML, Knapp-Hartung, etc.)
6. ✅ **Add workflow diagram** (see section 6.2.3)
7. ✅ **Document assumptions** (e.g., normality, independence)

#### **Strongly Recommended:**

8. ⚠️ **Consolidate redundant functions** (3 tau² DL implementations → 1)
9. ⚠️ **Add input validation** (assert statements for data integrity)
10. ⚠️ **Replace magic numbers** with named constants
11. ⚠️ **Add figure captions** (auto-generated)
12. ⚠️ **Test with example dataset** (include in supplementary materials)

#### **Nice to Have:**

13. ℹ️ **Add unit tests** for statistical functions
14. ℹ️ **Parallelize LOO** for large meta-analyses
15. ℹ️ **Add accessibility features** (alt text, colorblind palettes)
16. ℹ️ **Create standalone version** (non-Colab compatible)

### Estimated Refactoring Effort

| Task | Time Estimate | Difficulty |
|------|---------------|------------|
| Split cells | 2-3 hours | Easy |
| Add documentation | 3-4 hours | Easy |
| Version logging | 1 hour | Easy |
| Consolidate functions | 2-3 hours | Medium |
| Add tests | 5-8 hours | Medium |
| Workflow diagram | 1 hour | Easy |
| **Total** | **14-20 hours** | - |

---

## 9. Compliance Checklist for Methods in Ecology and Evolution

### Manuscript Requirements

- [ ] **Code Availability Statement**
  - Example: "All analyses were conducted in Python 3.10 using a custom Jupyter notebook (Co_Met_6_3.ipynb) available at [GitHub URL] under MIT License."

- [ ] **Data Availability Statement**
  - Example: "Raw data and processed effect sizes are available in Supplementary Data S1 (Excel format)."

- [ ] **Reproducibility Statement**
  - Example: "Analysis code was executed in Google Colab with package versions recorded in Supplementary Code S1. Random seed set to 42 for all stochastic procedures."

### Supplementary Materials to Include

1. **Supplementary Code S1:** Co_Met_6_3.ipynb (refactored)
2. **Supplementary Code S2:** requirements.txt (package versions)
3. **Supplementary Data S1:** Raw_Data.xlsx (input data)
4. **Supplementary Data S2:** Processed_Data.xlsx (effect sizes + metadata)
5. **Supplementary Table S1:** Analysis_Settings.xlsx (all parameters)
6. **Supplementary Figure S1:** Workflow_Diagram.pdf

### Statistical Reporting Checklist

- [x] Effect size type clearly stated (lnRR, Hedges' g, etc.)
- [x] Confidence interval level reported (95%)
- [x] Heterogeneity metrics reported (I², tau², Q-test)
- [x] Model selection justified (2-level vs. 3-level)
- [x] Tau² estimation method specified (REML)
- [ ] Knapp-Hartung adjustment documented (if used)
- [x] Publication bias tests reported (Egger's, Trim-Fill)
- [x] Sensitivity analysis performed (Leave-One-Out)
- [ ] Moderator analysis pre-specified (should be in protocol)

---

## 10. Conclusion

**Co_Met_6_3.ipynb** is a **statistically rigorous and feature-rich** meta-analysis toolkit that demonstrates:

✅ **Strengths:**
- Advanced statistical methods (3-level models, VCV matrices, robust SE)
- Comprehensive diagnostics (publication bias, sensitivity, cumulative)
- Publication-ready visualizations
- Well-documented functions
- Numerical stability optimizations

⚠️ **Areas for Improvement:**
- **Code organization:** Cells are too large (avg. 997 lines)
- **Reproducibility:** No package version tracking
- **Documentation:** Limited narrative explanations
- **Modularity:** Some code duplication

**Recommendation:** With **2-3 days of focused refactoring** (14-20 hours), this notebook will meet or exceed Methods in Ecology and Evolution standards for computational reproducibility and code quality.

**Priority Actions:**
1. Split Cell 1 into logical subcells
2. Add package version logging
3. Create requirements.txt
4. Add markdown narrative and workflow diagram
5. Cite statistical methods

After these changes, the notebook will be **publication-ready** and suitable for archival repositories (e.g., Zenodo, Dryad, GitHub).

---

**Report Generated:** 2026-01-03
**Notebook Analyzed:** Co_Met_6_3.ipynb (976.2 KB)
**Total Analysis Time:** ~45 minutes
**Tools Used:** jq, grep, bash, comprehensive code inspection
