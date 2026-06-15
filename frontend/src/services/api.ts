import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

export const uploadFiles = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getStats = async () => {
  const response = await api.get('/analyze/stats/overview');
  return response.data;
};

export const getHistory = async () => {
  const response = await api.get('/analyze/history');
  return response.data;
};

export const analyzeProject = async (projectId: string) => {
  const response = await api.post(`/analyze/${projectId}`);
  return response.data;
};

export default api;
