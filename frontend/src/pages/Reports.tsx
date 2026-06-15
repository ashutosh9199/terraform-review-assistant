import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, CircularProgress } from '@mui/material';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getHistory } from '../services/api';

export default function Reports() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getHistory().then(data => {
      setHistory(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <div>
      <Typography variant="h4" gutterBottom>Historical Reports</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Date Uploaded</strong></TableCell>
              <TableCell><strong>Project ID</strong></TableCell>
              <TableCell><strong>Files Analyzed</strong></TableCell>
              <TableCell align="right"><strong>Action</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {history.map((row) => (
              <TableRow key={row.project_id}>
                <TableCell>{row.date}</TableCell>
                <TableCell>{row.project_id}</TableCell>
                <TableCell>{row.files_count} files</TableCell>
                <TableCell align="right">
                  <Button variant="contained" size="small" onClick={() => navigate(`/analysis?projectId=${row.project_id}`)}>
                    View Report
                  </Button>
                </TableCell>
              </TableRow>
            ))}
            {history.length === 0 && (
              <TableRow>
                <TableCell colSpan={4} align="center">No historical reports found.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
