import re
import subprocess

def remove_nullok_from_common_auth():
    filepath = '/etc/pam.d/common-auth'
    
    try:
        # Read the current contents of the file
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Modify the lines, removing 'nullok' from the specific line if it exists
        updated_lines = []
        pattern = r'(auth \[success=2 default=ignore\] pam_unix\.so)(.*nullok)(.*)'
        
        for line in lines:
            # Check if the line matches the pattern
            if re.search(pattern, line):
                # Remove 'nullok' from the line
                modified_line = re.sub(r'\s*nullok', '', line)
                updated_lines.append(modified_line)
                print(f"Modified line: {modified_line.strip()}")
            else:
                updated_lines.append(line)
        
        # Write the updated content back to the file
        with open(filepath, 'w') as file:
            file.writelines(updated_lines)
        
        print(f"Updated '{filepath}' successfully.")
    
    except PermissionError:
        print(f"Permission denied: Unable to modify {filepath}. Try running as root.")
    except FileNotFoundError:
        print(f"File not found: {filepath}.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Open file in gedit for user verification (optional)
    try:
        subprocess.run(['gedit', f'admin://{filepath}'], check=True)
    except subprocess.CalledProcessError:
        print("Failed to open file in gedit.")
    except Exception as e:
        print(f"An error occurred while opening the file in gedit: {e}")

# Run the function
remove_nullok_from_common_auth()
