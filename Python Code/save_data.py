# -*- coding: utf-8 -*-
"""
This function takes three arguments: the list of dictionaries containing the
data to be saved, the filename for the CSV file, and the filename for the Excel
file. It first converts the list of dictionaries to a Pandas DataFrame using
the from_records method. The resulting DataFrame will have columns
corresponding to the keys in the dictionaries.

Then, the function saves the DataFrame to a CSV file using the to_csv method
and the specified filename. The index=False argument tells the method not to
include the row index in the output. Similarly, it saves the DataFrame to an
Excel file using the to_excel method and the specified filename.
"""

import pandas as pd

def save_dicts_to_files(data_list, csv_filename, excel_filename):
    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame.from_records(data_list)

    # Save the DataFrame to a CSV file
    df.to_csv(csv_filename, index=False)

    # Save the DataFrame to an Excel file
    df.to_excel(excel_filename, index=False)

    
    return


