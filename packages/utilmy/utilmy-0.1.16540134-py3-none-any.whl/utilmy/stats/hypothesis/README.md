# hypothetical - Hypothesis and Statistical Testing in Python

library for conducting hypothesis and other group comparison tests.


## Available Methods

### Analysis of Variance

* One-way Analysis of Variance (ANOVA)
* One-way Multivariate Analysis of Variance (MANOVA)
* Bartlett's Test for Homogenity of Variances
* Levene's Test for Homogenity of Variances
* Van Der Waerden's (normal scores) Test

### Contingency Tables and Related Tests

* Chi-square test of independence
* Fisher's Exact Test
* McNemar's Test of paired nominal data
* Cochran's Q test
* D critical value (used in the Kolomogorov-Smirnov Goodness-of-Fit test).

### Critical Value Tables and Lookup Functions

* Chi-square statistic
* r (one-sample runs test and Wald-Wolfowitz runs test) statistic 
* Mann-Whitney U-statistic
* Wilcoxon Rank Sum W-statistic

### Descriptive Statistics

* Kurtosis
* Skewness
* Mean Absolute Deviation
* Pearson Correlation
* Spearman Correlation
* Covariance
  - Several algorithms for computing the covariance and covariance matrix of 
    sample data are available
* Variance
  - Several algorithms are also available for computing variance.
* Simulation of Correlation Matrices
  - Multiple simulation algorithms are available for generating correlation matrices.

### Factor Analysis

* Several algorithms for performing Factor Analysis are available, including principal components, principal 
      factors, and iterated principal factors.

### Hypothesis Testing

* Binomial Test
* t-test
  - paired, one and two sample testing

### Nonparametric Methods

* Friedman's test for repeated measures
* Kruskal-Wallis (nonparametric equivalent of one-way ANOVA)
* Mann-Whitney (two sample nonparametric variant of t-test)
* Mood's Median test
* One-sample Runs Test
* Wald-Wolfowitz Two-Sample Runs Test
* Sign test of consistent differences between observation pairs
* Wald-Wolfowitz Two-Sample Runs test
* Wilcoxon Rank Sum Test (one sample nonparametric variant of paired and one-sample t-test)

### Normality and Goodness-of-Fit Tests

* Chi-square one-sample goodness-of-fit
* Jarque-Bera test

### Post-Hoc Analysis

* Tukey's Honestly Significant Difference (HSD)
* Games-Howell (nonparametric)

### Helpful Functions

* Add noise to a correlation or other matrix
* Tie Correction for ranked variables
* Contingency table marginal sums
* Contingency table expected frequencies
* Runs and count of runs


## Requirements

* Python 3.5+
* `numpy>=1.13.0`
* `numpy_indexed>=0.3.5`
* `pandas>=0.22.0`
* `scipy>=1.1.0`
* `statsmodels>=0.9.0`

