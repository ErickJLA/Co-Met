# ADD TO END OF CELL 6 (Calculate Effect Sizes) - FIXED VERSION
# This integrates download into a new tab instead of appending to cell

# Check if tabs exist and analysis_data is available
if 'analysis_data' in globals() and analysis_data is not None and len(analysis_data) > 0:

    # Prepare metadata
    metadata = {
        'title': 'Complete Dataset with Effect Sizes - Co-Met Meta-Analysis',
        'summary': {
            'Total Studies': int(len(analysis_data['id'].unique())) if 'id' in analysis_data.columns else 'N/A',
            'Total Observations': int(len(analysis_data)),
            'Effect Size Type': str(ANALYSIS_CONFIG.get('es_config', {}).get('effect_type', 'Hedges g')) if 'ANALYSIS_CONFIG' in globals() else 'Hedges g',
            'Analysis Date': datetime.now().strftime('%Y-%m-%d')
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
            'w_fixed': 'Weight for fixed-effect model (1/Vg)'
        }
    }

    # Create download tab
    download_tab = create_download_tab(
        data=analysis_data,
        filename_base='data_with_effect_sizes',
        title='Download Complete Dataset',
        description='⭐ ESSENTIAL - Complete dataset with all calculated effect sizes for full reproducibility.',
        formats=['csv', 'excel'],
        metadata=metadata
    )

    # Add to existing tabs
    if 'tabs' in locals():
        # Get existing tabs
        existing_children = list(tabs.children)
        existing_children.append(download_tab)
        tabs.children = existing_children
        tabs.set_title(len(existing_children) - 1, '📥 Download')
    else:
        # No tabs exist, display standalone
        display(HTML("<div style='background:#667eea;padding:10px;color:white;border-radius:5px;margin:10px 0;'><strong>📥 Download Options</strong></div>"))
        display(download_tab)
else:
    print("⚠️  Download not available: analysis_data not found or empty")
