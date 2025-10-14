# data_processor.py
import pandas as pd
import numpy as np

class DataProcessor:
    """
    A class to process and analyze dataset.
    """
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        """Loads data from a CSV file."""
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("The file is empty.")
        return True

    def clean_data(self):
        """Removes rows with any missing values."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        # This is intentionally simple; we can profile this later
        initial_size = len(self.data)
        self.data = self.data.dropna()
        final_size = len(self.data)
        print(f"Cleaned data: {initial_size - final_size} rows removed.")
        return final_size

    def filter_by_value(self, column, value):
        """Filters the dataset where column equals value."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        self.data = self.data[self.data[column] == value]
        return len(self.data)

    def calculate_mean(self, column):
        """Calculates the mean of a numeric column."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise TypeError(f"Column '{column}' is not numeric.")
        if self.data[column].isnull().all():
            raise ValueError(f"Column '{column}' contains only null values.")
        # This is a good candidate for performance checking
        return self.data[column].mean()

    def find_max(self, column):
        """Finds the maximum value in a column."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise TypeError(f"Column '{column}' is not numeric.")
        if self.data[column].isnull().all():
            raise ValueError(f"Column '{column}' contains only null values.")
        return self.data[column].max()