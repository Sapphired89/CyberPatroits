import subprocess, os, shutil, time

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

def enable_ufw():
    if shutil.which("ufw"):
        print(f"{bcolors.OKCYAN}Enabling UFW...{bcolors.ENDC}")
        try:
            result = subprocess.run(
                ['ufw', 'enable'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0:
                print(f"{bcolors.OKGREEN}UFW enabled successfully!{bcolors.ENDC}")
            else:
                print(f"{bcolors.FAIL}Failed to enable UFW:{bcolors.ENDC}")
                print(result.stderr)
        except Exception as e:
            print(f"{bcolors.FAIL}An error occurred: {e}{bcolors.ENDC}")
    else:
        print(f"{bcolors.FAIL}UFW not found!{bcolors.ENDC}")

def update():
    subprocess.call(["sudo", "apt-get", "update"])
    subprocess.call(["spd-say", "\"update has finished\""])
    print("---------")
    time.sleep(1)

    subprocess.call(["sudo", "apt-get", "upgrade", "-y"])
    subprocess.call(["spd-say", "\"upgrade has finished\""])
    print("---------")
    time.sleep(1)

    subprocess.call(["sudo", "apt-get", "dist-upgrade", "-y"])
    subprocess.call(["spd-say", "\"dist-upgrade has finished\""])
    print("---------")
    time.sleep(1)   

def find_mp3s():
    print(f"{bcolors.OKCYAN}Searching for MP3 files...{bcolors.ENDC}")
    try:
        result = subprocess.run(['find', os.path.expanduser('~'), '-name', '*.mp3'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            mp3_files = result.stdout.strip().split('\n')
            if mp3_files and mp3_files[0]:
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

def list_authorized_users():
    print(f"{bcolors.OKCYAN}\nListing all authorized users...{bcolors.ENDC}")
    users = []
    try:
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                parts = line.strip().split(':')
                username, shell = parts[0], parts[-1]
                if shell in ['/bin/bash', '/bin/zsh', '/bin/sh']:
                    users.append(username)  # Collect usernames
                    print(f"{bcolors.OKGREEN}User: {username}{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while listing users: {e}{bcolors.ENDC}")
    return users 

def rm_pkg(package):
    if package and package.lower() != 'quit':
        if shutil.which("apt"):
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
        else:
            print(f"{bcolors.FAIL}apt not found!{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Invalid package name or quit command received.{bcolors.ENDC}")

def pre_rm():
    print("--------------------\nPre Script Removal:\n")
    rm_pkg('wireshark')
    rm_pkg('ophcrack')
    rm_pkg('openciv')

def run_command(cmd, sudo=False):
    if sudo:
        cmd.insert(0, 'sudo')
    if shutil.which(cmd[0]):
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
    else:
        print(f"{bcolors.FAIL}Command {cmd[0]} not found!{bcolors.ENDC}")

# Password aging
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

# Complexity
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

# History
def set_password_history():
    print(f"{bcolors.OKCYAN}Configuring password history (prevent reuse)...{bcolors.ENDC}")
    try:
        with open('/etc/pam.d/common-password', 'r') as f:
            lines = f.readlines()
        with open('/etc/pam.d/common-password', 'w') as f:
            for line in lines:
                if 'pam_unix.so' in line and 'remember=' not in line:
                    line = line.strip() + ' remember=5\n'
                f.write(line)
        print(f"{bcolors.OKGREEN}Password history policy set in /etc/pam.d/common-password{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred updating /etc/pam.d/common-password: {e}{bcolors.ENDC}")

# Lockout
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

# SSH root login
def check_and_disable_ssh_root_login():
    print(f"{bcolors.OKCYAN}Checking SSH root login configuration...{bcolors.ENDC}")
    try:
        with open('/etc/ssh/sshd_config', 'r') as ssh_config_file:
            lines = ssh_config_file.readlines()
        root_login_enabled = any('PermitRootLogin yes' in line for line in lines)
        if root_login_enabled:
            print(f"{bcolors.WARNING}Root login is enabled. Disabling it...{bcolors.ENDC}")
            with open('/etc/ssh/sshd_config', 'w') as ssh_config_file:
                for line in lines:
                    if 'PermitRootLogin' in line:
                        line = 'PermitRootLogin no\n'
                    ssh_config_file.write(line)
            print(f"{bcolors.OKGREEN}Root login disabled in SSH configuration.{bcolors.ENDC}")
        else:
            print(f"{bcolors.OKGREEN}Root login is already disabled.{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while checking SSH configuration: {e}{bcolors.ENDC}")


def list_and_remove_user():
    print(f"{bcolors.OKCYAN}\nListing all authorized users...{bcolors.ENDC}")
    users = []
    
    try:
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                parts = line.strip().split(':')
                username, shell = parts[0], parts[-1]
                if shell in ['/bin/bash', '/bin/zsh', '/bin/sh']:
                    users.append(username)  # Collect usernames
                    print(f"{bcolors.OKGREEN}User {len(users) - 1}: {username}{bcolors.ENDC}")  # Display user with number
    except Exception as e:
        print(f"{bcolors.FAIL}An error occurred while listing users: {e}{bcolors.ENDC}")
        return

    if users:
        while True:
            user_input = input(f"{bcolors.OKCYAN}Select a user number to remove (0-{len(users) - 1} or 'q' to quit): {bcolors.ENDC}")

            if user_input.lower() == 'q':
                print(f"{bcolors.OKCYAN}Exiting user removal.{bcolors.ENDC}")
                return  # Exit the function

            try:
                user_number = int(user_input)

                if 1 <= user_number < len(users):
                    user_to_remove = users[user_number]
                    print(f"{bcolors.OKCYAN}Removing user: {user_to_remove}{bcolors.ENDC}")
                    try:
                        result = subprocess.run(['sudo', 'userdel', user_to_remove],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        if result.returncode == 0:
                            print(f"{bcolors.OKGREEN}User {user_to_remove} removed successfully!{bcolors.ENDC}")
                        else:
                            print(f"{bcolors.FAIL}Failed to remove user {user_to_remove}:{bcolors.ENDC}")
                            print(result.stderr)
                    except Exception as e:
                        print(f"{bcolors.FAIL}An error occurred while removing user: {e}{bcolors.ENDC}")
                    break
                elif user_number == 0:
                    print(f"{bcolors.OKCYAN}Exiting user removal.\n{bcolors.ENDC}")
                    return  # Exit the function
                else:
                    print(f"{bcolors.FAIL}Invalid user number!{bcolors.ENDC}")
            except ValueError:
                print(f"{bcolors.FAIL}Please enter a valid number.{bcolors.ENDC}")


if __name__ == "__main__":
    list_and_remove_user()
    enable_ufw()
    find_mp3s()
    update()
    pre_rm()
    set_password_aging()
    set_password_complexity()
    set_password_history()
    set_lockout_policy()
    check_and_disable_ssh_root_login()
