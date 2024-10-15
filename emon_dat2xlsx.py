import glob
import os
import subprocess

# Define the path to search for files
path_to_search = r'C:\Users\sdp\Desktop\EMON_data\Sep27'
os.chdir(path_to_search)
# Use glob.glob() to find all matching files
pattern = os.path.join(path_to_search, '*.dat')
files = glob.glob(pattern)

# Iterate over the matching files and perform the command
for file_path in files:
    # Get the base name of the file (excluding the path)
    dat_name = os.path.basename(file_path)
    xls_name = dat_name.replace('.dat', '.xlsx')
    #Generate xlsx from edp data
    parse_cmd = 'python "C:\Program Files (x86)\IntelSWTools\sep\config\edp\pyedp\edp.py" \
        -m P-core="C:\Program Files (x86)\IntelSWTools\sep\config\edp\lioncove_private_beta.xml" \
        E-core="C:\Program Files (x86)\IntelSWTools\sep\config\edp\skymont_private.xml" \
        -f P-core="C:\Program Files (x86)\IntelSWTools\sep\config\edp\chart_format_lioncove_private.txt" \
        E-core="C:\Program Files (x86)\IntelSWTools\sep\config\edp\chart_format_skymont_private.txt" '
    cmd = parse_cmd + ' -i ' + dat_name + ' -o ' + xls_name
    print (cmd)
    try:
        subprocess.run(cmd, check=True)
        print(f"pyedp.edp ran successfully, output saved to {xls_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running pyedp.edp: {e}")