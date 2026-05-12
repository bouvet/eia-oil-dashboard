import React from 'react'
import { Grid, Card, CardContent, Typography, Box } from '@mui/material'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'

function TrendIndicator({ change }) {
  if (change == null) return null
  const up = change >= 0
  return (
    <Box display="flex" alignItems="center" mt={0.5}>
      {up
        ? <ArrowUpwardIcon sx={{ fontSize: 16, color: 'success.main' }} />
        : <ArrowDownwardIcon sx={{ fontSize: 16, color: 'error.main' }} />
      }
      <Typography
        variant="body2"
        color={up ? 'success.main' : 'error.main'}
        ml={0.25}
      >
        {Math.abs(change).toFixed(2)}
      </Typography>
    </Box>
  )
}

function KpiCard({ label, value, unit, change, dateStr }) {
  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="overline" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h4" fontWeight={700} mt={0.5}>
          {value != null ? value : '—'}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {unit}
        </Typography>
        <TrendIndicator change={change} />
        {dateStr && (
          <Typography variant="caption" color="text.disabled" display="block" mt={0.5}>
            as of {dateStr}
          </Typography>
        )}
      </CardContent>
    </Card>
  )
}

export default function KpiCards({ kpi }) {
  if (!kpi) return null

  const fmt = (v, decimals = 2) =>
    v != null ? Number(v).toFixed(decimals) : null

  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={3}>
        <KpiCard
          label="Brent Crude"
          value={fmt(kpi.brent_price)}
          unit="USD / barrel"
          change={kpi.brent_change}
          dateStr={kpi.brent_date}
        />
      </Grid>
      <Grid item xs={6} md={3}>
        <KpiCard
          label="WTI Crude"
          value={fmt(kpi.wti_price)}
          unit="USD / barrel"
          change={kpi.wti_change}
          dateStr={kpi.wti_date}
        />
      </Grid>
      <Grid item xs={6} md={3}>
        <KpiCard
          label="US Crude Stocks"
          value={fmt(kpi.us_stocks_mb, 0)}
          unit="million barrels"
          change={kpi.us_stocks_change_mb}
          dateStr={kpi.us_stocks_date}
        />
      </Grid>
      <Grid item xs={6} md={3}>
        <KpiCard
          label="Refinery Utilization"
          value={fmt(kpi.refinery_util_pct, 1)}
          unit="% of operable capacity"
          change={kpi.refinery_change}
          dateStr={kpi.refinery_date}
        />
      </Grid>
    </Grid>
  )
}
