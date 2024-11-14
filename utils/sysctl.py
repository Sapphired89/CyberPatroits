import re
import subprocess

def update_sysctl_settings():
    filepath = '/etc/sysctl.conf'
    
    try:
        # Read the current contents of the file
        with open(filepath, 'r') as file:
            lines = file.readlines()
        
        # Define patterns to search for and their replacements
        patterns = {
            r'^net\.ipv4\.tcp_syncookies\s*=\s*0$': 'net.ipv4.tcp_syncookies=1\n',
            r'^net\.ipv4\.ip_forward\s*=\s*1$': 'net.ipv4.ip_forward=0\n'
        }
        
        # Modify the lines according to the patterns
        updated_lines = []
        for line in lines:
            modified = False
            for pattern, replacement in patterns.items():
                if re.match(pattern, line):
                    # Replace line with the desired setting
                    updated_lines.append(replacement)
                    print(f"Modified line: {replacement.strip()}")
                    modified = True
                    break
            if not modified:
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
update_sysctl_settings()
