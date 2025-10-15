"""
DataProcessor - A robust data processing and analysis class.
Handles data loading, cleaning, filtering, and statistical operations.
"""
import pandas as pd
import numpy as np
from typing import Union, Optional

class DataProcessor:
    """
    A comprehensive data processing toolkit for cleaning, filtering,
    and analyzing structured datasets.
    """
    
    def __init__(self):
        """Initialize DataProcessor with empty dataset."""
        self.data = None
        self._column_types = {}  # Cache for performance optimization
    
    def load_data(self, file_path: str) -> bool:
        """
        Load data from CSV file into pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            bool: True if successful
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is empty or invalid
        """
        try:
            self.data = pd.read_csv(file_path)
            self._precompute_column_types()
            print(f"Successfully loaded data with {len(self.data)} rows and {len(self.data.columns)} columns")
            return True
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("The file is empty.")
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def _precompute_column_types(self):
        """Precompute column types for performance optimization."""
        if self.data is not None:
            self._column_types = {
                col: str(self.data[col].dtype) for col in self.data.columns
            }
    
    def clean_data(self) -> int:
        """
        Remove rows with any missing values.
        
        Returns:
            int: Number of rows after cleaning
            
        Raises:
            ValueError: If no data is loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        initial_size = len(self.data)
        self.data = self.data.dropna()
        final_size = len(self.data)
        
        removed_count = initial_size - final_size
        print(f"Data cleaning: {removed_count} rows removed ({removed_count/initial_size*100:.1f}%)")
        
        self._precompute_column_types()
        return final_size
    
    def filter_by_value(self, column: str, value: Union[str, int, float]) -> int:
        """
        Filter dataset where column equals specified value.
        
        Args:
            column (str): Column name to filter on
            value: Value to match
            
        Returns:
            int: Number of rows after filtering
            
        Raises:
            ValueError: If column doesn't exist or no data loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data. Available columns: {list(self.data.columns)}")
        
        mask = self.data[column] == value
        self.data = self.data[mask]
        result_count = len(self.data)
        
        print(f"Filtered by {column}={value}: {result_count} rows match")
        return result_count
    
    def calculate_mean(self, column: str) -> float:
        """
        Calculate mean of a numeric column with validation.
        
        Args:
            column (str): Numeric column name
            
        Returns:
            float: Mean value
            
        Raises:
            ValueError: For various error conditions
            TypeError: For non-numeric columns
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        
        # Use cached type check for performance
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise TypeError(f"Column '{column}' is not numeric. Type: {self._column_types.get(column, 'unknown')}")
        
        if self.data[column].isnull().all():
            raise ValueError(f"Column '{column}' contains only null values.")
        
        # Handle partial nulls efficiently
        valid_data = self.data[column].dropna()
        if len(valid_data) == 0:
            raise ValueError(f"No valid numeric values in column '{column}'")
        
        return float(valid_data.mean())
    
    def find_max(self, column: str) -> float:
        """
        Find maximum value in a numeric column.
        
        Args:
            column (str): Numeric column name
            
        Returns:
            float: Maximum value
            
        Raises:
            ValueError: For various error conditions
            TypeError: For non-numeric columns
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data.")
        
        if not np.issubdtype(self.data[column].dtype, np.number):
            raise TypeError(f"Column '{column}' is not numeric. Type: {self._column_types.get(column, 'unknown')}")
        
        if self.data[column].isnull().all():
            raise ValueError(f"Column '{column}' contains only null values.")
        
        valid_data = self.data[column].dropna()
        return float(valid_data.max())
    
    def get_summary_stats(self) -> dict:
        """
        Generate comprehensive summary statistics for all numeric columns.
        
        Returns:
            dict: Summary statistics
            
        Raises:
            ValueError: If no data loaded
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
        
        numeric_columns = self.data.select_dtypes(include=[np.number]).columns
        summary = {}
        
        for col in numeric_columns:
            summary[col] = {
                'mean': float(self.data[col].mean()),
                'max': float(self.data[col].max()),
                'min': float(self.data[col].min()),
                'std': float(self.data[col].std()),
                'count': int(self.data[col].count())
            }
        
        return summary
    
    @property
    def shape(self) -> tuple:
        """Return current data shape (rows, columns)."""
        return self.data.shape if self.data is not None else (0, 0)
    
    @property
    def columns(self) -> list:
        """Return list of column names."""
        return list(self.data.columns) if self.data is not None else []