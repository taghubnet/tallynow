#!/usr/bin/env python3
"""
Convert Excel files to CSV format for TallyNow
This script converts all Excel sheets to individual CSV files
"""

import pandas as pd
import os
from pathlib import Path

def convert_excel_to_csv():
    """Convert all Excel files in sheets/ folder to CSV format"""
    
    sheets_dir = Path("sheets")
    csv_dir = Path("csv_sheets")
    
    # Create csv_sheets directory if it doesn't exist
    csv_dir.mkdir(exist_ok=True)
    
    # Excel files to convert
    excel_files = [
        "10 3-4 Tie-back Tally Test_Well_As Run.xlsx",
        "9 5-8 Liner Tally Test Well As Run.xlsx", 
        "assemblies_in_completion.xlsx",
        "tubing tallies.xlsx"
    ]
    
    for excel_file in excel_files:
        excel_path = sheets_dir / excel_file
        
        if not excel_path.exists():
            print(f"Warning: {excel_file} not found in sheets/ directory")
            continue
            
        print(f"Converting {excel_file}...")
        
        try:
            # Read all sheets from the Excel file
            xl_file = pd.ExcelFile(excel_path)
            
            for sheet_name in xl_file.sheet_names:
                # Read the sheet
                df = pd.read_excel(excel_path, sheet_name=sheet_name)
                
                # Create CSV filename
                base_name = excel_file.replace('.xlsx', '')
                csv_filename = f"{base_name}_{sheet_name}.csv"
                csv_path = csv_dir / csv_filename
                
                # Save as CSV
                df.to_csv(csv_path, index=False)
                print(f"  -> {csv_filename}")
                
        except Exception as e:
            print(f"Error converting {excel_file}: {e}")
    
    print(f"\nConversion complete! CSV files saved to {csv_dir}/")

if __name__ == "__main__":
    convert_excel_to_csv()