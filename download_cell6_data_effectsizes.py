#@title 📥 DOWNLOAD: Complete Data + Effect Sizes

# =============================================================================
# INSERT THIS AT THE END OF CELL 6 (Calculate Effect Sizes)
# This is the MOST IMPORTANT download - provides full reproducibility
# =============================================================================

if 'analysis_data' in globals() and analysis_data is not None:

    create_download_section('Download Complete Dataset', '💾')

    # Prepare metadata
    metadata = {
        'title': 'Complete Dataset with Effect Sizes - Co-Met Meta-Analysis',
        'summary': {
            'Total Studies': len(analysis_data['id'].unique()) if 'id' in analysis_data.columns else 'N/A',
            'Total Observations': len(analysis_data),
            'Effect Size Type': ANALYSIS_CONFIG.get('es_config', {}).get('effect_type', 'Hedges g'),
            'Analysis Date': datetime.now().strftime('%Y-%m-%d'),
            'SD Imputation': f"{ANALYSIS_CONFIG.get('imputation_count', 0)} observations" if ANALYSIS_CONFIG.get('imputation_count', 0) > 0 else 'None'
        },
        'columns': {
            'id': 'Study/paper identifier',
            'xe': 'Mean value (experimental/treatment group)',
            'sde': 'Standard deviation (experimental group)',
            'ne': 'Sample size (experimental group)',
            'xc': 'Mean value (control group)',
            'sdc': 'Standard deviation (control group)',
            'nc': 'Sample size (control group)',
            'hedges_g': 'Standardized mean difference (Hedges g with bias correction)',
            'Vg': 'Variance of effect size',
            'SE_g': 'Standard error of effect size',
            'CI_lower_g': 'Lower bound of 95% confidence interval',
            'CI_upper_g': 'Upper bound of 95% confidence interval',
            'w_fixed': 'Weight for fixed-effect model (1/Vg)',
            'w_random': 'Weight for random-effects model'
        },
        'sheets': {
            'README': 'Analysis documentation and metadata',
            'Data': 'Complete dataset with calculated effect sizes'
        }
    }

    create_download_button(
        data=analysis_data,
        filename_base='data_with_effect_sizes',
        title='📊 Complete Dataset + Effect Sizes',
        description='⭐ ESSENTIAL for reproducibility - Contains all raw data and calculated effect sizes.',
        includes_list=[
            'Raw data (means, SDs, sample sizes)',
            'Calculated effect sizes (Hedges g)',
            'Confidence intervals and weights',
            'All moderator variables',
            f'{len(analysis_data)} observations from {len(analysis_data["id"].unique())} studies'
        ],
        formats=['csv', 'excel'],
        metadata=metadata,
        expected_columns=['id', 'hedges_g', 'Vg']
    )

else:
    print("⚠️ Warning: analysis_data not found. Please run Cell 6 first.")
