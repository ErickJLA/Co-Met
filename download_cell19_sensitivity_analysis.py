#@title 📥 DOWNLOAD: Leave-One-Out Sensitivity Analysis

# =============================================================================
# INSERT THIS AT THE END OF CELL 19 (Leave-One-Out Sensitivity)
# Downloads influence diagnostics showing impact of each study
# =============================================================================

if 'loo_results' in globals() and loo_results is not None:

    create_download_section('Download Sensitivity Analysis', '🛡️')

    # Add overall result as reference
    if 'overall_results' in ANALYSIS_CONFIG:
        overall_g = ANALYSIS_CONFIG['overall_results'].get('pooled_g', np.nan)
        overall_se = ANALYSIS_CONFIG['overall_results'].get('SE_pooled', np.nan)
        overall_ci_lower = ANALYSIS_CONFIG['overall_results'].get('CI_lower', np.nan)
        overall_ci_upper = ANALYSIS_CONFIG['overall_results'].get('CI_upper', np.nan)

        # Calculate differences and flag influential studies
        loo_results_copy = loo_results.copy()

        if 'pooled_g_loo' in loo_results_copy.columns:
            loo_results_copy['Difference_from_Original'] = loo_results_copy['pooled_g_loo'] - overall_g
            loo_results_copy['Percent_Change'] = (loo_results_copy['Difference_from_Original'] / overall_g * 100)
            loo_results_copy['Influential'] = loo_results_copy['Percent_Change'].abs() > 5  # >5% change

        # Identify influential studies
        if 'Influential' in loo_results_copy.columns:
            influential_df = loo_results_copy[loo_results_copy['Influential'] == True].copy()
            influential_df = influential_df.sort_values('Percent_Change', ascending=False, key=abs)
        else:
            influential_df = pd.DataFrame({'Note': ['No influential studies detected']})

        # Summary statistics
        summary_df = pd.DataFrame({
            'Metric': [
                'Original Pooled Effect',
                'Min LOO Effect',
                'Max LOO Effect',
                'Range',
                'Mean LOO Effect',
                'SD LOO Effect',
                'Influential Studies (>5%)',
                'Influential Studies (>10%)',
                'Most Influential Study',
                'Max % Change'
            ],
            'Value': [
                f"{overall_g:.4f}",
                f"{loo_results_copy['pooled_g_loo'].min():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
                f"{loo_results_copy['pooled_g_loo'].max():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
                f"{loo_results_copy['pooled_g_loo'].max() - loo_results_copy['pooled_g_loo'].min():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
                f"{loo_results_copy['pooled_g_loo'].mean():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
                f"{loo_results_copy['pooled_g_loo'].std():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
                int((loo_results_copy['Percent_Change'].abs() > 5).sum()) if 'Percent_Change' in loo_results_copy.columns else 'N/A',
                int((loo_results_copy['Percent_Change'].abs() > 10).sum()) if 'Percent_Change' in loo_results_copy.columns else 'N/A',
                loo_results_copy.loc[loo_results_copy['Percent_Change'].abs().idxmax(), 'study_removed'] if 'Percent_Change' in loo_results_copy.columns and len(loo_results_copy) > 0 else 'N/A',
                f"{loo_results_copy['Percent_Change'].abs().max():.1f}%" if 'Percent_Change' in loo_results_copy.columns else 'N/A'
            ]
        })

        # Combine into dict
        sensitivity_dict = {
            'Leave_One_Out_Results': loo_results_copy,
            'Influential_Studies': influential_df,
            'Summary_Statistics': summary_df
        }

    else:
        sensitivity_dict = {'Leave_One_Out_Results': loo_results}

    # Metadata
    metadata = {
        'title': 'Leave-One-Out Sensitivity Analysis - Co-Met',
        'summary': {
            'Total Studies': len(loo_results),
            'Original Pooled Effect': f"{overall_g:.4f}" if 'overall_results' in ANALYSIS_CONFIG else 'N/A',
            'Influential Studies (>5%)': int((loo_results_copy['Percent_Change'].abs() > 5).sum()) if 'Percent_Change' in loo_results_copy.columns else 'N/A',
            'Effect Range (LOO)': f"{loo_results_copy['pooled_g_loo'].min():.4f} to {loo_results_copy['pooled_g_loo'].max():.4f}" if 'pooled_g_loo' in loo_results_copy.columns else 'N/A',
            'Analysis Date': datetime.now().strftime('%Y-%m-%d')
        },
        'sheets': {
            'README': 'Analysis documentation',
            'Leave_One_Out_Results': 'Complete LOO results (all studies)',
            'Influential_Studies': 'Studies with >5% influence on pooled estimate',
            'Summary_Statistics': 'Overview of sensitivity analysis'
        },
        'columns': {
            'study_removed': 'Study identifier (omitted from analysis)',
            'pooled_g_loo': 'Pooled effect without this study',
            'SE_loo': 'Standard error without this study',
            'CI_lower_loo': 'Lower 95% CI without this study',
            'CI_upper_loo': 'Upper 95% CI without this study',
            'Difference_from_Original': 'Change in pooled effect',
            'Percent_Change': 'Percentage change from original',
            'Influential': 'TRUE if >5% influence detected'
        }
    }

    create_download_button(
        data=sensitivity_dict,
        filename_base='leave_one_out_sensitivity',
        title='🛡️ Leave-One-Out Sensitivity Analysis',
        description='Assess robustness - Shows how each study influences your pooled estimate.',
        includes_list=[
            f'{len(loo_results)} leave-one-out iterations',
            'Influence diagnostics per study',
            'Influential studies flagged (>5% change)',
            'Summary statistics (range, mean, SD)',
            f'{int((loo_results_copy["Percent_Change"].abs() > 5).sum()) if "Percent_Change" in loo_results_copy.columns else 0} influential studies identified'
        ],
        formats=['csv', 'excel'],
        metadata=metadata
    )

else:
    print("⚠️ Warning: loo_results not found. Please run Cell 19 first.")
