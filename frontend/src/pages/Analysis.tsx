import React, { useEffect, useState } from 'react';
import { Typography, CircularProgress, Box, Card, CardContent, Chip } from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import { analyzeProject } from '../services/api';

export default function Analysis() {
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get('projectId');
  const [loading, setLoading] = useState(true);
  const [report, setReport] = useState<any>(null);

  useEffect(() => {
    if (projectId) {
      analyzeProject(projectId).then(data => {
        setReport(data);
        setLoading(false);
      }).catch(err => {
        console.error(err);
        setLoading(false);
      });
    }
  }, [projectId]);

  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}><CircularProgress /></Box>;
  }

  if (!report) {
    return <Typography>No analysis report found.</Typography>;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>Analysis Report</Typography>
      <Typography variant="h5">Overall Score: {report.overall_score}/100</Typography>
      
      <Box sx={{ mt: 4 }}>
        <Typography variant="h6">Findings</Typography>
        {report.findings.map((f: any, idx: number) => (
          <Card key={idx} sx={{ mt: 2, mb: 2 }}>
            <CardContent>
              <Typography variant="h6">
                {f.issue} <Chip label={f.risk_level} color={f.risk_level === 'High' ? 'error' : 'warning'} size="small" />
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                <strong>Resource:</strong> {f.resource_type} ({f.resource_name})
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                <strong>Impact:</strong> {f.business_impact}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                <strong>Recommendation:</strong> {f.recommendation}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
    </div>
  );
}
