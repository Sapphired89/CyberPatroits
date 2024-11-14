import subprocess
import os

def create_pam_faillock_configs():
    lock_path = '/usr/share/pam-configs/faillock'
    notif_path = '/usr/share/pam-configs/faillock_notify'

    # Faillock configuration content
    lock_content = """Name: Enforce failed login attempt counter
Default: no
Priority: 0
Auth-Type: Primary
Auth:
    [default=die]   pam_faillock.so authfail
    sufficient      pam_faillock.so authsucc
"""
    
    notif_content = """Name: Notify on failed login attempts
Default: no
Priority: 1024
Auth-Type: Primary
Auth:
    requisite   pam_faillock.so preauth
"""

    # Write lock configuration file
    try:
        with open(lock_path, "w") as lock_file:
            lock_file.write(lock_content)
        print(f"Faillock configuration written to {lock_path}")
    except PermissionError:
        print(f"Permission denied: Unable to write to {lock_path}. Try running as root.")
        return
    
    # Write notification configuration file
    try:
        with open(notif_path, "w") as notif_file:
            notif_file.write(notif_content)
        print(f"Notification configuration written to {notif_path}")
    except PermissionError:
        print(f"Permission denied: Unable to write to {notif_path}. Try running as root.")
        return

    # Use subprocess to refresh the files, if needed
    try:
        subprocess.run(['sudo', 'touch', lock_path], check=True)
        print("Touched faillock configuration to ensure permissions.")
    except subprocess.CalledProcessError:
        print("Failed to touch faillock configuration file.")

    # Open in editor (optional, requires user permission and graphical environment)
    if os.getenv("DISPLAY"):  # Check if in graphical environment
        subprocess.run(['gedit', f'admin://{lock_path}'])
    else:
        print("No graphical environment detected; skipping editor step.")
        
create_pam_faillock_configs()
