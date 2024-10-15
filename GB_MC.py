import os
import re
import subprocess
from datetime import datetime
from collections import defaultdict

# Set the number of times to run
N = 10  # You can change this value to the number of iterations you want
iterations = 5
section = 2 # 1 for single core; 2 for multi core

# Set the path to Geekbench
geekbench_path = r"C:\IBT\Geekbench-6.1.0-03618f1e9_llorg_default\Geekbench-6.1.0-03618f1e9\build.avx2\geekbench_avx2.exe"

# Create a directory with the current date to store the result files
current_date = datetime.now().strftime("%Y%m%d_%H%M")
result_dir = os.path.join(r"C:\Users\sdp\Desktop\geekbench_results", current_date)
os.makedirs(result_dir, exist_ok=True)


# Execute Geekbench N times and save the results to files
for i in range(N):
    current_time = datetime.now().strftime("%H%M%S")
    filename = f"geekbench_{current_time}_{i}.txt"
    filepath = os.path.join(result_dir, filename)
    print(f"Running Geekbench iteration: {i + 1}")
    cmd = [geekbench_path, "--no-upload", "--skip-sysinfo", "--iterations", str(iterations), "--section", str(section), "--export-text", filepath]
    print(f"Executing command: {' '.join(cmd)}")
    print(f"Saving log in file: {filepath}")
    subprocess.run(cmd, check=True)

