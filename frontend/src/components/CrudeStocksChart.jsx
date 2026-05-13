import React, { useState, useMemo } from 'react'
import { Card, CardContent, Typography, ToggleButtonGroup, ToggleButton, Box } from '@mui/material'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, ReferenceLine,
} from 'recharts'

const RANGES = ['1Y', '3Y', '5Y', 'All']

function filterByRange(data, range) {
  if (range === 'All' || !data.length) return data
  const years = parseInt(range)
  const cutoff = new Date()
  cutoff.setFullYear(cutoff.getFullYear() - years)
  return data.filter(d => new Date(d.date) >= cutoff)
}

function fiveYearAvg(data) {
  const cutoff = new Date()
  cutoff.setFullYear(cutoff.getFullYear() - 5)
  const slice = data.filter(d => new Date(d.date) >= cutoff && d.us_stocks_kb != null)
  if (!slice.length) return null
  return slice.reduce((sum, d) => sum + d.us_stocks_kb, 0) / slice.length
}

const fmt = v => v != null ? (v / 1000).toFixed(0) + 'M' : ''

export default function CrudeStocksChart({ data }) {
  const [range, setRange] = useState('3Y')

  const filtered = useMemo(() => filterByRange(data, range), [data, range])
  const avg = useMemo(() => fiveYearAvg(data), [data])

  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="subtitle1" fontWeight={600}>
            US Crude Oil Stocks
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
          <span style={{ color: '#f0a500' }}>—</span> US Total &nbsp;|&nbsp;
          <span style={{ color: '#4da6ff' }}>—</span> Cushing OK &nbsp;|&nbsp;
          <span style={{ color: '#888' }}>- -</span> 5Y avg
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
              tickFormatter={v => (v / 1000).toFixed(0) + 'M'}
              tick={{ fontSize: 11 }}
              width={55}
            />
            <Tooltip
              formatter={(v, name) => [
                v != null ? `${(v / 1000).toFixed(1)}M bbl` : 'N/A',
                name,
              ]}
              labelFormatter={l => `Week of ${l}`}
              contentStyle={{ backgroundColor: '#1e2530', border: 'none' }}
            />
            {avg && (
              <ReferenceLine
                y={avg}
                stroke="#888"
                strokeDasharray="6 3"
                label={{ value: '5Y avg', fill: '#888', fontSize: 11, position: 'right' }}
              />
            )}
            <Line
              type="monotone"
              dataKey="us_stocks_kb"
              name="US Total"
              stroke="#f0a500"
              dot={false}
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="cushing_stocks_kb"
              name="Cushing OK"
              stroke="#4da6ff"
              dot={false}
              strokeWidth={1.5}
              strokeDasharray="4 2"
            />
          </LineChart>
        </ResponsiveContainer>

        <Typography variant="caption" color="text.secondary">
          Thousand barrels &nbsp;|&nbsp; Dashed: 5-year average
        </Typography>
      </CardContent>
    </Card>
  )
}
