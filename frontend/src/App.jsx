import React, { useEffect, useState } from 'react'
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Grid,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material'
import client from './api/client'
import KpiCards from './components/KpiCards'
import CrudeStocksChart from './components/CrudeStocksChart'
import ProductionChart from './components/ProductionChart'
import TopCountriesChart from './components/TopCountriesChart'
import WorldMap from './components/WorldMap'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#f0a500' },
    background: { default: '#0d1117', paper: '#161b22' },
  },
  typography: { fontFamily: 'Roboto, sans-serif' },
})

export default function App() {
  const [kpi, setKpi] = useState(null)
  const [stocks, setStocks] = useState([])
  const [production, setProduction] = useState([])
  const [countries, setCountries] = useState([])
  const [world, setWorld] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [kpiRes, stocksRes, prodRes, countriesRes, worldRes] = await Promise.all([
          client.get('/api/kpi'),
          client.get('/api/stocks'),
          client.get('/api/production'),
          client.get('/api/countries'),
          client.get('/api/world'),
        ])
        setKpi(kpiRes.data)
        setStocks(stocksRes.data)
        setProduction(prodRes.data)
        setCountries(countriesRes.data)
        setWorld(worldRes.data)
      } catch (err) {
        setError(
          'Could not connect to the backend. Make sure the FastAPI server is running on http://localhost:8000 and data has been ingested.'
        )
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <AppBar position="static" color="transparent" elevation={1}
        sx={{ borderBottom: '1px solid', borderColor: 'divider' }}>
        <Toolbar>
          <Box>
            <Typography variant="h6" fontWeight={700} color="primary">
              EIA Oil Dashboard
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Data source: U.S. Energy Information Administration
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 3 }}>
        {loading && (
          <Box display="flex" justifyContent="center" mt={8}>
            <CircularProgress color="primary" />
          </Box>
        )}

        {error && (
          <Alert severity="warning" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {!loading && !error && (
          <Grid container spacing={3}>
            {/* KPI row */}
            <Grid item xs={12}>
              <KpiCards kpi={kpi} />
            </Grid>

            {/* Stocks chart */}
            <Grid item xs={12} lg={8}>
              <CrudeStocksChart data={stocks} />
            </Grid>

            {/* Production chart */}
            <Grid item xs={12} lg={4}>
              <ProductionChart data={production} />
            </Grid>

            {/* World map */}
            <Grid item xs={12} lg={7}>
              <WorldMap data={world} />
            </Grid>

            {/* Top countries */}
            <Grid item xs={12} lg={5}>
              <TopCountriesChart data={countries} />
            </Grid>
          </Grid>
        )}
      </Container>
    </ThemeProvider>
  )
}
