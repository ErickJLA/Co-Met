# ADD TO END OF CELL 9 (Subgroup Analysis) - FIXED VERSION
# This integrates download into tabs and fixes the AttributeError

# Check if subgroup_results exist and are properly structured
if 'ANALYSIS_CONFIG' in globals() and 'subgroup_results' in ANALYSIS_CONFIG:

    subgroup_results = ANALYSIS_CONFIG['subgroup_results']

    # FIXED: Check if subgroup_results is actually a dict and not empty
    if isinstance(subgroup_results, dict) and len(subgroup_results) > 0:

        try:
            # Create summary table with proper error handling
            summary_rows = []
            valid_moderators = 0

            for moderator, levels in subgroup_results.items():
                # FIXED: Check if levels is actually a dict
                if not isinstance(levels, dict):
                    print(f"⚠️  Skipping {moderator}: not a dictionary")
                    continue

                valid_moderators += 1

                for level_name, level_results in levels.items():
                    # FIXED: Check if level_results is a dict with expected keys
                    if not isinstance(level_results, dict):
                        continue

                    summary_rows.append({
                        'Moderator': str(moderator),
                        'Level': str(level_name),
                        'k_studies': level_results.get('k_studies', np.nan),
                        'n_observations': level_results.get('n_observations', np.nan),
                        'Pooled_g': level_results.get('pooled_g', np.nan),
                        'SE': level_results.get('SE_pooled', np.nan),
                        'CI_Lower': level_results.get('CI_lower', np.nan),
                        'CI_Upper': level_results.get('CI_upper', np.nan),
                        'p_value': level_results.get('p_value', np.nan),
                        'I_squared': level_results.get('I_squared', np.nan)
                    })

            if len(summary_rows) > 0:
                summary_df = pd.DataFrame(summary_rows)

                # Create dict for Excel
                results_dict = {'Summary_All_Moderators': summary_df}

                # Add detailed sheets per moderator
                for moderator, levels in subgroup_results.items():
                    if not isinstance(levels, dict):
                        continue

                    detailed_rows = []
                    for level_name, level_results in levels.items():
                        if not isinstance(level_results, dict):
                            continue

                        detailed_rows.append({
                            'Subgroup_Level': str(level_name),
                            'k_studies': level_results.get('k_studies', np.nan),
                            'n_observations': level_results.get('n_observations', np.nan),
                            'Pooled_g_3Level': level_results.get('pooled_g', np.nan),
                            'SE': level_results.get('SE_pooled', np.nan),
                            'CI_Lower_95': level_results.get('CI_lower', np.nan),
                            'CI_Upper_95': level_results.get('CI_upper', np.nan),
                            'p_value': level_results.get('p_value', np.nan),
                            'I_squared': level_results.get('I_squared', np.nan)
                        })

                    if len(detailed_rows) > 0:
                        detailed_df = pd.DataFrame(detailed_rows)
                        sanitized_name = str(moderator)[:25].replace('/', '_')
                        results_dict[f'Mod_{sanitized_name}'] = detailed_df

                # Metadata
                metadata = {
                    'title': 'Subgroup Meta-Analysis Results - Co-Met',
                    'summary': {
                        'Moderators Analyzed': valid_moderators,
                        'Total Subgroups': len(summary_df),
                        'Analysis Method': '3-Level Random Effects (REML)',
                        'Analysis Date': datetime.now().strftime('%Y-%m-%d')
                    }
                }

                # Create download tab
                download_tab = create_download_tab(
                    data=results_dict,
                    filename_base='subgroup_analysis',
                    title='Download Subgroup Results',
                    description=f'Comprehensive moderator analysis - {valid_moderators} moderators, {len(summary_df)} subgroups',
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

            else:
                print("⚠️  No valid subgroup data to download")

        except Exception as e:
            print(f"⚠️  Download error: {str(e)}")
            print("   Subgroup results may have unexpected structure")

    else:
        print("⚠️  subgroup_results is empty or not a dictionary")
else:
    print("⚠️  Download not available: subgroup_results not found")
