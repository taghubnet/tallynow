"""Disclaimer: The code in this file was mostly written by ChatGPT, 
with slight modifications to make it work as expected.
"""

import pandas as pd

def extract_casing_joints(excel_path, sheet_name, column_letter, start_row, end_row):
    # Convert the column letter to the appropriate column name
    column_name = ord(column_letter.upper()) - ord('A')

    # Load the specified sheet of the Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=[column_name], skiprows=start_row-1, nrows=end_row-start_row+1, header=None)

    # Get the column data
    column_data = df[column_name]

    # Initialize a list to hold the numbers
    numbers = []

    # Iterate over the column items
    for item in column_data:
        # Check if the item is a number (int or float)
        if isinstance(item, (int, float)):
            # Add the number to the list
            numbers.append(round(item, 2))

    # Return the list of numbers
    return numbers

def extract_deck_tally(excel_path, sheet_name, column_letter, start_row, end_row):
    # Convert the column letter to the appropriate column name
    column_name = ord(column_letter.upper()) - ord('A')

    # Load the specified sheet of the Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=[column_name], skiprows=start_row-1, nrows=end_row-start_row+1, header=None)

    # Get the column data
    column_data = df[column_name]

    # Initialize a list to hold the numbers
    numbers = []

    # Iterate over the column items
    for item in column_data:
        # Check if the item is a number (int or float)
        if isinstance(item, (int, float)):
            # Add the number to the list
            numbers.append(round(item, 3))
        else:
            numbers.append(item)

    # Return the list of numbers
    return numbers

def extract_ids(excel_path, sheet_name, column_letter, start_row, end_row):
    # Convert the column letter to the appropriate column name
    column_name = ord(column_letter.upper()) - ord('A')

    # Load the specified sheet of the Excel file
    df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=[column_name], skiprows=start_row-1, nrows=end_row-start_row+1, header=None)

    # Get the column data
    column_data = df[column_name]

    # Initialize a list to hold the numbers
    numbers = []

    # Iterate over the column items
    for item in column_data:
        # Check if the item is a number (int or float)
        if isinstance(item, (int, float)):
            # Add the number to the list
            numbers.append(round(item))

    # Return the list of numbers
    return numbers

def extract_excel_rows_to_list(excel_file_name):
    """
    Extracts the first 8 columns from each row in an Excel file into a list of lists.

    :param excel_file_name: The name of the Excel file.
    :return: A list of lists, where each sublist contains the data from one row.
    """
    # Read the Excel file, assuming the file is in the current working directory
    df = pd.read_excel(excel_file_name, usecols=range(8))

    # Convert the DataFrame to a NumPy array
    data_array = df.to_numpy()

    # Convert NaN values to None
    row_data = [[None if pd.isna(cell) else cell for cell in row] for row in data_array]

    return row_data
