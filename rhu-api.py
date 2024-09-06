from flask import Flask, request, jsonify
import requests
import subprocess
import os

app = Flask(__name__)

# Function to download the .ogg file
def download_file(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        return True
    else:
        return False

# Function to generate lip-sync data
def generate_lip_sync_data(audio_file_name):
    print(f"Generating lip-sync data for audio file: {audio_file_name}")
    
    working_directory = '/home/amir/pod/rhu/lib/python3.11/site-packages'
    output_file = 'output.json'
    
    command = f'/home/amir/pod/rhu/lib/python3.11/site-packages/Rhubarb-Lip-Sync-1.13.0-Linux/rhubarb -f json "{audio_file_name}" -o "{output_file}"'

    print(f"Executing command: {command}")

    try:
        result = subprocess.run(command, cwd=working_directory, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data = f.read()
            return data
        else:
            return None

    except Exception as e:
        print(f"Error generating lip-sync data: {e}")
        raise

# API endpoint to process the AWS URL
@app.route('/rhubarb_convert', methods=['POST'])
def rhubarb_convert():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Download the file
    if download_file(url, 'output.ogg'):
        # Generate lip-sync data
        lip_sync_data = generate_lip_sync_data('output.ogg')
        
        if lip_sync_data:
            return jsonify({'data': lip_sync_data}), 200
        else:
            return jsonify({'error': 'Failed to generate lip-sync data'}), 500
    else:
        return jsonify({'error': 'Failed to download file'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
