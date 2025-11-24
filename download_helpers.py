"""
Co-Met Meta-Analysis - Download Helper Functions
Version: 1.0
Purpose: Provide professional download functionality for all analysis outputs
"""

import pandas as pd
import numpy as np
from datetime import datetime
from google.colab import files
import io
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import traceback
import warnings

# ============================================================================
# CORE DOWNLOAD FUNCTIONS
# ============================================================================

def download_csv_with_metadata(df, filename, metadata=None):
    """
    Download DataFrame as CSV with comprehensive metadata header.

    Parameters:
    -----------
    df : pd.DataFrame
        Data to download
    filename : str
        Output filename (with .csv extension)
    metadata : dict
        Metadata dictionary with keys: title, summary, columns, methods, notes

    Features:
    - UTF-8 with BOM (Excel compatibility)
    - Metadata as commented header
    - No index (unless meaningful)
    - Clean formatting
    """

    buffer = io.StringIO()

    # === WRITE METADATA HEADER ===
    if metadata:
        buffer.write("="*80 + "\n")
        buffer.write(f"# {metadata.get('title', 'Meta-Analysis Results')}\n")
        buffer.write("="*80 + "\n")
        buffer.write("#\n")
        buffer.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if 'analyst' in metadata:
            buffer.write(f"# Analyst: {metadata['analyst']}\n")

        buffer.write("#\n")
        buffer.write("-"*80 + "\n")

        # Summary section
        if 'summary' in metadata:
            buffer.write("# SUMMARY:\n")
            buffer.write("#\n")
            for key, value in metadata['summary'].items():
                buffer.write(f"#   {key}: {value}\n")
            buffer.write("#\n")
            buffer.write("-"*80 + "\n")

        # Column descriptions
        if 'columns' in metadata:
            buffer.write("# COLUMN DESCRIPTIONS:\n")
            buffer.write("#\n")
            for col in df.columns:
                if col in metadata['columns']:
                    desc = metadata['columns'][col]
                    buffer.write(f"#   {col}: {desc}\n")
            buffer.write("#\n")
            buffer.write("-"*80 + "\n")

        # Methods
        if 'methods' in metadata:
            buffer.write("# METHODS:\n")
            buffer.write("#\n")
            for method in metadata['methods']:
                buffer.write(f"#   - {method}\n")
            buffer.write("#\n")
            buffer.write("-"*80 + "\n")

        # Notes
        if 'notes' in metadata:
            buffer.write("# NOTES:\n")
            buffer.write("#\n")
            for note in metadata['notes']:
                buffer.write(f"#   - {note}\n")
            buffer.write("#\n")

        buffer.write("="*80 + "\n")
        buffer.write("#\n")
        buffer.write("# DATA BEGINS BELOW\n")
        buffer.write("#\n")
        buffer.write("="*80 + "\n")

    # === WRITE DATA ===
    include_index = not isinstance(df.index, pd.RangeIndex)

    df.to_csv(
        buffer,
        index=include_index,
        encoding='utf-8-sig',
        float_format='%.6f',
        na_rep='NA',
        quoting=1  # Quote non-numeric
    )

    # === DOWNLOAD ===
    csv_content = buffer.getvalue()
    files.download(filename, csv_content.encode('utf-8-sig'))

    return len(csv_content)


def download_excel_with_formatting(data_dict, filename, metadata=None):
    """
    Download data as professionally formatted Excel workbook.

    Parameters:
    -----------
    data_dict : dict or pd.DataFrame
        If dict: {sheet_name: DataFrame}
        If DataFrame: Single sheet named 'Data'
    filename : str
        Output filename (with .xlsx extension)
    metadata : dict
        Metadata for README sheet

    Features:
    - Multiple sheets
    - README sheet with documentation
    - Formatted headers (bold, colored)
    - Auto-sized columns
    - Frozen panes
    - Intelligent number formatting
    """

    # Convert single DataFrame to dict
    if isinstance(data_dict, pd.DataFrame):
        data_dict = {'Data': data_dict}

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book

        # === DEFINE FORMATS ===
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#ffffff',
            'bg_color': '#2c5282',
            'align': 'left',
            'valign': 'vcenter',
            'border': 1
        })

        section_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'font_color': '#2c5282',
            'bg_color': '#e6f2ff',
            'border': 1
        })

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'align': 'center',
            'fg_color': '#4a90e2',
            'font_color': '#ffffff',
            'border': 1,
            'font_size': 11
        })

        number_format = workbook.add_format({
            'num_format': '0.0000',
            'border': 1
        })

        integer_format = workbook.add_format({
            'num_format': '0',
            'border': 1
        })

        pvalue_format = workbook.add_format({
            'num_format': '0.0000',
            'border': 1
        })

        text_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1
        })

        significant_format = workbook.add_format({
            'num_format': '0.0000',
            'bg_color': '#d4edda',
            'border': 1
        })

        # === CREATE README SHEET ===
        if metadata:
            readme = workbook.add_worksheet('README')
            row = 0

            # Title
            readme.merge_range(row, 0, row, 5,
                             metadata.get('title', 'Meta-Analysis Results'),
                             title_format)
            readme.set_row(row, 25)
            row += 2

            # Generation info
            readme.write(row, 0, 'Generated:', section_format)
            readme.merge_range(row, 1, row, 5,
                             datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             text_format)
            row += 2

            # Summary
            if 'summary' in metadata:
                readme.merge_range(row, 0, row, 5, 'ANALYSIS SUMMARY', section_format)
                row += 1
                for key, value in metadata['summary'].items():
                    readme.write(row, 0, f"{key}:", text_format)
                    readme.merge_range(row, 1, row, 5, str(value), text_format)
                    row += 1
                row += 1

            # Sheet contents
            if 'sheets' in metadata:
                readme.merge_range(row, 0, row, 5, 'WORKBOOK CONTENTS', section_format)
                row += 1
                readme.write(row, 0, 'Sheet', header_format)
                readme.write(row, 1, 'Description', header_format)
                row += 1
                for sheet_name, desc in metadata['sheets'].items():
                    readme.write(row, 0, sheet_name, text_format)
                    readme.write(row, 1, desc, text_format)
                    row += 1
                row += 1

            # Column descriptions
            if 'columns' in metadata:
                readme.merge_range(row, 0, row, 5, 'COLUMN DESCRIPTIONS', section_format)
                row += 1
                readme.write(row, 0, 'Column', header_format)
                readme.write(row, 1, 'Description', header_format)
                row += 1
                for col, desc in metadata['columns'].items():
                    readme.write(row, 0, col, text_format)
                    readme.write(row, 1, desc, text_format)
                    readme.set_row(row, 30)
                    row += 1

            # Set column widths
            readme.set_column(0, 0, 25)
            readme.set_column(1, 5, 80)

        # === CREATE DATA SHEETS ===
        for sheet_name, df in data_dict.items():
            if sheet_name.lower() == 'readme':
                continue

            # Sanitize sheet name
            sheet_name = sheet_name[:31].replace('/', '_').replace('\\', '_')

            # Write data
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=1)
            worksheet = writer.sheets[sheet_name]

            # Format headers
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(1, col_num, value, header_format)
                worksheet.set_row(1, 30)

            # Format data columns
            for col_num, col in enumerate(df.columns):
                col_lower = col.lower()

                # Determine format based on column name
                if any(x in col_lower for x in ['p_value', 'pvalue', 'p-value']):
                    cell_format = pvalue_format
                    width = 12
                    # Highlight significant p-values
                    for row_num in range(len(df)):
                        value = df.iloc[row_num][col]
                        if pd.notna(value) and value < 0.05:
                            worksheet.write(row_num + 2, col_num, value, significant_format)
                        else:
                            worksheet.write(row_num + 2, col_num, value, cell_format)

                elif any(x in col_lower for x in ['k_studies', 'n_obs', 'df', 'n_']):
                    cell_format = integer_format
                    width = 10
                    for row_num in range(len(df)):
                        worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], cell_format)

                elif pd.api.types.is_numeric_dtype(df[col]):
                    cell_format = number_format
                    width = 14
                    for row_num in range(len(df)):
                        worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], cell_format)

                else:
                    cell_format = text_format
                    max_len = df[col].astype(str).str.len().max()
                    width = min(max_len + 2, 40)
                    for row_num in range(len(df)):
                        worksheet.write(row_num + 2, col_num, df.iloc[row_num][col], cell_format)

                worksheet.set_column(col_num, col_num, width)

            # Freeze panes
            worksheet.freeze_panes(2, 0)

            # Auto-filter
            worksheet.autofilter(1, 0, len(df) + 1, len(df.columns) - 1)

    # === DOWNLOAD ===
    buffer.seek(0)
    files.download(filename, buffer.read())

    return buffer.tell()


# ============================================================================
# UI HELPER FUNCTIONS
# ============================================================================

def create_download_section(title, icon='💾'):
    """Create styled section header for downloads."""
    display(HTML(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0 10px 0;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>
                {icon} {title}
            </h2>
        </div>
    """))


def create_success_message(filename, file_size=None):
    """Display success message after download."""
    size_text = f" ({file_size})" if file_size else ""
    display(HTML(f"""
        <div style='background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px 0;
                    color: #155724;'>
            <strong>✅ Download Complete!</strong><br>
            File: <code>{filename}</code>{size_text}<br>
            Check your browser's download folder.
        </div>
    """))


def create_error_message(error_msg):
    """Display error message if download fails."""
    display(HTML(f"""
        <div style='background-color: #f8d7da;
                    border: 1px solid #f5c6cb;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px 0;
                    color: #721c24;'>
            <strong>❌ Download Failed</strong><br>
            Error: {error_msg}<br>
            Please try again or check the console for details.
        </div>
    """))


def validate_download_data(data, expected_columns=None, min_rows=1):
    """
    Validate data before download.

    Returns: (is_valid, error_message)
    """

    if data is None:
        return False, "Data is None"

    if isinstance(data, pd.DataFrame):
        if len(data) < min_rows:
            return False, f"DataFrame has fewer than {min_rows} rows"

        if expected_columns:
            missing = set(expected_columns) - set(data.columns)
            if missing:
                return False, f"Missing required columns: {missing}"

        # Check for all-NaN columns
        all_nan_cols = data.columns[data.isna().all()].tolist()
        if all_nan_cols:
            return False, f"Columns with all missing values: {all_nan_cols}"

    elif isinstance(data, dict):
        if not data:
            return False, "Data dictionary is empty"

        for key, df in data.items():
            if isinstance(df, pd.DataFrame):
                is_valid, error = validate_download_data(df, min_rows=0)
                if not is_valid:
                    return False, f"Sheet '{key}': {error}"

    return True, None


# ============================================================================
# UNIFIED DOWNLOAD BUTTON CREATOR
# ============================================================================

def create_download_button(
    data,
    filename_base,
    title,
    description,
    includes_list,
    formats=['csv', 'excel'],
    metadata=None,
    expected_columns=None,
    button_style='info'
):
    """
    Create a complete download interface with format selection and button.

    Parameters:
    -----------
    data : pd.DataFrame or dict
        Data to download
    filename_base : str
        Base filename without extension
    title : str
        Title for the download card
    description : str
        User-friendly description
    includes_list : list
        List of items included in download
    formats : list
        Available formats: ['csv'], ['excel'], or ['csv', 'excel']
    metadata : dict
        Metadata dictionary
    expected_columns : list
        Required columns for validation
    button_style : str
        'info', 'success', or 'warning'
    """

    # Create styled card
    includes_html = '\n'.join([f'<li style="margin: 5px 0;">✓ {item}</li>'
                                for item in includes_list])

    display(HTML(f"""
        <div style='background-color: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 15px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
            <h3 style='color: #2d3748; margin-top: 0; font-size: 18px;'>
                {title}
            </h3>
            <p style='color: #4a5568; margin: 10px 0;'>
                {description}
            </p>
            <div style='background-color: #f7fafc;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 10px 0;'>
                <strong style='color: #2d3748;'>Includes:</strong>
                <ul style='margin: 5px 0; padding-left: 20px; color: #4a5568;'>
                    {includes_html}
                </ul>
            </div>
        </div>
    """))

    # Format selector (if multiple formats)
    if len(formats) > 1:
        format_widget = widgets.RadioButtons(
            options=[(f.upper(), f) for f in formats],
            value=formats[0],
            description='Format:',
            disabled=False,
            layout=widgets.Layout(width='200px')
        )
        display(format_widget)
    else:
        format_widget = None

    # Download button
    download_btn = widgets.Button(
        description=f'📥 Download',
        button_style=button_style,
        tooltip=description,
        icon='download',
        layout=widgets.Layout(width='300px', height='45px')
    )

    output_area = widgets.Output()

    # Click handler
    def on_download_click(b):
        with output_area:
            clear_output()

            try:
                # Validate data
                is_valid, error = validate_download_data(
                    data,
                    expected_columns=expected_columns,
                    min_rows=1
                )

                if not is_valid:
                    create_error_message(f"Data validation failed: {error}")
                    return

                # Get selected format
                if format_widget:
                    selected_format = format_widget.value
                else:
                    selected_format = formats[0]

                # Generate filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

                print(f"⏳ Preparing {selected_format.upper()} download...")

                if selected_format == 'csv':
                    filename = f"{filename_base}_{timestamp}.csv"
                    file_size = download_csv_with_metadata(data, filename, metadata)
                    size_str = f"{file_size/1024:.1f} KB"

                elif selected_format == 'excel':
                    filename = f"{filename_base}_{timestamp}.xlsx"
                    file_size = download_excel_with_formatting(data, filename, metadata)
                    size_str = f"{file_size/1024:.1f} KB"

                create_success_message(filename, size_str)

            except Exception as e:
                create_error_message(str(e))
                print("\nDetailed error trace:")
                print(traceback.format_exc())

    download_btn.on_click(on_download_click)

    # Display
    display(download_btn)
    display(output_area)


print("✅ Download helper functions loaded successfully!")
print("   Available functions:")
print("   - download_csv_with_metadata()")
print("   - download_excel_with_formatting()")
print("   - create_download_button()")
print("   - create_download_section()")
