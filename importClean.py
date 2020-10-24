import pandas as pd
import numpy as np


def load_data_frame(fileName):
    """Loads dataframe from specified file"""
    try:
        df = pd.read_csv(fileName)
    except Exception as e:
        print("File not found")
    return formattingData(df)


def formattingData(df):
    """This formats the necessary data"""
    # Check age column
    df["age"] = df.age.apply(np.ceil)  # Applies ceiling to the age column
    # Check platelets column (Not sure if should do this or not)
    df["platelets"] = df.platelets.apply(np.floor)  # Applies floor to the platelets column
    return df


def addRowIndex(df):
    """This adds an additional index row to the dataset for viewing"""
    add_row_index = []
    for i in range(1, len(df) + 1):
        add_row_index.append(i)
    df.insert(0, "row", add_row_index, True)
    return df
