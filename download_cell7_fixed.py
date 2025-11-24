# ADD AS NEW CELL AFTER CELL 7 (Overall Meta-Analysis) - FIXED VERSION
# This creates a download tab for overall results

# Check if overall results exist
if 'ANALYSIS_CONFIG' in globals() and 'overall_results' in ANALYSIS_CONFIG:

    try:
        results = ANALYSIS_CONFIG['overall_results']

        # Create model comparison DataFrame with safe value extraction
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

        # Combine for Excel
        results_dict = {
            'Model_Comparison': model_comparison,
            'Heterogeneity': heterogeneity
        }

        # Metadata
        metadata = {
            'title': 'Overall Meta-Analysis Results - Co-Met',
            'summary': {
                'Pooled Effect (3-Level)': f"{results.get('pooled_g', np.nan):.4f}" if not np.isnan(results.get('pooled_g', np.nan)) else 'N/A',
                'Studies': results.get('k_studies', 'N/A'),
                'Observations': results.get('n_observations', 'N/A'),
                'Analysis Date': datetime.now().strftime('%Y-%m-%d')
            }
        }

        # Create download tab
        download_tab = create_download_tab(
            data=results_dict,
            filename_base='overall_meta_analysis',
            title='Download Overall Results',
            description='Primary meta-analysis findings - Perfect for manuscript tables.',
            formats=['excel', 'csv'],
            metadata=metadata
        )

        # Add to existing tabs
        if 'tabs' in locals():
            existing_children = list(tabs.children)
            existing_children.append(download_tab)
            tabs.children = existing_children
            tabs.set_title(len(existing_children) - 1, '📥 Download')
        else:
            display(HTML("<div style='background:#667eea;padding:10px;color:white;border-radius:5px;margin:10px 0;'><strong>📥 Download Options</strong></div>"))
            display(download_tab)

    except Exception as e:
        print(f"⚠️  Download error: {str(e)}")
        print("   Overall results may have unexpected structure")
else:
    print("⚠️  Download not available: overall_results not found")
