# Co-Met 📊

A comprehensive Google Colab notebook for conducting publication-ready meta-analyses with advanced statistical methods.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ErickJLA/Co-Met/blob/main/Co_Met.ipynb)

## Overview

Co-Met is a user-friendly, interactive tool for performing rigorous meta-analyses directly in your browser using Google Colab. It implements state-of-the-art statistical methods for combining research findings across multiple studies, with special support for:

- Multiple effect size measures (Log Response Ratio, Hedges' g, Cohen's d, Log Odds Ratio)
- Three-level meta-analytic models for dependent effect sizes
- Cluster-robust inference
- Publication bias assessment
- Meta-regression and subgroup analyses
- Advanced heterogeneity estimation
- Publication-ready visualizations

## Features

### ✨ Core Capabilities

- **Multiple Effect Size Types**: Automatically detect and calculate appropriate effect sizes
- **Three-Level Models**: Account for multiple effect sizes per study using multilevel models
- **Robust Statistics**: Cluster-robust variance estimation and multiple heterogeneity estimators (DL, REML, ML, PM, SJ)
- **Publication Bias Tools**: Funnel plots, Egger's test, trim-and-fill analysis
- **Meta-Regression**: Test continuous and categorical moderators
- **Spline Analysis**: Model non-linear relationships
- **Sensitivity Analysis**: Leave-one-out and cumulative meta-analysis
- **Interactive Interface**: User-friendly widgets for configuration
- **Publication-Ready Plots**: High-quality forest plots, funnel plots, and more

### 📊 Supported Effect Sizes

- **lnRR**: Log Response Ratio (for ratio-scale data)
- **Hedges' g**: Standardized mean difference with small-sample correction
- **Cohen's d**: Standardized mean difference
- **Log OR**: Log odds ratio

## Quick Start

### 1. Open in Google Colab

Click the "Open in Colab" badge above or [click here](https://colab.research.google.com/github/ErickJLA/Co-Met/blob/main/Co_Met.ipynb).

### 2. Prepare Your Data

Create a Google Sheet with the following required columns:

| Column | Description | Example |
|--------|-------------|---------|
| `id` | Study identifier | "Smith2020" |
| `xe` | Experimental group mean | 25.3 |
| `sde` | Experimental group SD | 4.2 |
| `ne` | Experimental group sample size | 30 |
| `xc` | Control group mean | 22.1 |
| `sdc` | Control group SD | 3.8 |
| `nc` | Control group sample size | 28 |

**Optional**: Add categorical columns for moderator analysis (e.g., "species", "treatment_type", "year")

### 3. Run the Analysis

Follow the step-by-step workflow in the notebook:

1. **Cell 1**: Import libraries & authenticate with Google
2. **Cell 2**: Load your data from Google Sheets
3. **Cell 3**: Configure analysis parameters
4. **Cell 4**: Apply configuration & clean data
5. **Cell 6**: Detect effect size type
6. **Cell 7**: Calculate effect sizes
7. **Cell 8**: View overall meta-analysis results
8. **Cells 9-19**: Advanced analyses (subgroups, regression, plots)

## Statistical Methods

This notebook implements methods from:

- **Borenstein, M., Hedges, L. V., Higgins, J. P., & Rothstein, H. R. (2009)**. *Introduction to Meta-Analysis*. John Wiley & Sons.
- **Viechtbauer, W. (2010)**. *Conducting meta-analyses in R with the metafor package*. Journal of Statistical Software, 36(3), 1-48.
- **Hedges, L. V., & Olkin, I. (1985)**. *Statistical methods for meta-analysis*. Academic Press.

## Requirements

No local installation required! Everything runs in Google Colab.

The notebook uses the following Python packages (automatically available in Colab):
- NumPy
- Pandas
- SciPy
- Matplotlib
- gspread (for Google Sheets integration)
- ipywidgets (for interactive interface)
- statsmodels (for regression)

## Use Cases

Co-Met is ideal for:

- **Academic researchers** conducting systematic reviews and meta-analyses
- **Graduate students** learning meta-analytic methods
- **Research teams** needing collaborative, cloud-based analysis
- **Educators** teaching meta-analysis techniques
- **Anyone** needing publication-ready meta-analysis without R or specialized software

## Advanced Features

- **Three-Level Models**: Properly handle dependency when studies contribute multiple effect sizes
- **Cluster-Robust Inference**: Adjust standard errors for within-study correlation
- **Multiple Tau² Estimators**: Choose from DL, REML, ML, PM, or SJ methods
- **Spline Meta-Regression**: Test for non-linear moderator effects
- **Publication Bias Assessment**: Multiple diagnostic tools and corrections
- **Sensitivity Analysis**: Assess influence of individual studies
- **Customizable Plots**: Publication-ready figures with extensive customization

## Citation

If you use Co-Met in your research, please cite:

```
Co-Met: A Google Colab notebook for meta-analysis (2025)
GitHub repository: https://github.com/ErickJLA/Co-Met
```

And please cite the statistical methods you use (references provided in the notebook).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## Troubleshooting

### "Authentication Failed"
- Restart runtime and re-run Cell 1
- Check Google account permissions

### "Data Not Found"
- Verify Google Sheet name spelling
- Ensure sheet is shared with your Colab email
- Check that worksheet exists

### "Invalid Column Names"
- Use Cell 3 accordion to map column names
- Ensure no duplicate mappings

## Support

For questions, issues, or suggestions:
- Open an issue on [GitHub](https://github.com/ErickJLA/Co-Met/issues)
- Check the detailed documentation within the notebook

## Acknowledgments

This tool implements statistical methods developed by the meta-analysis research community. We are grateful to the authors of the foundational texts and packages that made this work possible.

---

**Made with ❤️ for the research community**
