"""
Shared pytest fixtures for DataProcessor tests.
"""
import pytest
import pandas as pd
import tempfile
import os

@pytest.fixture
def sample_dataframe():
    """Provides a sample DataFrame for standard tests."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'value': [10.5, 20.3, None, 40.7, 50.1],
        'category': ['A', 'B', 'A', None, 'B'],
        'score': [100, 200, 150, 300, 250]
    })

@pytest.fixture
def temp_csv_file(tmp_path, sample_dataframe):
    """Creates a temporary CSV file for testing load_data."""
    file = tmp_path / "test_data.csv"
    sample_dataframe.to_csv(file, index=False)
    return str(file)

@pytest.fixture
def empty_dataframe():
    """Provides an empty DataFrame for edge case testing."""
    return pd.DataFrame()

@pytest.fixture
def all_nulls_dataframe():
    """Provides a DataFrame with all null values."""
    return pd.DataFrame({
        'col1': [None, None, None],
        'col2': [None, None, None]
    })