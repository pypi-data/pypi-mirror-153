import pandas as pd

def importing_data(file_name):
    """
    This function imports the data from the csv file.
    """
    data = pd.read_csv(file_name)
    return data

def duplicate_count(data):
    """
    This function counts the number of duplicates in the data.
    """
    count = data.duplicated().sum()
    return count

def drop_duplicates(data):
    """
    This function drops the duplicates from the data.
    """
    data = data.drop_duplicates()
    return data 