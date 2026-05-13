import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer,
} from 'recharts'

const BAR_COLOR = '#4da6ff'

export default function TopCountriesChart({ data }) {
  // Sort descending so the largest producers appear at the top
  const sorted = [...data].sort((a, b) => b.value_kbd - a.value_kbd)

  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="subtitle1" fontWeight={600} mb={1}>
          Top 15 Countries by Annual Production
        </Typography>

        <Typography variant="caption" color="text.secondary" display="block" mb={1}>
          Thousand barrels per day
        </Typography>

        <ResponsiveContainer width="100%" height={400}>
          <BarChart
            data={sorted}
            layout="vertical"
            margin={{ top: 5, right: 50, bottom: 5, left: 0 }}
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
            <Bar dataKey="value_kbd" name="Production (kbd)" fill={BAR_COLOR} radius={[0, 3, 3, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
