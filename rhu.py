import requests

# URL of the .ogg file hosted on AWS S3
url = "https://mygenerateddatabucket.s3.eu-north-1.amazonaws.com/audios/output.ogg"

# Name of the file you want to save it as
output_file = "output.ogg"

# Send HTTP GET request to download the file
response = requests.get(url)

# Write the content to a file
with open(output_file, "wb") as file:
    file.write(response.content)

print(f"The .ogg file has been downloaded and saved as {output_file}.")


#Executing the command using the above file
import subprocess
import os

def generate_lip_sync_data(audio_file_name):
    print(f"Generating lip-sync data for audio file: {audio_file_name}")
    
    # Define the working directory and the command
    working_directory = '/Users/amir/desktop/rhubarb/rhu/lib/python3.12/site-packages'
    output_file = 'output.json'
    
    command = f'/Users/amir/Desktop/rhubarb/rhu/lib/python3.12/site-packages/Rhubarb-Lip-Sync-1.13.0-macOS/rhubarb -f json "{audio_file_name}" -o "{output_file}"'

    print(f"Executing command: {command}")

    try:
        # Run the command
        result = subprocess.run(command, cwd=working_directory, shell=True, capture_output=True, text=True)
        
        # Print stdout and stderr
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        # Check if the output file was created successfully
        if os.path.exists(output_file):
            print("Lip-sync data generated successfully")
        else:
            print("Failed to generate lip-sync data")

        return "Lip-sync data generated successfully"
    
    except Exception as e:
        print(f"Error generating lip-sync data: {e}")
        raise

# Example usage
audio_file_name = "output.ogg"
generate_lip_sync_data(audio_file_name)
