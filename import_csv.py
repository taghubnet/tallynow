"""
CSV import functions for TallyNow
Replaces Excel-based import_casing.py with CSV functionality
"""

import pandas as pd

def extract_casing_joints(csv_path, column_letter, start_row, end_row):
    """Extract casing joints from CSV file"""
    # Convert the column letter to column index
    column_index = ord(column_letter.upper()) - ord('A')
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Get the column by index (0-based)
    if column_index >= len(df.columns):
        raise ValueError(f"Column {column_letter} not found in CSV file")
    
    column_name = df.columns[column_index]
    
    # Extract the specified rows (convert to 0-based indexing)
    start_idx = start_row - 1
    end_idx = end_row - 1
    
    if start_idx < 0 or end_idx >= len(df):
        raise ValueError(f"Row range {start_row}-{end_row} is out of bounds")
    
    # Get the column data for the specified range
    column_data = df[column_name].iloc[start_idx:end_idx+1]
    
    # Initialize a list to hold the numbers
    numbers = []
    
    # Iterate over the column items
    for item in column_data:
        # Try to convert to float first
        if pd.notna(item):
            try:
                # Try to convert to float
                float_val = float(item)
                numbers.append(round(float_val, 2))
            except (ValueError, TypeError):
                # Skip non-numeric values
                pass
    
    return numbers

def extract_deck_tally(csv_path, column_letter, start_row, end_row):
    """Extract deck tally from CSV file"""
    # Convert the column letter to column index
    column_index = ord(column_letter.upper()) - ord('A')
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Get the column by index
    if column_index >= len(df.columns):
        raise ValueError(f"Column {column_letter} not found in CSV file")
    
    column_name = df.columns[column_index]
    
    # Extract the specified rows (convert to 0-based indexing)
    start_idx = start_row - 1
    end_idx = end_row - 1
    
    if start_idx < 0 or end_idx >= len(df):
        raise ValueError(f"Row range {start_row}-{end_row} is out of bounds")
    
    # Get the column data for the specified range
    column_data = df[column_name].iloc[start_idx:end_idx+1]
    
    # Initialize a list to hold the values
    values = []
    
    # Iterate over the column items
    for item in column_data:
        # Try to convert to float first
        if pd.notna(item):
            try:
                # Try to convert to float
                float_val = float(item)
                values.append(round(float_val, 3))
            except (ValueError, TypeError):
                # If conversion fails, keep original value
                values.append(item)
        else:
            values.append(item)
    
    return values

def extract_ids(csv_path, column_letter, start_row, end_row):
    """Extract IDs from CSV file"""
    # Convert the column letter to column index
    column_index = ord(column_letter.upper()) - ord('A')
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Get the column by index
    if column_index >= len(df.columns):
        raise ValueError(f"Column {column_letter} not found in CSV file")
    
    column_name = df.columns[column_index]
    
    # Extract the specified rows (convert to 0-based indexing)
    start_idx = start_row - 1
    end_idx = end_row - 1
    
    if start_idx < 0 or end_idx >= len(df):
        raise ValueError(f"Row range {start_row}-{end_row} is out of bounds")
    
    # Get the column data for the specified range
    column_data = df[column_name].iloc[start_idx:end_idx+1]
    
    # Initialize a list to hold the numbers
    numbers = []
    
    # Iterate over the column items
    for item in column_data:
        # Try to convert to float first
        if pd.notna(item):
            try:
                # Try to convert to float
                float_val = float(item)
                numbers.append(round(float_val))
            except (ValueError, TypeError):
                # Skip non-numeric values
                pass
    
    return numbers

def extract_csv_rows_to_list(csv_file_name):
    """
    Extracts the first 8 columns from each row in a CSV file into a list of lists.
    
    :param csv_file_name: The name of the CSV file.
    :return: A list of lists, where each sublist contains the data from one row.
    """
    # Read the CSV file, taking only the first 8 columns
    df = pd.read_csv(csv_file_name, usecols=range(8))
    
    # Convert the DataFrame to a NumPy array
    data_array = df.to_numpy()
    
    # Convert NaN values to None
    row_data = [[None if pd.isna(cell) else cell for cell in row] for row in data_array]
    
    return row_data