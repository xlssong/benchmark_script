import os

def update_ini_file(file_path, key, value, section='Settings'):
    """
    Manually updates the value of a given key in an INI file within a specified section,
    while preserving comments, whitespace, and other non-standard content.
    
    Args:
    file_path (str): The path to the INI file.
    key (str): The key in the INI file to update.
    value (str): The new value to set for the key.
    section (str): The section in the INI file where the key exists (default is 'Settings').
    
    Returns:
    bool: True if the operation is successful, False otherwise.
    """
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return False

    # Read the INI file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except IOError as e:
        print(f"Error reading file: {e}")
        return False

    # Update the key with the new value
    section_found = False
    key_found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f'[{section}]'):
            section_found = True
        elif section_found and line.strip().startswith(key):
            lines[i] = f"{key}={value}\n"
            key_found = True
            break

    if not section_found:
        print(f"Error: The section {section} does not exist in the file.")
        return False

    if not key_found:
        print(f"Error: The key {key} does not exist in the section {section}.")
        return False

    # Write the changes back to the file
    try:
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Updated {key} to {value} in section {section}.")
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")
        return False

#file_path = r'c:\Xiaoling\ibtpgo_config.ini'
# Example usage:
#result = update_ini_file(file_path, 'ProfilingReady', '0')
#result = update_ini_file(file_path, 'ProfileOutputDir', r'c:/Xiaoling/profile/')
#print(result)  # Output will be True if successful, False otherwise
