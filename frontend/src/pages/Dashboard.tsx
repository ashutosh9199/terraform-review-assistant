import { Typography, Box, Card, CardContent } from '@mui/material';

export default function Dashboard() {
  return (
    <div>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
        <Box sx={{ flex: '1 1 200px' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Total Reviews</Typography>
              <Typography variant="h5">12</Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: '1 1 200px' }}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Avg Score</Typography>
              <Typography variant="h5">85/100</Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </div>
  );
}
