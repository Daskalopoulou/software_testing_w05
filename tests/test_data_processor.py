"""
Comprehensive test suite for DataProcessor class.
"""
import pytest
import pandas as pd
import numpy as np
from src.data_processor import DataProcessor
import time

class TestDataProcessorBasic:
    """Test basic functionality and initialization."""
    
    def test_initialization(self):
        """Test that DataProcessor initializes correctly."""
        processor = DataProcessor()
        assert processor.data is None
        assert processor.shape == (0, 0)
        assert processor.columns == []
    
    def test_import_success(self):
        """Test that the module can be imported successfully."""
        try:
            from src.data_processor import DataProcessor
            processor = DataProcessor()
            assert processor is not None
        except ImportError as e:
            pytest.fail(f"Failed to import DataProcessor: {e}")

class TestDataLoading:
    """Test data loading functionality."""
    
    def test_load_data_success(self, temp_csv_file):
        """Test successfully loading data from a CSV file."""
        processor = DataProcessor()
        result = processor.load_data(temp_csv_file)
        
        assert result is True
        assert processor.data is not None
        assert len(processor.data) == 5
        assert processor.shape == (5, 4)
        assert 'id' in processor.columns
    
    def test_load_data_file_not_found(self):
        """Test loading data with a non-existent file."""
        processor = DataProcessor()
        with pytest.raises(FileNotFoundError):
            processor.load_data("non_existent_file.csv")
    
    def test_load_data_empty_file(self, tmp_path):
        """Test loading an empty CSV file."""
        empty_file = tmp_path / "empty.csv"
        empty_file.write_text("")
        
        processor = DataProcessor()
        with pytest.raises(ValueError, match="empty"):
            processor.load_data(str(empty_file))

class TestDataCleaning:
    """Test data cleaning functionality."""
    
    def test_clean_data_removes_nulls(self, sample_dataframe):
        """Test that clean_data removes rows with null values."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()
        initial_rows = len(processor.data)

        final_rows = processor.clean_data()

        assert final_rows == 3  # 2 rows with nulls should be removed
        assert len(processor.data) == 3
        assert processor.data.isnull().sum().sum() == 0
    
    def test_clean_data_no_data_loaded(self):
        """Test clean_data when no data is loaded."""
        processor = DataProcessor()
        with pytest.raises(ValueError, match="No data loaded"):
            processor.clean_data()
    
    def test_clean_all_nulls_dataframe(self, all_nulls_dataframe):
        """Test cleaning a dataframe with all null values."""
        processor = DataProcessor()
        processor.data = all_nulls_dataframe.copy()
        
        cleaned_count = processor.clean_data()
        
        assert cleaned_count == 0
        assert len(processor.data) == 0

class TestDataFiltering:
    """Test data filtering functionality."""
    
    def test_filter_by_value_success(self, sample_dataframe):
        """Test filtering data by a specific value."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()

        result_count = processor.filter_by_value('category', 'A')

        assert result_count == 2
        assert all(processor.data['category'] == 'A')
    
    def test_filter_by_value_column_not_found(self, sample_dataframe):
        """Test filtering with a non-existent column."""
        processor = DataProcessor()
        processor.data = sample_dataframe
        with pytest.raises(ValueError, match="Column 'unknown' not found"):
            processor.filter_by_value('unknown', 'value')
    
    def test_filter_by_numeric_value(self, sample_dataframe):
        """Test filtering by numeric value."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()
        
        result_count = processor.filter_by_value('id', 1)
        
        assert result_count == 1
        assert processor.data['id'].iloc[0] == 1

class TestStatisticalOperations:
    """Test statistical calculation methods."""
    
    def test_calculate_mean_success(self, sample_dataframe):
        """Test calculating the mean of a numeric column."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()
        processor.clean_data()  # Clean data first

        mean_value = processor.calculate_mean('value')
        # After cleaning, values are [10.5, 40.7, 50.1] - mean is (10.5 + 40.7 + 50.1) / 3
        expected_mean = (10.5 + 40.7 + 50.1) / 3  # This equals 33.76666666666667

        assert mean_value == pytest.approx(expected_mean)
    
    def test_calculate_mean_non_numeric_column(self, sample_dataframe):
        """Test calculating mean on a non-numeric column."""
        processor = DataProcessor()
        processor.data = sample_dataframe
        with pytest.raises(TypeError, match="not numeric"):
            processor.calculate_mean('category')
    
    def test_calculate_mean_all_null_column(self):
        """Test calculating mean on a column with all null values."""
        processor = DataProcessor()
        # Create a dataframe with a numeric column that has all nulls
        # We need to explicitly set the dtype to float to ensure it's numeric
        processor.data = pd.DataFrame({
            'numeric_col': pd.Series([None, None, None], dtype=float)
        })
        with pytest.raises(ValueError, match="only null values"):
            processor.calculate_mean('numeric_col')
    
    def test_find_max_success(self, sample_dataframe):
        """Test finding the maximum value in a column."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()
        processor.clean_data()

        max_value = processor.find_max('value')
        assert max_value == 50.1
    
    def test_find_max_with_nulls(self, sample_dataframe):
        """Test finding max in column with some null values."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()  # Don't clean to keep nulls
        
        max_value = processor.find_max('score')
        assert max_value == 300  # Should ignore nulls

class TestSummaryStatistics:
    """Test summary statistics generation."""
    
    def test_get_summary_stats_success(self, sample_dataframe):
        """Test generating summary statistics."""
        processor = DataProcessor()
        processor.data = sample_dataframe.copy()
        processor.clean_data()
        
        stats = processor.get_summary_stats()
        
        assert 'value' in stats
        assert 'score' in stats
        assert 'mean' in stats['value']
        assert 'max' in stats['value']
        assert 'min' in stats['value']
        assert stats['value']['count'] == 3
    
    def test_get_summary_stats_no_data(self):
        """Test summary stats with no data loaded."""
        processor = DataProcessor()
        with pytest.raises(ValueError, match="No data loaded"):
            processor.get_summary_stats()

class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_dataframe_operations(self, empty_dataframe):
        """Test operations on empty dataframe."""
        processor = DataProcessor()
        processor.data = empty_dataframe
        
        # For empty dataframe, any column won't be found
        with pytest.raises(ValueError, match="Column 'any_column' not found"):
            processor.calculate_mean('any_column')
    
    def test_single_row_dataframe(self):
        """Test operations on single-row dataframe."""
        processor = DataProcessor()
        processor.data = pd.DataFrame({'col': [42]})
        
        assert processor.calculate_mean('col') == 42.0
        assert processor.find_max('col') == 42
        assert processor.shape == (1, 1)
    
    def test_large_integer_handling(self):
        """Test handling of large integer values."""
        large_values = [10**i for i in range(6)]  # 1 to 100000
        processor = DataProcessor()
        processor.data = pd.DataFrame({'large_col': large_values})
        
        mean = processor.calculate_mean('large_col')
        max_val = processor.find_max('large_col')
        
        assert mean == sum(large_values) / len(large_values)
        assert max_val == 100000

class TestPerformance:
    """Performance and scalability tests."""
    
    def test_mean_calculation_performance(self):
        """Test performance of mean calculation on large dataset."""
        processor = DataProcessor()
        # Create a simple large dataset without using the problematic fixture
        large_data = pd.DataFrame({
            'numeric_col': range(10000)
        })
        processor.data = large_data.copy()
        
        start_time = time.time()
        mean_value = processor.calculate_mean('numeric_col')
        end_time = time.time()
        
        execution_time = end_time - start_time
        # Should complete in reasonable time (adjust threshold as needed)
        assert execution_time < 1.0  # 1 second threshold
        assert mean_value == pytest.approx(4999.5)  # mean of 0-9999

class TestCICDValidation:
    """Tests specifically for CI/CD pipeline validation."""
    
    def test_module_structure(self):
        """Verify module has required classes and methods."""
        from src.data_processor import DataProcessor
        
        # Check required methods exist
        required_methods = ['load_data', 'clean_data', 'calculate_mean', 'find_max', 'get_summary_stats']
        for method in required_methods:
            assert hasattr(DataProcessor, method), f"Missing method: {method}"
    
    def test_error_messages_consistent(self):
        """Test that error messages are consistent and informative."""
        processor = DataProcessor()
        
        with pytest.raises(ValueError, match="No data loaded"):
            processor.clean_data()
        
        processor.data = pd.DataFrame({'col': [1, 2, 3]})
        with pytest.raises(ValueError, match="Column 'missing' not found"):
            processor.calculate_mean('missing')

def test_coverage_completeness():
    """Test to ensure all major code paths are covered."""
    processor = DataProcessor()
    
    # Test initial state
    assert processor.data is None
    assert processor._column_types == {}
    
    # Test property accessors on uninitialized processor
    assert processor.shape == (0, 0)
    assert processor.columns == []