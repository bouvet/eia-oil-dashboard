import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'

const US_COLOR = '#f0a500'
const DEFAULT_COLOR = '#4da6ff'

export default function TopCountriesChart({ data }) {
  // Sort ascending so the largest bar is at the top in a horizontal chart
  const sorted = [...data].sort((a, b) => a.value_kbd - b.value_kbd)

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="subtitle1" fontWeight={600} mb={2}>
          Top 15 Countries by Annual Production
        </Typography>

        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 5, right: 30, bottom: 5, left: 100 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" horizontal={false} />
            <XAxis
              type="number"
              tickFormatter={v => `${(v / 1000).toFixed(0)}M`}
              tick={{ fontSize: 11 }}
            />
            <YAxis
              type="category"
              dataKey="country_name"
              tick={{ fontSize: 11 }}
              width={95}
            />
            <Tooltip
              formatter={v => [`${v != null ? v.toLocaleString() : 'N/A'} kbd`]}
              contentStyle={{ backgroundColor: '#1e2530', border: 'none' }}
            />
            <Bar dataKey="value_kbd" name="Production (kbd)" radius={[0, 3, 3, 0]}>
              {sorted.map((entry, i) => (
                <Cell
                  key={i}
                  fill={entry.iso3 === 'USA' ? US_COLOR : DEFAULT_COLOR}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <Typography variant="caption" color="text.secondary">
          Thousand barrels per day &nbsp;|&nbsp;
          <span style={{ color: US_COLOR }}>■</span> United States
        </Typography>
      </CardContent>
    </Card>
  )
}
