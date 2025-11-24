#@title 📥 DOWNLOAD: Overall Meta-Analysis Results

# =============================================================================
# INSERT THIS AT THE END OF CELL 7 (Overall Meta-Analysis)
# Downloads pooled estimates, heterogeneity, and model comparison
# =============================================================================

if 'overall_results' in ANALYSIS_CONFIG:

    create_download_section('Download Overall Results', '📊')

    # Extract results
    results = ANALYSIS_CONFIG['overall_results']

    # Create model comparison DataFrame
    model_comparison = pd.DataFrame({
        'Model': ['Fixed Effect', 'Random 2-Level', 'Random 3-Level'],
        'Pooled_Effect': [
            results.get('pooled_g_fixed', np.nan),
            results.get('pooled_g_random', np.nan),
            results.get('pooled_g', np.nan)
        ],
        'SE': [
            results.get('SE_pooled_fixed', np.nan),
            results.get('SE_pooled_random', np.nan),
            results.get('SE_pooled', np.nan)
        ],
        'CI_Lower': [
            results.get('CI_lower_fixed', np.nan),
            results.get('CI_lower_random', np.nan),
            results.get('CI_lower', np.nan)
        ],
        'CI_Upper': [
            results.get('CI_upper_fixed', np.nan),
            results.get('CI_upper_random', np.nan),
            results.get('CI_upper', np.nan)
        ],
        'p_value': [
            results.get('p_value_fixed', np.nan),
            results.get('p_value_random', np.nan),
            results.get('p_value', np.nan)
        ],
        'AIC': [
            results.get('AIC_fixed', np.nan),
            results.get('AIC_random', np.nan),
            results.get('AIC', np.nan)
        ]
    })

    # Create heterogeneity DataFrame
    heterogeneity = pd.DataFrame({
        'Metric': ['τ² (Level 2)', 'τ² (Level 3)', 'I²', 'H²', 'Q Statistic', 'Q p-value'],
        'Value': [
            results.get('tau_squared_level2', np.nan),
            results.get('tau_squared_level3', np.nan),
            results.get('I_squared', np.nan),
            results.get('H_squared', np.nan),
            results.get('Q_statistic', np.nan),
            results.get('Q_p_value', np.nan)
        ]
    })

    # Create sample info DataFrame
    sample_info = pd.DataFrame({
        'Metric': ['Total Studies', 'Total Observations', 'Effect Size Type', 'Best Model (AIC)'],
        'Value': [
            results.get('k_studies', 'N/A'),
            results.get('n_observations', 'N/A'),
            ANALYSIS_CONFIG.get('es_config', {}).get('effect_type', 'Hedges g'),
            '3-Level Random Effects' if results.get('AIC', 9999) == min(
                results.get('AIC_fixed', 9999),
                results.get('AIC_random', 9999),
                results.get('AIC', 9999)
            ) else 'See AIC comparison'
        ]
    })

    # Combine into dict for Excel
    results_dict = {
        'Model_Comparison': model_comparison,
        'Heterogeneity': heterogeneity,
        'Sample_Info': sample_info
    }

    # Metadata
    metadata = {
        'title': 'Overall Meta-Analysis Results - Co-Met',
        'summary': {
            'Pooled Effect (3-Level)': f"{results.get('pooled_g', np.nan):.4f}",
            '95% CI': f"[{results.get('CI_lower', np.nan):.4f}, {results.get('CI_upper', np.nan):.4f}]",
            'p-value': f"{results.get('p_value', np.nan):.4f}",
            'I² (Heterogeneity)': f"{results.get('I_squared', np.nan):.1f}%",
            'Studies': results.get('k_studies', 'N/A'),
            'Observations': results.get('n_observations', 'N/A')
        },
        'sheets': {
            'README': 'Analysis documentation',
            'Model_Comparison': 'Fixed, 2-level, and 3-level model results',
            'Heterogeneity': 'Heterogeneity statistics (τ², I², H², Q)',
            'Sample_Info': 'Sample size and analysis details'
        },
        'columns': {
            'Pooled_Effect': 'Overall pooled effect size estimate',
            'SE': 'Standard error of pooled estimate',
            'CI_Lower': 'Lower bound of 95% confidence interval',
            'CI_Upper': 'Upper bound of 95% confidence interval',
            'p_value': 'Statistical significance (two-tailed)',
            'AIC': 'Akaike Information Criterion (lower = better fit)',
            'tau_squared': 'Between-study variance',
            'I_squared': 'Percentage of variation due to heterogeneity',
            'Q_statistic': 'Cochran Q test for heterogeneity'
        }
    }

    create_download_button(
        data=results_dict,
        filename_base='overall_meta_analysis',
        title='📊 Overall Meta-Analysis Results',
        description='Primary findings from your meta-analysis - Perfect for manuscript tables.',
        includes_list=[
            'Model comparison (Fixed, 2-Level, 3-Level)',
            'Pooled effect estimates with confidence intervals',
            'Heterogeneity statistics (τ², I², H², Q)',
            'Model fit criteria (AIC)',
            f'{results.get("k_studies", "N/A")} studies, {results.get("n_observations", "N/A")} observations'
        ],
        formats=['excel', 'csv'],
        metadata=metadata
    )

else:
    print("⚠️ Warning: overall_results not found. Please run Cell 7 first.")
