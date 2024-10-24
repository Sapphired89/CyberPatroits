import subprocess
import os



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



# Function to find all MP3 files
def find_mp3s():
    print(f"{bcolors.OKCYAN}Searching for MP3 files...{bcolors.ENDC}")
    try:
        result = subprocess.run(['find', os.path.expanduser('~'), '-name', '*.mp3'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            mp3_files = result.stdout.strip().split('\n')
            if mp3_files[0]:
                print(f"{bcolors.OKGREEN}Found the following MP3 files:{bcolors.ENDC}")
                for file in mp3_files:
                    print(file)
            else:
                print(f"{bcolors.WARNING}No MP3 files found.{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Error searching for MP3 files:{bcolors.ENDC}")
            print(result.stderr)
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}")



# Function to list authorized users with valid login shells
def list_authorized_users():
    print(f"{bcolors.OKCYAN}\nListing all authorized users...{bcolors.ENDC}")
    try:
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                parts = line.strip().split(':')
                username, shell = parts[0], parts[-1]
                if shell in ['/bin/bash', '/bin/zsh', '/bin/sh']:
                    print(f"{bcolors.OKGREEN}User: {username}{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while listing users: {e}{bcolors.ENDC}")



# Function to remove packages
def rm_pkg(package):
    if package and package.lower() != 'quit':
        try:
            result = subprocess.run(
                ['sudo', 'apt', 'remove', '-y', package],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0:
                print(f"{bcolors.OKGREEN}Package {package} removed successfully!{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}Error removing package {package}:{bcolors.ENDC}")
                print(result.stderr)
        except Exception as e:
            print(f"{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}")



# Pre-removal process
def pre_rm():
    print("--------------------\n")
    print("Pre Script Removal:\n")
    rm_pkg('wireshark')



# Command execution helper function
def run_command(cmd, sudo=False):
    if sudo:
        cmd.insert(0, 'sudo')
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"{bcolors.OKGREEN}Command successful: {' '.join(cmd)}{bcolors.ENDC}")
            return result.stdout
        else:
            print(f"{bcolors.FAIL}Command failed: {' '.join(cmd)}{bcolors.ENDC}")
            print(result.stderr)
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}")



# Password aging policy
def set_password_aging():
    print(f"{bcolors.OKCYAN}Configuring password aging policies...{bcolors.ENDC}")
    
    login_defs_changes = {
        'PASS_MAX_DAYS': '90',
        'PASS_MIN_DAYS': '7',
        'PASS_WARN_AGE': '7'
    }

    try:
        with open('/etc/login.defs', 'r') as f:
            lines = f.readlines()

        with open('/etc/login.defs', 'w') as f:
            for line in lines:
                for key, value in login_defs_changes.items():
                    if key in line:
                        line = f"{key} {value}\n"
                f.write(line)
        print(f"{bcolors.OKGREEN}Password aging policy set in /etc/login.defs{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred updating /etc/login.defs: {e}{bcolors.ENDC}")



# Password complexity policy
def set_password_complexity():
    print(f"{bcolors.OKCYAN}Configuring password complexity policies...{bcolors.ENDC}")
    
    complexity_config = [
        "minlen = 8",
        "dcredit = -1",
        "ucredit = -1",
        "lcredit = -1",
        "ocredit = -1",
        "retry = 3"
    ]
    
    try:
        with open('/etc/security/pwquality.conf', 'w') as f:
            f.write("\n".join(complexity_config) + "\n")
        print(f"{bcolors.OKGREEN}Password complexity policy set in /etc/security/pwquality.conf{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred updating /etc/security/pwquality.conf: {e}{bcolors.ENDC}")



# Password history policy
def set_password_history():
    print(f"{bcolors.OKCYAN}Configuring password history (prevent reuse)...{bcolors.ENDC}")
    
    try:
        with open('/etc/pam.d/common-password', 'r') as f:
            lines = f.readlines()

        with open('/etc/pam.d/common-password', 'w') as f:
            for line in lines:
                if 'pam_unix.so' in line:
                    if 'remember=' not in line:
                        line = line.strip() + ' remember=5\n'
                f.write(line)
        print(f"{bcolors.OKGREEN}Password history policy set in /etc/pam.d/common-password{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred updating /etc/pam.d/common-password: {e}{bcolors.ENDC}")



# Lockout policy
def set_lockout_policy():
    print(f"{bcolors.OKCYAN}Configuring account lockout policy...{bcolors.ENDC}")
    
    lockout_config = [
        "deny = 5",
        "unlock_time = 600",
        "fail_interval = 900"
    ]
    
    try:
        with open('/etc/security/faillock.conf', 'w') as f:
            f.write("\n".join(lockout_config) + "\n")
        print(f"{bcolors.OKGREEN}Account lockout policy set in /etc/security/faillock.conf{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred updating /etc/security/faillock.conf: {e}{bcolors.ENDC}")



# Main loop to interact with the user
def main():
    set_password_aging()
    set_password_complexity()
    set_password_history()
    set_lockout_policy()
    pre_rm()
    find_mp3s()
    list_authorized_users()

    while True:
        print("--------------------\n")
        i = input(f"{bcolors.HEADER}: ")

        if i.lower() == 'quit':
            break
        else:
            rm_pkg(i)



if __name__ == "__main__":
    main()
