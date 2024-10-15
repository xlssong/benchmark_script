#This is to anyalyze GB result generated from geekbench.exe --export-txt output
#extract_performance_scores() function check output text file and extract into performance_scores_dict, benchmark_scores_dict
#average_geekbench_scores() function calls extract_performance_scores(), and go through all files in the file_folder with name format
#geekbench_*.txt, and return average_performance_scores, average_benchmark_scores
#main function calls average_geekbench_scores() and print average result.
#log format and debug level need to be considered.

import re
import os
import csv
import glob
from collections import defaultdict

def write_to_csv(file_path, headers, data):
    # Check if the file already exists
    file_exists = os.path.isfile(file_path)
    
    # Open the file in append mode
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # If the file does not exist, write the header
        if not file_exists:
            writer.writerow(headers)
        
        # Write the data
        writer.writerow(data)

def extract_performance_scores(file_path):
    # Read file content
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Define regex pattern
    # Extract content under "Multi-Core Performance" section
    core_performance_section = re.search(r"(Multi-Core Performance|Single-Core Performance)\s*([\s\S]+?)\n{2,}Benchmark Summary", text)
    performance_scores_dict = {}
    if core_performance_section:
        # Get the text for the performance scores part
        performance_text = core_performance_section.group(0)

        # Match performance score names and values
        performance_score_pattern = re.compile(r"([^\n]+?)\s+(\d+)\s*\|*\s*\n", re.MULTILINE)
        performance_scores = performance_score_pattern.findall(performance_text)
        performance_scores_dict = {name.strip(): score for name, score in performance_scores}

    # Find "Benchmark Summary" part
    benchmark_summary_pattern = re.compile(r"Benchmark Summary\s*([\s\S]+)$", re.MULTILINE)
    benchmark_summary_match = benchmark_summary_pattern.search(text)
    benchmark_scores_dict = {}
    if benchmark_summary_match:
        # Get the text for the Benchmark Summary part
        benchmark_text = benchmark_summary_match.group(1)
        # Define regex to match all score names and their values
        benchmark_score_pattern = r'([\w\s-]+?)\s+(\d+)\n'
        # Use findall to match all scores
        benchmark_scores = re.findall(benchmark_score_pattern, benchmark_text)
        benchmark_scores_dict = {name.strip(): score for name, score in benchmark_scores}
    
    print("\n====Result file: ", file_path)
    print("Performance Scores:")
    for test_name, score in performance_scores_dict.items():
        print(f"{test_name}: {score}")
    print("\nBenchmark Summary Scores:")
    for test_name, score in benchmark_scores_dict.items():
        print(f"{test_name} Score: {score}")

    return performance_scores_dict, benchmark_scores_dict



def average_geekbench_scores(result_dir, output_csv):
    # Initialize score accumulation dictionaries
    total_performance_scores = defaultdict(int)
    total_benchmark_scores = defaultdict(int)
    file_count = 0

    pattern = os.path.join(result_dir, 'result_file_*.txt')
    gb_result_files = glob.glob(pattern)

    # Prepare headers for the CSV file
    headers_written = False
    headers = []


    # Iterate through all result files in the directory
    for gb_result_file in gb_result_files:
        performance_scores_dict, benchmark_scores_dict = extract_performance_scores(gb_result_file)
        
        # Accumulate scores
        for test_name, score in performance_scores_dict.items():
            total_performance_scores[test_name] += int(score)
        for test_name, score in benchmark_scores_dict.items():
            total_benchmark_scores[test_name] += int(score)
        
        file_count += 1

        # Prepare data for CSV
        if not headers_written:
            headers = ['Test Name'] + [f'Run {i+1}' for i in range(file_count)]
            headers_written = True
        
        data = [test_name] + list(performance_scores_dict.values()) + list(benchmark_scores_dict.values())
        
        # Write to CSV
        write_to_csv(output_csv, headers, data)
  
    # Calculate average scores
    average_performance_scores = {test_name: total_score / file_count for test_name, total_score in total_performance_scores.items()}
    average_benchmark_scores = {test_name: total_score / file_count for test_name, total_score in total_benchmark_scores.items()}

    return average_performance_scores, average_benchmark_scores


## Directory path
result_dir = r'C:\IBT\Geekbench-6.1.0-03618f1e9_llorg_default\Geekbench-6.1.0-03618f1e9\build.avx2'
csv_file = os.path.join(result_dir, "result.csv")
average_geekbench_scores(result_dir, csv_file)

## Print average scores
#print("\n\n****Average Performance Scores:")
#for test_name, average_score in average_performance_scores.items():
#    print(f"{test_name}: {average_score:.2f}")
#print("\n****Average Benchmark Summary Scores:")
#for test_name, average_score in average_benchmark_scores.items():
#    print(f"{test_name} Score: {average_score:.2f}")
