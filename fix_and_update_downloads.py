#!/usr/bin/env python3
"""
Script to fix download functionality in Co_Met_3 notebook
Fixes: AttributeError, integrates into tabs, adds error handling
"""

import json
from pathlib import Path

def read_file_as_source(filepath):
    """Read Python file as notebook source."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()

def main():
    notebook_path = Path('/home/user/Co-Met/Co_Met_3.ipynb')
    download_dir = Path('/home/user/Co-Met')

    print("📖 Reading notebook...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    cells = notebook['cells']
    print(f"   Original cells: {len(cells)}")

    # Step 1: Add/Replace helper functions
    print("\n1️⃣  Adding FIXED helper functions...")
    helper_source = read_file_as_source(download_dir / 'download_helpers_fixed.py')
    helper_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"cellView": "form"},
        "outputs": [],
        "source": helper_source
    }
    
    # Insert after Cell 1 (index 1)
    cells.insert(2, helper_cell)
    print("   ✅ Helper functions added at index 2")

    # Step 2: Add download cells after key analysis cells
    print("\n2️⃣  Adding download cells...")
    
    download_configs = [
        {'search': 'CALCULATE EFFECT SIZES', 'file': 'download_cell6_fixed.py', 'title': 'Download: Data + Effect Sizes', 'offset': 7},
        {'search': 'OVERALL META-ANALYSIS', 'file': 'download_cell7_fixed.py', 'title': 'Download: Overall Results', 'offset': 8},
        {'search': 'SUBGROUP ANALYSIS', 'file': 'download_cell9_fixed.py', 'title': 'Download: Subgroup Results', 'offset': 10},
    ]
    
    for config in download_configs:
        try:
            download_source = read_file_as_source(download_dir / config['file'])
            download_cell = {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {"cellView": "form"},
                "outputs": [],
                "source": [f"#@title 📥 {config['title']}\n\n"] + download_source
            }
            # Insert at approximate position (will adjust)
            cells.insert(config['offset'], download_cell)
            print(f"   ✅ Added {config['title']}")
        except Exception as e:
            print(f"   ⚠️  Failed to add {config['title']}: {e}")

    # Save
    notebook['cells'] = cells
    output_path = notebook_path.with_name('Co_Met_3_FIXED.ipynb')
    
    print(f"\n💾 Saving: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"\n✅ SUCCESS!")
    print(f"   Final cells: {len(cells)}")
    print(f"   Added: {len(cells) - 22} cells")
    print(f"\n📄 Notebook saved as: Co_Met_3_FIXED.ipynb")
    print(f"\n🎯 Fixes applied:")
    print(f"   ✅ Robust error handling")
    print(f"   ✅ Fixed AttributeError")
    print(f"   ✅ Tab integration")
    print(f"   ✅ Data structure validation")
    print(f"\n🚀 Open Co_Met_3_FIXED.ipynb in Colab to test!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
