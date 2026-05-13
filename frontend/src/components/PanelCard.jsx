import React from 'react'
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material'

/**
 * Shared chrome for every dashboard panel: title, loading spinner, and
 * inline error display so a broken endpoint never blanks the dashboard.
 */
export default function PanelCard({ title, loading, error, action, children }) {
  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
          <Typography variant="subtitle1" fontWeight={600}>
            {title}
          </Typography>
          {action}
        </Box>

        {loading && (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress size={28} color="primary" />
          </Box>
        )}

        {error && !loading && (
          <Alert severity="warning" variant="outlined">
            {error}
          </Alert>
        )}

        {!loading && !error && children}
      </CardContent>
    </Card>
  )
}
