import subprocess

def disable_vsftpd_service():
    try:
        # Disable and stop the vsftpd service
        print("Disabling and stopping the vsftpd service...")
        subprocess.run(['sudo', 'systemctl', 'disable', '--now', 'vsftpd'], check=True)
        print("vsftpd service has been disabled and stopped.")
        
    except subprocess.CalledProcessError:
        print("Failed to disable and stop vsftpd. Ensure you have sudo privileges.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function
disable_vsftpd_service()
