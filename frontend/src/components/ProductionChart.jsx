import React, { useState, useMemo } from 'react'
import { Card, CardContent, Typography, ToggleButtonGroup, ToggleButton, Box } from '@mui/material'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts'

const RANGES = ['5Y', '10Y', 'All']

function filterByRange(data, range) {
  if (range === 'All' || !data.length) return data
  const years = parseInt(range)
  const cutoff = new Date()
  cutoff.setFullYear(cutoff.getFullYear() - years)
  return data.filter(d => new Date(d.date) >= cutoff)
}

export default function ProductionChart({ data }) {
  const [range, setRange] = useState('10Y')
  const filtered = useMemo(() => filterByRange(data, range), [data, range])

  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="subtitle1" fontWeight={600}>
            US Monthly Crude Production
          </Typography>
          <ToggleButtonGroup
            value={range}
            exclusive
            onChange={(_, v) => v && setRange(v)}
            size="small"
          >
            {RANGES.map(r => (
              <ToggleButton key={r} value={r}>{r}</ToggleButton>
            ))}
          </ToggleButtonGroup>
        </Box>

        <Typography variant="caption" color="text.secondary" display="block" mb={1}>
          <span style={{ color: '#4caf50' }}>—</span> US Production (kbd)
        </Typography>

        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={filtered} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
            <XAxis
              dataKey="date"
              tickFormatter={d => d.slice(0, 7)}
              tick={{ fontSize: 11 }}
              interval="preserveStartEnd"
            />
            <YAxis
              tickFormatter={v => v.toLocaleString()}
              tick={{ fontSize: 11 }}
              width={65}
            />
            <Tooltip
              formatter={v => [`${v != null ? v.toLocaleString() : 'N/A'} kbd`]}
              labelFormatter={l => l}
              contentStyle={{ backgroundColor: '#1e2530', border: 'none' }}
            />
            <Line
              type="monotone"
              dataKey="production_kbd"
              name="US Production"
              stroke="#4caf50"
              dot={false}
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>

        <Typography variant="caption" color="text.secondary">
          Thousand barrels per day
        </Typography>
      </CardContent>
    </Card>
  )
}
