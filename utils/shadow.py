import subprocess

def modify_shadow_permissions():
    shadow_path = '/etc/shadow'

    try:
        # List the details of /etc/shadow
        print("Listing current permissions for /etc/shadow:")
        subprocess.run(['ls', '-alF', shadow_path], check=True)
        
        # Change permissions to 640
        print("\nChanging permissions of /etc/shadow to 640...")
        subprocess.run(['sudo', 'chmod', '640', shadow_path], check=True)
        
        # Confirm the new permissions
        print("\nPermissions after modification:")
        subprocess.run(['ls', '-alF', shadow_path], check=True)

    except subprocess.CalledProcessError:
        print("An error occurred while modifying /etc/shadow permissions. Ensure you have sudo privileges.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function
modify_shadow_permissions()
