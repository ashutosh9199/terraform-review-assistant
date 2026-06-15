import json
import urllib.request
import urllib.parse
import mimetypes
import uuid
import os

filepath = r'C:\Users\Admin\.gemini\antigravity\scratch\terraform-review-assistant\sample_vulnerable_project.tf'

def upload_file(url, file_path):
    boundary = uuid.uuid4().hex
    filename = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        file_content = f.read()

    data = []
    data.append(f'--{boundary}\r\n'.encode('utf-8'))
    data.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode('utf-8'))
    data.append(b'Content-Type: application/octet-stream\r\n\r\n')
    data.append(file_content)
    data.append(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
    
    body = b''.join(data)
    
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())

print("Uploading...")
res = upload_file('http://127.0.0.1:8000/api/v1/upload/', filepath)
print("Upload:", res)

project_id = res['project_id']
print("Analyzing...")
req = urllib.request.Request(f'http://127.0.0.1:8000/api/v1/analyze/{project_id}', method='POST')
with urllib.request.urlopen(req) as response:
    print("Analyze:")
    print(json.dumps(json.loads(response.read()), indent=2))
