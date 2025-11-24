#@title 📥 DOWNLOAD: Meta-Regression Results

# =============================================================================
# INSERT THIS AT THE END OF CELL 12 (Meta-Regression)
# Downloads regression coefficients, model statistics, and predictions
# =============================================================================

if 'meta_regression_RVE_results' in globals():

    create_download_section('Download Meta-Regression Results', '📈')

    results = meta_regression_RVE_results

    # Coefficients table
    coefficients_df = pd.DataFrame({
        'Term': ['Intercept (β₀)', results.get('predictor_name', 'Predictor (β₁)')],
        'Beta': [results.get('beta_0', np.nan), results.get('beta_1', np.nan)],
        'SE_Robust': [results.get('SE_beta_0', np.nan), results.get('SE_beta_1', np.nan)],
        't_statistic': [results.get('t_beta_0', np.nan), results.get('t_beta_1', np.nan)],
        'df': [results.get('df', np.nan), results.get('df', np.nan)],
        'p_value': [results.get('p_beta_0', np.nan), results.get('p_beta_1', np.nan)],
        'CI_Lower_95': [results.get('CI_lower_beta_0', np.nan), results.get('CI_lower_beta_1', np.nan)],
        'CI_Upper_95': [results.get('CI_upper_beta_0', np.nan), results.get('CI_upper_beta_1', np.nan)]
    })

    # Model statistics
    model_stats_df = pd.DataFrame({
        'Statistic': [
            'R² (variance explained)',
            'Adjusted R²',
            'τ² Level 2 (residual within)',
            'τ² Level 3 (residual between)',
            'QE (residual heterogeneity)',
            'QE p-value',
            'QM (model test)',
            'QM p-value',
            'AIC',
            'Log-likelihood',
            'df'
        ],
        'Value': [
            f"{results.get('R_squared', np.nan):.4f}",
            f"{results.get('R_squared_adjusted', np.nan):.4f}",
            f"{results.get('tau_squared_level2', np.nan):.4f}",
            f"{results.get('tau_squared_level3', np.nan):.4f}",
            f"{results.get('QE', np.nan):.4f}",
            f"{results.get('QE_p_value', np.nan):.4f}",
            f"{results.get('QM', np.nan):.4f}",
            f"{results.get('QM_p_value', np.nan):.4f}",
            f"{results.get('AIC', np.nan):.2f}",
            f"{results.get('logLik', np.nan):.2f}",
            results.get('df', 'N/A')
        ]
    })

    # Predicted values (if available)
    if 'predicted_values' in results and results['predicted_values'] is not None:
        predicted_df = results['predicted_values']
    else:
        predicted_df = pd.DataFrame({
            'Note': ['Predicted values not available - generate in plot cell']
        })

    # Combine into dict
    regression_dict = {
        'Regression_Coefficients': coefficients_df,
        'Model_Statistics': model_stats_df,
        'Predicted_Values': predicted_df
    }

    # Metadata
    metadata = {
        'title': 'Meta-Regression Results - Co-Met',
        'summary': {
            'Predictor': results.get('predictor_name', 'N/A'),
            'Slope (β₁)': f"{results.get('beta_1', np.nan):.4f}",
            'p-value': f"{results.get('p_beta_1', np.nan):.4f}",
            'R²': f"{results.get('R_squared', np.nan)*100:.1f}%",
            'Studies': results.get('k_studies', 'N/A'),
            'Observations': results.get('n_observations', 'N/A')
        },
        'sheets': {
            'README': 'Analysis documentation',
            'Regression_Coefficients': 'Intercept and slope with cluster-robust SEs',
            'Model_Statistics': 'R², heterogeneity, model fit (AIC)',
            'Predicted_Values': 'Fitted values for plotting (if available)'
        },
        'columns': {
            'Beta': 'Regression coefficient',
            'SE_Robust': 'Cluster-robust standard error (RVE)',
            't_statistic': 't-test statistic',
            'p_value': 'Statistical significance (two-tailed)',
            'R_squared': 'Proportion of between-study variance explained',
            'QE': 'Residual heterogeneity test',
            'QM': 'Omnibus test of moderator(s)',
            'tau_squared': 'Residual variance after accounting for predictor'
        }
    }

    create_download_button(
        data=regression_dict,
        filename_base='meta_regression',
        title='📈 Meta-Regression Results',
        description='Quantitative moderator analysis showing how continuous variables relate to effect sizes.',
        includes_list=[
            'Regression coefficients (intercept + slope)',
            'Cluster-robust standard errors (RVE)',
            f'R² = {results.get("R_squared", 0)*100:.1f}% variance explained',
            'Model statistics (QE, QM, AIC)',
            'Predicted values for plotting'
        ],
        formats=['excel', 'csv'],
        metadata=metadata
    )

else:
    print("⚠️ Warning: meta_regression_RVE_results not found. Please run Cell 12 first.")
