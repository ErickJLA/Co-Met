#@title 📦 Download Helper Functions (FIXED VERSION)

# =============================================================================
# DOWNLOAD HELPER FUNCTIONS - FIXED VERSION
# Purpose: Professional download functionality with robust error handling
# Location: Replace Cell 2 with this version
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime
from google.colab import files
import io
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import traceback

# === CORE DOWNLOAD FUNCTIONS ===

def download_csv_with_metadata(df, filename, metadata=None):
    """Download DataFrame as CSV with metadata header."""
    try:
        buffer = io.StringIO()

        if metadata:
            buffer.write("="*80 + "\n")
            buffer.write(f"# {metadata.get('title', 'Meta-Analysis Results')}\n")
            buffer.write("="*80 + "\n#\n")
            buffer.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n#\n")
            buffer.write("-"*80 + "\n")

            if 'summary' in metadata:
                buffer.write("# SUMMARY:\n#\n")
                for key, value in metadata['summary'].items():
                    buffer.write(f"#   {key}: {value}\n")
                buffer.write("#\n" + "-"*80 + "\n")

            if 'columns' in metadata:
                buffer.write("# COLUMN DESCRIPTIONS:\n#\n")
                for col in df.columns:
                    if col in metadata['columns']:
                        buffer.write(f"#   {col}: {metadata['columns'][col]}\n")
                buffer.write("#\n" + "-"*80 + "\n")

            buffer.write("="*80 + "\n# DATA BEGINS BELOW\n" + "="*80 + "\n")

        df.to_csv(buffer, index=False, encoding='utf-8-sig', float_format='%.6f', na_rep='NA')
        files.download(filename, buffer.getvalue().encode('utf-8-sig'))
        return len(buffer.getvalue())
    except Exception as e:
        raise Exception(f"CSV download failed: {str(e)}")


def download_excel_with_formatting(data_dict, filename, metadata=None):
    """Download as professionally formatted Excel workbook."""
    try:
        if isinstance(data_dict, pd.DataFrame):
            data_dict = {'Data': data_dict}

        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            workbook = writer.book

            # Formats
            header_format = workbook.add_format({
                'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
                'fg_color': '#4a90e2', 'font_color': '#ffffff', 'border': 1
            })
            number_format = workbook.add_format({'num_format': '0.0000', 'border': 1})
            integer_format = workbook.add_format({'num_format': '0', 'border': 1})
            text_format = workbook.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})
            pvalue_format = workbook.add_format({'num_format': '0.0000', 'border': 1})
            significant_format = workbook.add_format({'num_format': '0.0000', 'bg_color': '#d4edda', 'border': 1})

            # README sheet
            if metadata:
                readme = workbook.add_worksheet('README')
                title_format = workbook.add_format({
                    'bold': True, 'font_size': 16, 'font_color': '#ffffff',
                    'bg_color': '#2c5282', 'border': 1
                })
                section_format = workbook.add_format({
                    'bold': True, 'font_size': 12, 'font_color': '#2c5282',
                    'bg_color': '#e6f2ff', 'border': 1
                })

                row = 0
                readme.merge_range(row, 0, row, 5, metadata.get('title', 'Meta-Analysis Results'), title_format)
                readme.set_row(row, 25)
                row += 2

                readme.write(row, 0, 'Generated:', section_format)
                readme.merge_range(row, 1, row, 5, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), text_format)
                row += 2

                if 'summary' in metadata:
                    readme.merge_range(row, 0, row, 5, 'ANALYSIS SUMMARY', section_format)
                    row += 1
                    for key, value in metadata['summary'].items():
                        readme.write(row, 0, f"{key}:", text_format)
                        readme.merge_range(row, 1, row, 5, str(value), text_format)
                        row += 1
                    row += 1

                readme.set_column(0, 0, 25)
                readme.set_column(1, 5, 80)

            # Data sheets
            for sheet_name, df in data_dict.items():
                if sheet_name.lower() == 'readme':
                    continue

                sheet_name = sheet_name[:31].replace('/', '_').replace('\\', '_')
                df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
                worksheet = writer.sheets[sheet_name]

                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(1, col_num, value, header_format)
                    worksheet.set_row(1, 30)

                for col_num, col in enumerate(df.columns):
                    col_lower = col.lower()

                    if any(x in col_lower for x in ['p_value', 'pvalue']):
                        width = 12
                        for row_num in range(len(df)):
                            value = df.iloc[row_num][col]
                            if pd.notna(value) and isinstance(value, (int, float)) and value < 0.05:
                                worksheet.write(row_num + 2, col_num, value, significant_format)
                            else:
                                worksheet.write(row_num + 2, col_num, value, pvalue_format)
                    elif any(x in col_lower for x in ['k_studies', 'n_obs', 'df']):
                        width = 10
                        for row_num in range(len(df)):
                            worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], integer_format)
                    elif pd.api.types.is_numeric_dtype(df[col]):
                        width = 14
                        for row_num in range(len(df)):
                            worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], number_format)
                    else:
                        max_len = df[col].astype(str).str.len().max()
                        width = min(max_len + 2, 40)
                        for row_num in range(len(df)):
                            worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], text_format)

                    worksheet.set_column(col_num, col_num, width)

                worksheet.freeze_panes(2, 0)
                worksheet.autofilter(1, 0, len(df) + 1, len(df.columns) - 1)

        buffer.seek(0)
        files.download(filename, buffer.read())
        return buffer.tell()
    except Exception as e:
        raise Exception(f"Excel download failed: {str(e)}")


# === UI HELPERS ===

def create_success_message(filename, file_size=None):
    """Display success message."""
    size_text = f" ({file_size})" if file_size else ""
    display(HTML(f"""
        <div style='background-color: #d4edda; border: 1px solid #c3e6cb;
                    border-radius: 5px; padding: 15px; margin: 10px 0; color: #155724;'>
            <strong>✅ Download Complete!</strong><br>
            File: <code>{filename}</code>{size_text}<br>
            Check your browser's download folder.
        </div>
    """))


def create_error_message(error_msg):
    """Display error message."""
    display(HTML(f"""
        <div style='background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 5px; padding: 15px; margin: 10px 0; color: #721c24;'>
            <strong>❌ Download Failed</strong><br>
            Error: {error_msg}
        </div>
    """))


def create_download_tab(data, filename_base, title, description,
                        formats=['csv', 'excel'], metadata=None):
    """
    Create download interface in a tab format (like rest of notebook).
    Returns a tab widget that can be added to existing tabs.
    """
    output_area = widgets.Output()

    with output_area:
        # Header
        display(HTML(f"""
            <div style='padding: 10px;'>
                <h3 style='color: #2d3748; margin-top: 0;'>📥 {title}</h3>
                <p style='color: #4a5568; margin: 5px 0;'>{description}</p>
            </div>
        """))

        # Format selector
        if len(formats) > 1:
            format_widget = widgets.RadioButtons(
                options=[(f.upper(), f) for f in formats],
                value=formats[0],
                description='Format:',
                layout=widgets.Layout(width='200px')
            )
            display(format_widget)
        else:
            format_widget = None

        # Download button
        download_btn = widgets.Button(
            description='📥 Download',
            button_style='success',
            icon='download',
            layout=widgets.Layout(width='250px', height='40px')
        )

        download_output = widgets.Output()

        def on_download_click(b):
            with download_output:
                clear_output()
                try:
                    if data is None:
                        create_error_message("No data available for download")
                        return

                    if isinstance(data, pd.DataFrame) and len(data) == 0:
                        create_error_message("DataFrame is empty (0 rows)")
                        return

                    selected_format = format_widget.value if format_widget else formats[0]
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

                    print(f"⏳ Preparing {selected_format.upper()} download...")

                    if selected_format == 'csv':
                        filename = f"{filename_base}_{timestamp}.csv"
                        file_size = download_csv_with_metadata(data, filename, metadata)
                        size_str = f"{file_size/1024:.1f} KB"
                    else:
                        filename = f"{filename_base}_{timestamp}.xlsx"
                        file_size = download_excel_with_formatting(data, filename, metadata)
                        size_str = f"{file_size/1024:.1f} KB"

                    create_success_message(filename, size_str)

                except Exception as e:
                    create_error_message(str(e))
                    print(f"\nDetailed error:\n{traceback.format_exc()}")

        download_btn.on_click(on_download_click)
        display(download_btn)
        display(download_output)

    return output_area


print("✅ Download helper functions loaded (FIXED VERSION)!")
