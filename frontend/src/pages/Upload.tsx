import React, { useState } from 'react';
import { Typography, Button, Box, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadFiles, analyzeProject } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Upload() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const uploadRes = await uploadFiles(file);
      const projectId = uploadRes.project_id;
      // Navigate to analysis page with project id
      navigate(`/analysis?projectId=${projectId}`);
    } catch (error) {
      console.error(error);
      alert('Upload failed');
    }
    setLoading(false);
  };

  return (
    <Box sx={{ textAlign: 'center', mt: 5 }}>
      <Typography variant="h4" gutterBottom>Upload Terraform Project</Typography>
      <Box sx={{ border: '2px dashed gray', p: 5, borderRadius: 2, display: 'inline-block', mt: 3 }}>
        <input
          accept=".zip,.tf"
          style={{ display: 'none' }}
          id="raised-button-file"
          type="file"
          onChange={handleFileChange}
        />
        <label htmlFor="raised-button-file">
          <Button variant="contained" component="span" startIcon={<CloudUploadIcon />}>
            Select File (.zip or .tf)
          </Button>
        </label>
        {file && <Typography sx={{ mt: 2 }}>{file.name}</Typography>}
      </Box>
      <Box sx={{ mt: 3 }}>
        <Button 
          variant="contained" 
          color="secondary" 
          onClick={handleUpload} 
          disabled={!file || loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Analyze'}
        </Button>
      </Box>
    </Box>
  );
}
