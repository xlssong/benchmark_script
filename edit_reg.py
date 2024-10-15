import winreg

def set_appinit_dlls(dll_file):
    """
    Sets the AppInit_DLLs registry value to the specified DLL file path.
    
    Args:
    dll_file (str): The path to the DLL file.
    
    Returns:
    str: "pass" if the operation is successful, "fail" otherwise.
    """
    # Define the registry key path and the value name
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"
    value_name = "AppInit_DLLs"

    try:
        # Open the registry key with write access
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)

        # Set the value
        winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, dll_file)

        # Close the key
        winreg.CloseKey(key)
        print(f"Registry value {value_name} set to {dll_file}")
        return "pass"
    except PermissionError:
        print("Error: Insufficient permissions to modify the registry.")
        print("Please run this script as an administrator.")
        return "fail"
    except OSError as e:
        print(f"Error updating registry: {e}")
        return "fail"

def set_LoadAppInit(enable_load):
 # Define the registry key path and the value name
    key_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"
    value_name = "LoadAppInit_DLLs"

    try:
        # Open the registry key with write access
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY)

        if enable_load:
            # Set the value
            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 1)
        else:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, 0)

        # Close the key
        winreg.CloseKey(key)
        print(f"Registry value {value_name} set to {enable_load}")
        return "pass"
    except PermissionError:
        print("Error: Insufficient permissions to modify the registry.")
        print("Please run this script as an administrator.")
        return "fail"
    except OSError as e:
        print(f"Error updating registry: {e}")
        return "fail"

# Example usage:
#result = set_appinit_dlls(r"C:\xiaoling\ibtpgo_dll14.dll")
#result = set_LoadAppInit(1)
#print(result)  # Output will be "pass" or "fail"
