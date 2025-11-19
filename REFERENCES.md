# References

## Statistical Methods Implemented

This notebook implements statistical methods from the following foundational works in meta-analysis:

### Core Meta-Analysis Texts

**Borenstein, M., Hedges, L. V., Higgins, J. P., & Rothstein, H. R. (2009).**
*Introduction to Meta-Analysis.*
John Wiley & Sons.
ISBN: 978-0-470-05724-7

> Comprehensive introduction to meta-analytic methods, including effect size calculation, heterogeneity assessment, and publication bias detection.

**Hedges, L. V., & Olkin, I. (1985).**
*Statistical Methods for Meta-Analysis.*
Academic Press.
ISBN: 978-0-123-36380-0

> Foundational text on statistical methods for combining effect sizes, including the development of Hedges' g and methods for handling heterogeneity.

### Software and Implementation

**Viechtbauer, W. (2010).**
*Conducting meta-analyses in R with the metafor package.*
Journal of Statistical Software, 36(3), 1-48.
DOI: 10.18637/jss.v036.i03

> Reference implementation of meta-analytic methods in R. This notebook implements similar statistical approaches in Python.

### Specific Methods

#### Three-Level Meta-Analysis

**Van den Noortgate, W., López-López, J. A., Marín-Martínez, F., & Sánchez-Meca, J. (2013).**
*Three-level meta-analysis of dependent effect sizes.*
Behavior Research Methods, 45(2), 576-594.
DOI: 10.3758/s13428-012-0261-6

**Assink, M., & Wibbelink, C. J. (2016).**
*Fitting three-level meta-analytic models in R: A step-by-step tutorial.*
The Quantitative Methods for Psychology, 12(3), 154-174.
DOI: 10.20982/tqmp.12.3.p154

#### Heterogeneity Estimation

**DerSimonian, R., & Laird, N. (1986).**
*Meta-analysis in clinical trials.*
Controlled Clinical Trials, 7(3), 177-188.
DOI: 10.1016/0197-2456(86)90046-2

> DerSimonian-Laird estimator for between-study variance (tau²).

**Viechtbauer, W. (2005).**
*Bias and efficiency of meta-analytic variance estimators in the random-effects model.*
Journal of Educational and Behavioral Statistics, 30(3), 261-293.
DOI: 10.3102/10769986030003261

> Comparison of various heterogeneity estimators (REML, ML, PM, etc.).

#### Publication Bias

**Egger, M., Smith, G. D., Schneider, M., & Minder, C. (1997).**
*Bias in meta-analysis detected by a simple, graphical test.*
BMJ, 315(7109), 629-634.
DOI: 10.1136/bmj.315.7109.629

> Egger's test for funnel plot asymmetry.

**Duval, S., & Tweedie, R. (2000).**
*Trim and fill: a simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis.*
Biometrics, 56(2), 455-463.
DOI: 10.1111/j.0006-341X.2000.00455.x

> Trim-and-fill method for adjusting pooled estimates for publication bias.

#### Meta-Regression

**Thompson, S. G., & Higgins, J. P. (2002).**
*How should meta-regression analyses be undertaken and interpreted?*
Statistics in Medicine, 21(11), 1559-1573.
DOI: 10.1002/sim.1187

**Viechtbauer, W., & López-López, J. A. (2022).**
*Location-scale models for meta-analysis.*
Research Synthesis Methods, 13(6), 697-715.
DOI: 10.1002/jrsm.1562

#### Effect Sizes

**Hedges, L. V. (1981).**
*Distribution theory for Glass's estimator of effect size and related estimators.*
Journal of Educational Statistics, 6(2), 107-128.
DOI: 10.3102/10769986006002107

> Development of Hedges' g correction factor.

**Cohen, J. (1988).**
*Statistical Power Analysis for the Behavioral Sciences* (2nd ed.).
Lawrence Erlbaum Associates.
ISBN: 978-0-805-80283-7

> Cohen's d and interpretation of effect sizes.

**Lajeunesse, M. J. (2011).**
*On the meta-analysis of response ratios for studies with correlated and multi-group designs.*
Ecology, 92(11), 2049-2055.
DOI: 10.1890/11-0423.1

> Log response ratio (lnRR) for ecological and ratio-scale data.

### Methodological Guidelines

**Cochrane Handbook for Systematic Reviews of Interventions (2023).**
Version 6.4.
Edited by Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., & Welch, V. A.
Available at: [www.training.cochrane.org/handbook](https://training.cochrane.org/handbook)

> Comprehensive guide to conducting systematic reviews and meta-analyses following Cochrane standards.

**PRISMA 2020 Statement**
**Page, M. J., McKenzie, J. E., Bossuyt, P. M., et al. (2021).**
*The PRISMA 2020 statement: An updated guideline for reporting systematic reviews.*
BMJ, 372:n71.
DOI: 10.1136/bmj.n71

> Updated reporting guidelines for systematic reviews and meta-analyses.

---

## Python Packages Used

All packages used in this notebook are open-source:

- **NumPy**: Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585, 357-362.
- **Pandas**: McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56-61.
- **SciPy**: Virtanen, P., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261-272.
- **Matplotlib**: Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.
- **statsmodels**: Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 92-96.

---

## Note on Implementation

All code in this notebook is original implementation of the published methods cited above. No code has been copied from proprietary sources. The statistical formulas and algorithms are implemented based on the mathematical descriptions in the cited academic literature, which is standard practice in scientific computing.
