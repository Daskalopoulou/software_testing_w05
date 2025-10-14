#!/usr/bin/env python3
"""
Performance profiling and optimization analysis for DataProcessor.
Generates evidence for performance improvements and scalability testing.
"""
import cProfile
import pstats
import timeit
import pandas as pd
import numpy as np
import io
import time
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_processor import DataProcessor

def create_performance_dataset(rows=50000, null_frequency=0.1):
    """
    Create a realistic large dataset for performance testing.
    
    Args:
        rows (int): Number of rows to generate
        null_frequency (float): Frequency of null values (0-1)
    
    Returns:
        pd.DataFrame: Generated dataset
    """
    np.random.seed(42)  # For reproducible results
    
    data = {
        'user_id': range(rows),
        'age': np.random.randint(18, 80, rows),
        'income': np.random.normal(50000, 20000, rows),
        'score': np.random.exponential(2.0, rows),
        'department': np.random.choice(['Engineering', 'Marketing', 'Sales', 'HR'], rows),
        'is_active': np.random.choice([True, False], rows, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    
    # Introduce null values realistically
    null_mask = np.random.random(rows) < null_frequency
    df.loc[null_mask, 'income'] = np.nan
    df.loc[null_mask, 'score'] = np.nan
    
    print(f"Created performance dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Null values: {df.isnull().sum().sum()} total")
    
    return df

def profile_clean_data_operation():
    """Profile the clean_data method with detailed analysis."""
    print("=" * 60)
    print("PROFILING CLEAN_DATA OPERATION")
    print("=" * 60)
    
    processor = DataProcessor()
    processor.data = create_performance_dataset(10000)
    
    # Setup profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Execute operation multiple times for meaningful profiling
    for _ in range(100):
        processor.clean_data()
        # Reset data for next iteration
        processor.data = create_performance_dataset(10000)
    
    profiler.disable()
    
    # Analyze and print results
    print("\nTop 10 functions by cumulative time:")
    print("-" * 40)
    
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    print(stream.getvalue())
    
    return stats

def benchmark_operations():
    """Benchmark critical operations using timeit."""
    print("\n" + "=" * 60)
    print("BENCHMARKING CRITICAL OPERATIONS")
    print("=" * 60)
    
    processor = DataProcessor()
    test_datasets = {
        'Small (1K)': create_performance_dataset(1000),
        'Medium (10K)': create_performance_dataset(10000),
        'Large (50K)': create_performance_dataset(50000)
    }
    
    operations = [
        ('clean_data', 'processor.clean_data()'),
        ('calculate_mean', 'processor.calculate_mean("income")'),
        ('find_max', 'processor.find_max("score")'),
        ('filter_by_value', 'processor.filter_by_value("department", "Engineering")')
    ]
    
    benchmark_results = {}
    
    for dataset_name, dataset in test_datasets.items():
        print(f"\n{dataset_name} Dataset:")
        print("-" * 30)
        
        processor.data = dataset.copy()
        dataset_results = {}
        
        for op_name, op_code in operations:
            # Time the operation
            timer = timeit.Timer(op_code, globals={'processor': processor})
            
            # Run multiple times and take average
            number, time_taken = timer.autorange()
            avg_time = time_taken / number
            
            dataset_results[op_name] = avg_time
            print(f"  {op_name:20}: {avg_time:.6f} seconds")
            
            # Reset data after each operation
            processor.data = dataset.copy()
        
        benchmark_results[dataset_name] = dataset_results
    
    return benchmark_results

def memory_usage_analysis():
    """Analyze memory usage patterns."""
    print("\n" + "=" * 60)
    print("MEMORY USAGE ANALYSIS")
    print("=" * 60)
    
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    memory_samples = []
    
    processor = DataProcessor()
    
    # Measure memory at different stages
    memory_samples.append(('Initial', process.memory_info().rss / 1024 / 1024))
    
    processor.data = create_performance_dataset(10000)
    memory_samples.append(('After Data Load', process.memory_info().rss / 1024 / 1024))
    
    processor.clean_data()
    memory_samples.append(('After Cleaning', process.memory_info().rss / 1024 / 1024))
    
    processor.calculate_mean('income')
    memory_samples.append(('After Mean Calc', process.memory_info().rss / 1024 / 1024))
    
    print("Memory usage at different stages:")
    for stage, memory_mb in memory_samples:
        print(f"  {stage:20}: {memory_mb:.2f} MB")
    
    return memory_samples

def scalability_analysis():
    """Analyze how performance scales with dataset size."""
    print("\n" + "=" * 60)
    print("SCALABILITY ANALYSIS")
    print("=" * 60)
    
    dataset_sizes = [1000, 5000, 10000, 25000, 50000]
    clean_times = []
    mean_times = []
    
    for size in dataset_sizes:
        processor = DataProcessor()
        processor.data = create_performance_dataset(size)
        
        # Time clean_data
        clean_time = timeit.timeit(
            'processor.clean_data()', 
            globals=locals(), 
            number=10
        ) / 10
        
        # Time calculate_mean
        processor.data = create_performance_dataset(size)
        mean_time = timeit.timeit(
            'processor.calculate_mean("income")', 
            globals=locals(), 
            number=100
        ) / 100
        
        clean_times.append(clean_time)
        mean_times.append(mean_time)
        
        print(f"Size {size:6}: clean_data={clean_time:.4f}s, mean_calc={mean_time:.6f}s")
    
    # Calculate scaling factors
    if len(dataset_sizes) > 1:
        clean_scaling = clean_times[-1] / clean_times[0]
        mean_scaling = mean_times[-1] / mean_times[0]
        size_scaling = dataset_sizes[-1] / dataset_sizes[0]
        
        print(f"\nScaling Analysis:")
        print(f"  Dataset size increased by: {size_scaling:.1f}x")
        print(f"  clean_data time increased by: {clean_scaling:.1f}x")
        print(f"  calculate_mean time increased by: {mean_scaling:.1f}x")
    
    return {
        'sizes': dataset_sizes,
        'clean_times': clean_times,
        'mean_times': mean_times
    }

def generate_performance_report():
    """Generate comprehensive performance report."""
    print("DATA PROCESSOR PERFORMANCE ANALYSIS REPORT")
    print("=" * 60)
    print(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all analyses
    profile_stats = profile_clean_data_operation()
    benchmark_results = benchmark_operations()
    memory_usage = memory_usage_analysis()
    scalability_data = scalability_analysis()
    
    print("\n" + "=" * 60)
    print("PERFORMANCE SUMMARY")
    print("=" * 60)
    
    # Summary insights
    small_mean_time = benchmark_results['Small (1K)']['calculate_mean']
    large_mean_time = benchmark_results['Large (50K)']['calculate_mean']
    scaling_factor = large_mean_time / small_mean_time
    
    print(f"Performance Insights:")
    print(f"  • Mean calculation on 50K dataset: {large_mean_time:.6f}s")
    print(f"  • Scaling factor (1K to 50K): {scaling_factor:.1f}x")
    print(f"  • Peak memory usage: {max(mem for _, mem in memory_usage):.1f} MB")
    
    # Optimization recommendations
    print(f"\nOptimization Recommendations:")
    print(f"  • Consider caching for frequently accessed columns")
    print(f"  • Implement chunk processing for very large datasets")
    print(f"  • Use more efficient data types where possible")
    
    return {
        'profile': profile_stats,
        'benchmarks': benchmark_results,
        'memory': memory_usage,
        'scalability': scalability_data
    }

if __name__ == "__main__":
    # Check if detailed profiling is requested
    detailed = '--detailed' in sys.argv
    
    if detailed:
        report = generate_performance_report()
        print("\nDetailed performance report completed.")
    else:
        # Quick benchmark only
        benchmark_operations()
        print("\nQuick benchmark completed. Use --detailed for full analysis.")