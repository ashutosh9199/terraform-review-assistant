import { Typography, Box, Card, CardContent, CircularProgress } from '@mui/material';
import { useEffect, useState } from 'react';
import { getStats } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState({ total_reviews: 0, avg_score: 100 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStats().then(data => {
      setStats(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <div>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
        <Box sx={{ flex: '1 1 200px' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Total Reviews Analyzed</Typography>
              <Typography variant="h5">{stats.total_reviews}</Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 200px' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Platform Average Score</Typography>
              <Typography variant="h5">{stats.avg_score}/100</Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </div>
  );
}
