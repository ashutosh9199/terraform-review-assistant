import os
import shutil
import uuid
import zipfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from core.config import settings

router = APIRouter()

@router.post("/")
async def upload_files(file: UploadFile = File(...)):
    if not file.filename.endswith(('.zip', '.tf')):
        raise HTTPException(status_code=400, detail="Only .zip or .tf files are allowed.")
    
    project_id = str(uuid.uuid4())
    project_dir = os.path.join(settings.UPLOAD_DIR, project_id)
    os.makedirs(project_dir, exist_ok=True)
    
    file_path = os.path.join(project_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(project_dir)
            os.remove(file_path) # Remove zip after extraction
            
        return {"project_id": project_id, "message": "Files uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
