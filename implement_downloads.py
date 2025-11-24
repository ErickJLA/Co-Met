#!/usr/bin/env python3
"""
Script to automatically add download functionality to Co_Met_3.ipynb
Inserts helper functions and download buttons at strategic locations
"""

import json
import sys
from pathlib import Path

def read_file_as_source(filepath):
    """Read a Python file and convert to notebook source format (list of lines)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Keep newlines at end of each line
    return lines

def create_code_cell(source_lines):
    """Create a notebook code cell with given source."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }

def insert_cell_after_index(cells, index, new_cell):
    """Insert a new cell after the specified index."""
    cells.insert(index + 1, new_cell)
    return cells

def append_to_cell(cell, source_lines):
    """Append source lines to an existing cell."""
    # Add separator
    cell['source'].extend([
        "\n",
        "# " + "="*76 + "\n",
        "# DOWNLOAD BUTTON\n",
        "# " + "="*76 + "\n",
        "\n"
    ])
    # Add new source
    cell['source'].extend(source_lines)
    return cell

def main():
    # Paths
    notebook_path = Path('/home/user/Co-Met/Co_Met_3.ipynb')
    download_dir = Path('/home/user/Co-Met')

    # Read notebook
    print(f"📖 Reading notebook: {notebook_path}")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    initial_cell_count = len(cells)
    print(f"   Initial cell count: {initial_cell_count}")

    # Track adjustments for cell indices (as we insert cells, indices shift)
    offset = 0

    # ==========================================================================
    # 1. INSERT HELPER FUNCTIONS AFTER CELL 1
    # ==========================================================================
    print("\n1️⃣  Inserting helper functions after Cell 1...")
    helper_source = read_file_as_source(download_dir / 'download_cell_after_cell1_helpers.py')
    helper_cell = create_code_cell(helper_source)
    cells = insert_cell_after_index(cells, 1 + offset, helper_cell)
    offset += 1
    print(f"   ✅ Helper functions inserted (new cell at index {1 + offset})")

    # ==========================================================================
    # 2. APPEND TO CELL 6: Data + Effect Sizes
    # ==========================================================================
    print("\n2️⃣  Adding download to Cell 6 (Calculate Effect Sizes)...")
    cell6_index = 6 + offset
    cell6_source = read_file_as_source(download_dir / 'download_cell6_data_effectsizes.py')
    cells[cell6_index] = append_to_cell(cells[cell6_index], cell6_source)
    print(f"   ✅ Download code appended to Cell {cell6_index}")

    # ==========================================================================
    # 3. APPEND TO CELL 7: Overall Meta-Analysis Results
    # ==========================================================================
    print("\n3️⃣  Adding download to Cell 7 (Overall Meta-Analysis)...")
    cell7_index = 7 + offset
    cell7_source = read_file_as_source(download_dir / 'download_cell7_overall_results.py')
    cells[cell7_index] = append_to_cell(cells[cell7_index], cell7_source)
    print(f"   ✅ Download code appended to Cell {cell7_index}")

    # ==========================================================================
    # 4. APPEND TO CELL 9: Subgroup Analysis Results
    # ==========================================================================
    print("\n4️⃣  Adding download to Cell 9 (Subgroup Analysis)...")
    cell9_index = 9 + offset
    cell9_source = read_file_as_source(download_dir / 'download_cell9_subgroup_results.py')
    cells[cell9_index] = append_to_cell(cells[cell9_index], cell9_source)
    print(f"   ✅ Download code appended to Cell {cell9_index}")

    # ==========================================================================
    # 5. APPEND TO CELL 12: Meta-Regression
    # ==========================================================================
    print("\n5️⃣  Adding download to Cell 12 (Meta-Regression)...")
    cell12_index = 12 + offset
    cell12_source = read_file_as_source(download_dir / 'download_cell12_meta_regression.py')
    cells[cell12_index] = append_to_cell(cells[cell12_index], cell12_source)
    print(f"   ✅ Download code appended to Cell {cell12_index}")

    # ==========================================================================
    # 6. APPEND TO CELL 16: Publication Bias
    # ==========================================================================
    print("\n6️⃣  Adding download to Cell 16 (Publication Bias)...")
    cell16_index = 16 + offset
    cell16_source = read_file_as_source(download_dir / 'download_cell16_publication_bias.py')
    cells[cell16_index] = append_to_cell(cells[cell16_index], cell16_source)
    print(f"   ✅ Download code appended to Cell {cell16_index}")

    # ==========================================================================
    # 7. APPEND TO CELL 19: Leave-One-Out Sensitivity
    # ==========================================================================
    print("\n7️⃣  Adding download to Cell 19 (Sensitivity Analysis)...")
    cell19_index = 19 + offset
    cell19_source = read_file_as_source(download_dir / 'download_cell19_sensitivity_analysis.py')
    cells[cell19_index] = append_to_cell(cells[cell19_index], cell19_source)
    print(f"   ✅ Download code appended to Cell {cell19_index}")

    # ==========================================================================
    # 8. INSERT NEW CELL 22: Complete Package
    # ==========================================================================
    print("\n8️⃣  Inserting NEW Cell 22 (Complete Package)...")
    cell22_source = read_file_as_source(download_dir / 'download_cell22_complete_package.py')
    cell22 = create_code_cell(cell22_source)
    cells.append(cell22)
    print(f"   ✅ Complete Package cell added (index {len(cells)-1})")

    # Update notebook
    notebook['cells'] = cells

    # Save modified notebook
    output_path = notebook_path.with_name('Co_Met_3_with_downloads.ipynb')
    print(f"\n💾 Saving modified notebook: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    final_cell_count = len(cells)
    print(f"\n✅ SUCCESS!")
    print(f"   Original cells: {initial_cell_count}")
    print(f"   Final cells: {final_cell_count}")
    print(f"   Cells added: {final_cell_count - initial_cell_count}")
    print(f"   Download points: 7 appended + 1 new cell = 8 total")
    print(f"\n📄 New notebook saved as: Co_Met_3_with_downloads.ipynb")
    print(f"\n🎯 Next steps:")
    print(f"   1. Open Co_Met_3_with_downloads.ipynb in Google Colab")
    print(f"   2. Run all cells")
    print(f"   3. See download buttons appear after analysis cells!")
    print(f"\n🎉 Download functionality successfully implemented!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
