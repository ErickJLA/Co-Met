#@title 📥 DOWNLOAD: Subgroup Analysis Results

# =============================================================================
# INSERT THIS AT THE END OF CELL 9 (Subgroup Analysis Execution)
# Downloads all subgroup analyses organized by moderator
# =============================================================================

if 'subgroup_results' in ANALYSIS_CONFIG:

    create_download_section('Download Subgroup Analysis', '🔬')

    subgroup_results = ANALYSIS_CONFIG['subgroup_results']

    if subgroup_results and len(subgroup_results) > 0:

        # Create summary table (all moderators combined)
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
                    'tau_squared': level_results.get('tau_squared_level2', np.nan),
                    'I_squared': level_results.get('I_squared', np.nan)
                })

        summary_df = pd.DataFrame(summary_rows)

        # Create detailed sheets per moderator
        results_dict = {'Summary_All_Moderators': summary_df}

        for moderator, levels in subgroup_results.items():
            detailed_rows = []
            for level_name, level_results in levels.items():
                detailed_rows.append({
                    'Subgroup_Level': level_name,
                    'k_studies': level_results.get('k_studies', np.nan),
                    'n_observations': level_results.get('n_observations', np.nan),
                    'Pooled_g_3Level': level_results.get('pooled_g', np.nan),
                    'SE': level_results.get('SE_pooled', np.nan),
                    'CI_Lower_95': level_results.get('CI_lower', np.nan),
                    'CI_Upper_95': level_results.get('CI_upper', np.nan),
                    't_statistic': level_results.get('t_statistic', np.nan),
                    'df': level_results.get('df', np.nan),
                    'p_value': level_results.get('p_value', np.nan),
                    'tau_squared_within': level_results.get('tau_squared_level2', np.nan),
                    'tau_squared_between': level_results.get('tau_squared_level3', np.nan),
                    'I_squared': level_results.get('I_squared', np.nan),
                    'Q_statistic': level_results.get('Q_statistic', np.nan),
                    'Q_p_value': level_results.get('Q_p_value', np.nan),
                    'AIC': level_results.get('AIC', np.nan)
                })

            detailed_df = pd.DataFrame(detailed_rows)
            sanitized_name = moderator[:25].replace('/', '_')
            results_dict[f'Moderator_{sanitized_name}'] = detailed_df

        # Metadata
        metadata = {
            'title': 'Subgroup Meta-Analysis Results - Co-Met',
            'summary': {
                'Moderators Analyzed': len(subgroup_results),
                'Total Subgroups': len(summary_df),
                'Analysis Method': '3-Level Random Effects (REML)',
                'Analysis Date': datetime.now().strftime('%Y-%m-%d')
            },
            'sheets': {
                'README': 'Analysis documentation',
                'Summary_All_Moderators': 'Overview of all subgroup analyses',
                **{f'Moderator_{mod[:25]}': f'Detailed results for {mod}'
                   for mod in subgroup_results.keys()}
            },
            'columns': {
                'Moderator': 'Categorical moderator variable',
                'Level': 'Subgroup level within moderator',
                'k_studies': 'Number of unique studies',
                'n_observations': 'Number of effect size observations',
                'Pooled_g': 'Pooled effect size (3-level model)',
                'SE': 'Standard error',
                'CI_Lower': 'Lower 95% confidence interval',
                'CI_Upper': 'Upper 95% confidence interval',
                'p_value': 'Statistical significance',
                'tau_squared': 'Between-study variance within subgroup',
                'I_squared': 'Heterogeneity percentage',
                'Q_statistic': 'Cochran Q test statistic',
                'AIC': 'Model fit criterion (lower = better)'
            }
        }

        create_download_button(
            data=results_dict,
            filename_base='subgroup_analysis',
            title='🔬 Subgroup Analysis Results',
            description='Comprehensive moderator analysis - Explore which factors affect your effect size.',
            includes_list=[
                f'{len(subgroup_results)} moderators analyzed',
                f'{len(summary_df)} total subgroups',
                'Summary table (all moderators combined)',
                'Detailed sheets per moderator',
                'Between-group test statistics',
                'Heterogeneity within each subgroup'
            ],
            formats=['excel', 'csv'],
            metadata=metadata
        )

    else:
        print("⚠️ No subgroup results available.")

else:
    print("⚠️ Warning: subgroup_results not found. Please run Cell 9 first.")
