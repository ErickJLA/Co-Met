#@title 📦 DOWNLOAD: COMPLETE ANALYSIS PACKAGE

# =============================================================================
# NEW CELL 22: INSERT AT THE END OF THE NOTEBOOK
# Downloads EVERYTHING in one professionally formatted Excel workbook
# =============================================================================

# Check if key analyses are available
has_data = 'analysis_data' in globals() and analysis_data is not None
has_overall = 'overall_results' in ANALYSIS_CONFIG if 'ANALYSIS_CONFIG' in globals() else False
has_subgroups = 'subgroup_results' in ANALYSIS_CONFIG and len(ANALYSIS_CONFIG.get('subgroup_results', {})) > 0 if 'ANALYSIS_CONFIG' in globals() else False
has_regression = 'meta_regression_RVE_results' in globals()
has_bias = 'funnel_results' in globals() and 'trimfill_results' in globals()
has_loo = 'loo_results' in globals() and loo_results is not None

if has_data:

    create_download_section('Complete Analysis Package', '📦')

    display(HTML("""
        <div style='background-color: #fff3cd; border: 2px solid #ffc107;
                    border-radius: 10px; padding: 20px; margin: 15px 0;'>
            <h2 style='color: #856404; margin-top: 0;'>⭐ RECOMMENDED FOR PUBLICATIONS</h2>
            <p style='color: #856404; font-size: 16px;'>
                This downloads <strong>EVERYTHING</strong> in one professionally organized Excel file.
                Perfect for manuscript supplementary materials, peer review, and long-term archival.
            </p>
        </div>
    """))

    # Build complete package
    complete_package = {}

    # === DATA ===
    if has_data:
        complete_package['Complete_Dataset'] = analysis_data

    # === OVERALL RESULTS ===
    if has_overall:
        results = ANALYSIS_CONFIG['overall_results']

        # Model comparison
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
        complete_package['Overall_Model_Comparison'] = model_comparison

        # Heterogeneity
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
        complete_package['Overall_Heterogeneity'] = heterogeneity

    # === SUBGROUP RESULTS ===
    if has_subgroups:
        subgroup_results = ANALYSIS_CONFIG['subgroup_results']

        # Summary table
        summary_rows = []
        for moderator, levels in subgroup_results.items():
            for level_name, level_results in levels.items():
                summary_rows.append({
                    'Moderator': moderator,
                    'Level': level_name,
                    'k_studies': level_results.get('k_studies', np.nan),
                    'n_observations': level_results.get('n_observations', np.nan),
                    'Pooled_g': level_results.get('pooled_g', np.nan),
                    'SE': level_results.get('SE_pooled', np.nan),
                    'CI_Lower': level_results.get('CI_lower', np.nan),
                    'CI_Upper': level_results.get('CI_upper', np.nan),
                    'p_value': level_results.get('p_value', np.nan),
                    'I_squared': level_results.get('I_squared', np.nan)
                })
        complete_package['Subgroup_Summary'] = pd.DataFrame(summary_rows)

    # === META-REGRESSION ===
    if has_regression:
        results = meta_regression_RVE_results

        coefficients = pd.DataFrame({
            'Term': ['Intercept (β₀)', results.get('predictor_name', 'Predictor (β₁)')],
            'Beta': [results.get('beta_0', np.nan), results.get('beta_1', np.nan)],
            'SE_Robust': [results.get('SE_beta_0', np.nan), results.get('SE_beta_1', np.nan)],
            't_statistic': [results.get('t_beta_0', np.nan), results.get('t_beta_1', np.nan)],
            'p_value': [results.get('p_beta_0', np.nan), results.get('p_beta_1', np.nan)],
            'CI_Lower': [results.get('CI_lower_beta_0', np.nan), results.get('CI_lower_beta_1', np.nan)],
            'CI_Upper': [results.get('CI_upper_beta_0', np.nan), results.get('CI_upper_beta_1', np.nan)]
        })
        complete_package['Meta_Regression'] = coefficients

    # === PUBLICATION BIAS ===
    if has_bias:
        egger_df = pd.DataFrame({
            'Parameter': ['Intercept', 'SE', 't-statistic', 'p-value'],
            'Value': [
                funnel_results.get('egger_intercept', np.nan),
                funnel_results.get('egger_SE', np.nan),
                funnel_results.get('egger_t', np.nan),
                funnel_results.get('egger_p', np.nan)
            ]
        })
        complete_package['Publication_Bias_Egger'] = egger_df

        trimfill_df = pd.DataFrame({
            'Metric': ['Original Effect', 'Adjusted Effect', 'Studies Imputed'],
            'Value': [
                trimfill_results.get('original_pooled', np.nan),
                trimfill_results.get('adjusted_pooled', np.nan),
                trimfill_results.get('n_imputed', 0)
            ]
        })
        complete_package['Publication_Bias_TrimFill'] = trimfill_df

    # === SENSITIVITY ANALYSIS ===
    if has_loo:
        complete_package['Leave_One_Out'] = loo_results

    # === ANALYSIS SETTINGS ===
    settings_df = pd.DataFrame({
        'Setting': [
            'Analysis Date',
            'Effect Size Type',
            'Total Studies',
            'Total Observations',
            'Analysis Method',
            'Confidence Level',
            'Minimum n per group',
            'SD Imputation'
        ],
        'Value': [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ANALYSIS_CONFIG.get('es_config', {}).get('effect_type', 'Hedges g') if 'ANALYSIS_CONFIG' in globals() else 'N/A',
            len(analysis_data['id'].unique()) if 'id' in analysis_data.columns else 'N/A',
            len(analysis_data) if has_data else 'N/A',
            '3-Level Random Effects (REML)',
            '95%',
            ANALYSIS_CONFIG.get('min_n', 'N/A') if 'ANALYSIS_CONFIG' in globals() else 'N/A',
            f"{ANALYSIS_CONFIG.get('imputation_count', 0)} observations" if 'ANALYSIS_CONFIG' in globals() and ANALYSIS_CONFIG.get('imputation_count', 0) > 0 else 'None'
        ]
    })
    complete_package['Analysis_Settings'] = settings_df

    # === METADATA ===
    metadata = {
        'title': 'COMPLETE META-ANALYSIS PACKAGE - Co-Met',
        'summary': {
            'Package Type': 'Complete reproducibility package',
            'Analysis Date': datetime.now().strftime('%Y-%m-%d'),
            'Total Studies': len(analysis_data['id'].unique()) if 'id' in analysis_data.columns else 'N/A',
            'Total Observations': len(analysis_data) if has_data else 'N/A',
            'Effect Size': ANALYSIS_CONFIG.get('es_config', {}).get('effect_type', 'Hedges g') if 'ANALYSIS_CONFIG' in globals() else 'N/A',
            'Pooled Effect': f"{ANALYSIS_CONFIG['overall_results'].get('pooled_g', np.nan):.4f}" if has_overall else 'N/A',
            '95% CI': f"[{ANALYSIS_CONFIG['overall_results'].get('CI_lower', np.nan):.4f}, {ANALYSIS_CONFIG['overall_results'].get('CI_upper', np.nan):.4f}]" if has_overall else 'N/A',
            'Sheets Included': len(complete_package) + 1  # +1 for README
        },
        'sheets': {
            'README': '📄 Analysis documentation and metadata',
            'Complete_Dataset': '📊 Raw data + calculated effect sizes',
            'Overall_Model_Comparison': '🎯 Fixed, 2-level, and 3-level models',
            'Overall_Heterogeneity': '📉 Heterogeneity statistics (τ², I², Q)',
            'Subgroup_Summary': '🔬 Moderator analysis summary',
            'Meta_Regression': '📈 Regression coefficients (if run)',
            'Publication_Bias_Egger': '🔍 Egger test for asymmetry',
            'Publication_Bias_TrimFill': '🔍 Trim-and-Fill sensitivity',
            'Leave_One_Out': '🛡️ Influence diagnostics',
            'Analysis_Settings': '⚙️ Configuration and parameters'
        },
        'columns': {
            'id': 'Study identifier',
            'hedges_g': 'Effect size (Hedges g)',
            'Vg': 'Effect size variance',
            'SE_g': 'Standard error',
            'CI_lower_g': 'Lower 95% CI',
            'CI_upper_g': 'Upper 95% CI',
            'Pooled_Effect': 'Meta-analytic pooled estimate',
            'tau_squared': 'Between-study variance',
            'I_squared': 'Heterogeneity percentage',
            'p_value': 'Statistical significance'
        }
    }

    # Display what's included
    included_analyses = []
    if has_data: included_analyses.append(f'✓ Complete Dataset ({len(analysis_data)} obs)')
    if has_overall: included_analyses.append('✓ Overall Meta-Analysis')
    if has_subgroups: included_analyses.append(f'✓ Subgroup Analysis ({len(ANALYSIS_CONFIG["subgroup_results"])} moderators)')
    if has_regression: included_analyses.append('✓ Meta-Regression')
    if has_bias: included_analyses.append('✓ Publication Bias Tests')
    if has_loo: included_analyses.append(f'✓ Sensitivity Analysis ({len(loo_results)} iterations)')

    display(HTML(f"""
        <div style='background-color: white; border: 2px solid #4a90e2;
                    border-radius: 8px; padding: 20px; margin: 15px 0;'>
            <h3 style='color: #2d3748; margin-top: 0;'>📦 Complete Analysis Package</h3>
            <p style='color: #4a5568;'>
                This package includes <strong>all available analyses</strong> from your meta-analysis
                in a single, professionally formatted Excel workbook.
            </p>
            <div style='background-color: #f7fafc; padding: 15px; border-radius: 5px; margin: 10px 0;'>
                <strong style='color: #2d3748;'>Package Contents:</strong>
                <ul style='margin: 5px 0; padding-left: 20px; color: #4a5568;'>
                    {''.join([f'<li>{item}</li>' for item in included_analyses])}
                    <li>✓ Analysis Settings & Metadata</li>
                    <li>✓ Complete Data Dictionary</li>
                </ul>
                <p style='margin-top: 10px; color: #718096;'>
                    <strong>Total Sheets:</strong> {len(complete_package) + 1} (including README)
                </p>
            </div>
            <p style='color: #4a5568; margin-top: 15px;'>
                <strong>💡 Perfect for:</strong><br>
                • Manuscript supplementary materials<br>
                • Peer review transparency<br>
                • Sharing with collaborators<br>
                • Long-term archival<br>
                • Complete reproducibility
            </p>
        </div>
    """))

    # Download button
    download_btn = widgets.Button(
        description='📦 DOWNLOAD COMPLETE PACKAGE',
        button_style='success',
        tooltip='Download everything in one Excel file',
        icon='download',
        layout=widgets.Layout(width='100%', height='60px')
    )

    output_area = widgets.Output()

    def on_complete_download_click(b):
        with output_area:
            clear_output()

            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'MetaAnalysis_Complete_Package_{timestamp}.xlsx'

                print(f"⏳ Preparing complete package...")
                print(f"   Creating {len(complete_package) + 1} sheets...")

                file_size = download_excel_with_formatting(
                    complete_package,
                    filename,
                    metadata
                )

                size_str = f"{file_size/1024:.1f} KB"

                create_success_message(filename, size_str)

                display(HTML("""
                    <div style='background-color: #d4edda; border: 1px solid #c3e6cb;
                                border-radius: 5px; padding: 15px; margin: 10px 0;
                                color: #155724;'>
                        <strong>🎉 Complete package ready!</strong><br><br>
                        <strong>Next Steps:</strong><br>
                        1. Open the Excel file and review the README sheet<br>
                        2. Verify all analyses are included<br>
                        3. Use for manuscript supplementary materials<br>
                        4. Share with collaborators or reviewers<br>
                    </div>
                """))

            except Exception as e:
                create_error_message(str(e))
                print(traceback.format_exc())

    download_btn.on_click(on_complete_download_click)

    display(download_btn)
    display(output_area)

else:
    print("⚠️ Warning: No data available. Please run all analysis cells first.")
    print("\nRequired cells:")
    print("  ✓ Cell 6: Calculate Effect Sizes")
    print("  • Cell 7: Overall Meta-Analysis (recommended)")
    print("  • Cell 9: Subgroup Analysis (recommended)")
    print("  • Cell 12: Meta-Regression (optional)")
    print("  • Cell 16: Publication Bias (optional)")
    print("  • Cell 19: Sensitivity Analysis (optional)")
