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
def large_performance_data():
    """Provides a large DataFrame for performance testing."""
    return pd.DataFrame({
        'numeric_col': range(10000),
        'float_col': [x * 1.5 for x in range(10000)],
        'category_col': ['A', 'B', 'C'] * 3334  # Approximately 10000 rows
    })

@pytest.fixture
def temp_csv_file(sample_dataframe):
    """Creates a temporary CSV file for testing load_data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        sample_dataframe.to_csv(f.name, index=False)
        temp_path = f.name
    
    yield temp_path
    # Cleanup
    os.unlink(temp_path)

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