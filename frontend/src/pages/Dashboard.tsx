import React from 'react';
import { Typography, Grid, Card, CardContent } from '@mui/material';

export default function Dashboard() {
  return (
    <div>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Total Reviews</Typography>
              <Typography variant="h5">12</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>Avg Score</Typography>
              <Typography variant="h5">85/100</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}
