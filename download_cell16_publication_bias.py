#@title 📥 DOWNLOAD: Publication Bias Diagnostics

# =============================================================================
# INSERT THIS AT THE END OF CELL 16 (Publication Bias Diagnostics)
# Downloads Egger's test and Trim-and-Fill results
# =============================================================================

if 'funnel_results' in globals() and 'trimfill_results' in globals():

    create_download_section('Download Publication Bias Tests', '🔍')

    # Egger's test table
    egger_df = pd.DataFrame({
        'Parameter': [
            'Intercept (bias)',
            'SE',
            't-statistic',
            'df',
            'p-value',
            'CI_Lower_95',
            'CI_Upper_95',
            'Interpretation'
        ],
        'Value': [
            f"{funnel_results.get('egger_intercept', np.nan):.4f}",
            f"{funnel_results.get('egger_SE', np.nan):.4f}",
            f"{funnel_results.get('egger_t', np.nan):.4f}",
            funnel_results.get('egger_df', 'N/A'),
            f"{funnel_results.get('egger_p', np.nan):.4f}",
            f"{funnel_results.get('egger_CI_lower', np.nan):.4f}",
            f"{funnel_results.get('egger_CI_upper', np.nan):.4f}",
            'Significant asymmetry detected' if funnel_results.get('egger_p', 1.0) < 0.05 else 'No significant asymmetry'
        ]
    })

    # Trim-and-Fill summary
    trimfill_df = pd.DataFrame({
        'Metric': [
            'Original Pooled Effect',
            'Adjusted Pooled Effect',
            'Change in Effect',
            '% Change',
            'Original SE',
            'Adjusted SE',
            'Original CI Lower',
            'Adjusted CI Lower',
            'Original CI Upper',
            'Adjusted CI Upper',
            'Studies Imputed',
            'Imputation Side',
            'Original n Studies',
            'Adjusted n Studies'
        ],
        'Value': [
            f"{trimfill_results.get('original_pooled', np.nan):.4f}",
            f"{trimfill_results.get('adjusted_pooled', np.nan):.4f}",
            f"{trimfill_results.get('adjusted_pooled', np.nan) - trimfill_results.get('original_pooled', np.nan):.4f}",
            f"{((trimfill_results.get('adjusted_pooled', np.nan) - trimfill_results.get('original_pooled', np.nan)) / trimfill_results.get('original_pooled', 1.0)) * 100:.1f}%",
            f"{trimfill_results.get('original_SE', np.nan):.4f}",
            f"{trimfill_results.get('adjusted_SE', np.nan):.4f}",
            f"{trimfill_results.get('original_CI_lower', np.nan):.4f}",
            f"{trimfill_results.get('adjusted_CI_lower', np.nan):.4f}",
            f"{trimfill_results.get('original_CI_upper', np.nan):.4f}",
            f"{trimfill_results.get('adjusted_CI_upper', np.nan):.4f}",
            trimfill_results.get('n_imputed', 0),
            trimfill_results.get('side', 'N/A'),
            trimfill_results.get('n_studies_original', 'N/A'),
            trimfill_results.get('n_studies_adjusted', 'N/A')
        ]
    })

    # Combined interpretation
    interpretation_df = pd.DataFrame({
        'Test': ['Egger Test', 'Trim-and-Fill'],
        'Result': [
            f"p = {funnel_results.get('egger_p', np.nan):.4f}",
            f"{trimfill_results.get('n_imputed', 0)} studies imputed"
        ],
        'Conclusion': [
            'Asymmetry detected' if funnel_results.get('egger_p', 1.0) < 0.05 else 'No asymmetry',
            f"Effect adjusted by {((trimfill_results.get('adjusted_pooled', 0) - trimfill_results.get('original_pooled', 0)) / trimfill_results.get('original_pooled', 1.0)) * 100:.1f}%"
        ],
        'Recommendation': [
            'Investigate small-study effects' if funnel_results.get('egger_p', 1.0) < 0.05 else 'No action needed',
            'Report both original and adjusted estimates' if trimfill_results.get('n_imputed', 0) > 0 else 'Original estimate robust'
        ]
    })

    # Combine into dict
    bias_dict = {
        'Egger_Test': egger_df,
        'Trim_and_Fill_Summary': trimfill_df,
        'Combined_Interpretation': interpretation_df
    }

    # Metadata
    metadata = {
        'title': 'Publication Bias Diagnostics - Co-Met',
        'summary': {
            'Egger Test p-value': f"{funnel_results.get('egger_p', np.nan):.4f}",
            'Egger Result': 'Significant' if funnel_results.get('egger_p', 1.0) < 0.05 else 'Not significant',
            'Studies Imputed (T&F)': trimfill_results.get('n_imputed', 0),
            'Original Effect': f"{trimfill_results.get('original_pooled', np.nan):.4f}",
            'Adjusted Effect': f"{trimfill_results.get('adjusted_pooled', np.nan):.4f}",
            'Analysis Date': datetime.now().strftime('%Y-%m-%d')
        },
        'sheets': {
            'README': 'Analysis documentation',
            'Egger_Test': "Egger's regression test for funnel plot asymmetry",
            'Trim_and_Fill_Summary': 'Trim-and-Fill sensitivity analysis',
            'Combined_Interpretation': 'Overall assessment and recommendations'
        },
        'columns': {
            'Intercept': 'Egger regression intercept (bias indicator)',
            'p_value': 'Statistical significance (p < 0.05 = asymmetry)',
            'Original_Pooled': 'Pooled effect before adjustment',
            'Adjusted_Pooled': 'Pooled effect after imputing missing studies',
            'n_imputed': 'Number of missing studies imputed',
            'side': 'Which side of funnel studies were imputed'
        }
    }

    create_download_button(
        data=bias_dict,
        filename_base='publication_bias_tests',
        title='🔍 Publication Bias Diagnostics',
        description='Required for transparency - Assess potential publication bias in your meta-analysis.',
        includes_list=[
            "Egger's regression test for asymmetry",
            'Trim-and-Fill sensitivity analysis',
            f'{trimfill_results.get("n_imputed", 0)} studies imputed',
            'Original vs. adjusted pooled estimates',
            'Combined interpretation and recommendations'
        ],
        formats=['excel', 'csv'],
        metadata=metadata
    )

else:
    print("⚠️ Warning: funnel_results or trimfill_results not found. Please run Cell 16 first.")
