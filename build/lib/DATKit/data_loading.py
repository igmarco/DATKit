import pandas as pd
import os


def load_data(file_names, format_list):
    """
    Loads multiple DataFrames from a list of file names (CSV or Excel).

    Parameters
    ----------
    file_names : list of str
        A list of file paths or names of the files to be loaded.
    format_list : list of dicts, default=[]
        List of dicts containing:
        - 'delimiter': The delimiter used in CSV files (e.g., ";" for semicolon-separated files).
        - 'decimal': The decimal point character used in CSV files (e.g., "," for European format_element).

    Returns
    -------
    dataframes : list of pandas.DataFrame
        A list of DataFrames loaded from the specified files.

    Raises
    ------
    FileNotFoundError
        If one or more files in the list cannot be found.
    pd.errors.ParserError
        If there is an error while parsing one of the files.
    ValueError
        If the file format_element is unsupported or the sheet name is invalid.
    """
    dataframes = []

    # Build format_list if not provided
    if not format_list:
        format_list = [{'delimiter': ",", 'decimal': "."} for _ in range(len(file_names))]

    for file_name, format_element in zip(file_names, format_list):

        try:
            if '.xlsx' in file_name or '.xls' in file_name:  # Check if it's an Excel file
                # Check if a sheet name is specified in the format_element
                if '#' in file_name:
                    # Split the file name and sheet name
                    base_file_name, sheet_name = file_name.split('#')
                    sheet_name = sheet_name.strip()  # Clean any extra spaces
                    # base_file_path = os.path.join(os.path.dirname(__file__), base_file_name)
                    # df = pd.read_excel(base_file_path, sheet_name=sheet_name, decimal=format_element['decimal'])
                    df = pd.read_excel(base_file_name, sheet_name=sheet_name, decimal=format_element['decimal'])
                else:
                    file_path = os.path.join(os.path.dirname(__file__), file_name)
                    df = pd.read_excel(file_path, decimal=format_element['decimal'])

            else:  # If it's a CSV file
                # file_path = os.path.join(os.path.dirname(__file__), file_name)
                # df = pd.read_csv(file_path, delimiter=format_element['delimiter'], decimal=format_element['decimal'])
                df = pd.read_csv(file_name, delimiter=format_element['delimiter'], decimal=format_element['decimal'])

            dataframes.append(df)

        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_name}' was not found.")

        except pd.errors.ParserError as e:
            raise pd.errors.ParserError(f"Error parsing the file '{file_name}': {e}")

        except ValueError as ve:
            raise ValueError(f"Error loading the file '{file_name}': {ve}")

    return dataframes
