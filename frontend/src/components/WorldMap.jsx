import React, { useState, useMemo } from 'react'
import { Card, CardContent, Typography, Tooltip as MuiTooltip, Box, IconButton } from '@mui/material'
import { ComposableMap, Geographies, Geography, ZoomableGroup } from 'react-simple-maps'
import { scaleSequentialLog } from 'd3-scale'
import { interpolateYlOrRd } from 'd3-scale-chromatic'

const GEO_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'

// world-atlas TopoJSON encodes ISO numeric codes as feature `id` strings.
// This lookup converts numeric codes to ISO alpha-3 so we can join with EIA data.
const NUMERIC_TO_ISO3 = {
  "004": "AFG", "008": "ALB", "012": "DZA", "024": "AGO", "032": "ARG",
  "036": "AUS", "040": "AUT", "031": "AZE", "050": "BGD", "056": "BEL",
  "064": "BTN", "068": "BOL", "070": "BIH", "076": "BRA", "100": "BGR",
  "116": "KHM", "120": "CMR", "124": "CAN", "140": "CAF", "152": "CHL",
  "156": "CHN", "170": "COL", "178": "COG", "180": "COD", "191": "HRV",
  "192": "CUB", "196": "CYP", "203": "CZE", "204": "BEN", "208": "DNK",
  "218": "ECU", "818": "EGY", "222": "SLV", "231": "ETH", "246": "FIN",
  "250": "FRA", "266": "GAB", "276": "DEU", "288": "GHA", "300": "GRC",
  "320": "GTM", "324": "GIN", "340": "HND", "348": "HUN", "356": "IND",
  "360": "IDN", "364": "IRN", "368": "IRQ", "372": "IRL", "376": "ISR",
  "380": "ITA", "392": "JPN", "400": "JOR", "398": "KAZ", "404": "KEN",
  "408": "PRK", "410": "KOR", "414": "KWT", "417": "KGZ", "418": "LAO",
  "422": "LBN", "426": "LSO", "434": "LBY", "454": "MWI", "458": "MYS",
  "466": "MLI", "484": "MEX", "496": "MNG", "504": "MAR", "508": "MOZ",
  "516": "NAM", "524": "NPL", "528": "NLD", "540": "NCL", "554": "NZL",
  "558": "NIC", "562": "NER", "566": "NGA", "578": "NOR", "586": "PAK",
  "591": "PAN", "598": "PNG", "600": "PRY", "604": "PER", "608": "PHL",
  "616": "POL", "620": "PRT", "630": "PRI", "634": "QAT", "642": "ROU",
  "643": "RUS", "646": "RWA", "682": "SAU", "686": "SEN", "694": "SLE",
  "706": "SOM", "710": "ZAF", "724": "ESP", "728": "SSD", "144": "LKA",
  "736": "SDN", "752": "SWE", "756": "CHE", "760": "SYR", "762": "TJK",
  "764": "THA", "784": "ARE", "792": "TUR", "795": "TKM", "800": "UGA",
  "804": "UKR", "826": "GBR", "840": "USA", "858": "URY", "860": "UZB",
  "862": "VEN", "704": "VNM", "887": "YEM", "894": "ZMB", "716": "ZWE",
  "470": "MLT", "807": "MKD", "498": "MDA", "051": "ARM", "112": "BLR",
  "233": "EST", "268": "GEO", "428": "LVA", "440": "LTU", "703": "SVK",
  "705": "SVN", "499": "MNE", "688": "SRB", "020": "AND", "096": "BRN",
}

function getColor(value, scale) {
  if (value == null) return '#2c2c2c'
  return scale(value)
}

const INITIAL_POSITION = { coordinates: [0, 0], zoom: 1 }
const MIN_ZOOM = 1
const MAX_ZOOM = 8

export default function WorldMap({ data }) {
  const [tooltip, setTooltip] = useState(null)
  const [position, setPosition] = useState(INITIAL_POSITION)
  const [isDragging, setIsDragging] = useState(false)

  const handleZoomIn = () =>
    setPosition(p => ({ ...p, zoom: Math.min(p.zoom * 1.5, MAX_ZOOM) }))
  const handleZoomOut = () =>
    setPosition(p => ({ ...p, zoom: Math.max(p.zoom / 1.5, MIN_ZOOM) }))
  const handleReset = () => setPosition(INITIAL_POSITION)

  const dataByIso3 = useMemo(() => {
    const map = {}
    data.forEach(d => { map[d.iso3] = d })
    return map
  }, [data])

  const maxVal = useMemo(() => {
    const vals = data.map(d => d.value_kbd).filter(Boolean)
    return vals.length ? Math.max(...vals) : 1
  }, [data])

  const colorScale = useMemo(
    () => scaleSequentialLog([1, maxVal], interpolateYlOrRd),
    [maxVal]
  )

  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardContent sx={{ pb: 1, '&:last-child': { pb: 1 } }}>
        <Typography variant="subtitle1" fontWeight={600} mb={1}>
          World Crude Oil Production
        </Typography>

        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Typography variant="caption" color="text.secondary">Low</Typography>
          <Box
            sx={{
              width: 120,
              height: 10,
              borderRadius: 1,
              background: 'linear-gradient(to right, #ffffb2, #fd8d3c, #bd0026)',
            }}
          />
          <Typography variant="caption" color="text.secondary">High</Typography>
          <Typography variant="caption" color="text.disabled" ml={1}>
            — no data
          </Typography>
        </Box>

        <Box position="relative" sx={{ ml: -2, mr: 2, mt: 3 }}>
          <ComposableMap
            projection="geoNaturalEarth1"
            height={420}
            projectionConfig={{ scale: 155, center: [0, 12] }}
            style={{ width: '100%', height: 'auto' }}
          >
            <ZoomableGroup
              zoom={position.zoom}
              center={position.coordinates}
              minZoom={MIN_ZOOM}
              maxZoom={MAX_ZOOM}
              onMoveStart={() => {
                setIsDragging(true)
                setTooltip(null)
              }}
              onMoveEnd={pos => {
                setIsDragging(false)
                setPosition(pos)
              }}
            >
              <Geographies geography={GEO_URL}>
                {({ geographies }) =>
                  geographies.map(geo => {
                    const numericId = String(geo.id).padStart(3, '0')
                    const iso3 = NUMERIC_TO_ISO3[numericId]
                    const entry = iso3 ? dataByIso3[iso3] : null
                    const fill = getColor(entry?.value_kbd ?? null, colorScale)

                    return (
                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        fill={fill}
                        stroke="#111"
                        strokeWidth={0.4}
                        style={{
                          default: { outline: 'none' },
                          hover: { outline: 'none', fill: '#e0e0e0', cursor: 'pointer' },
                          pressed: { outline: 'none' },
                        }}
                        onMouseEnter={() => {
                          if (isDragging) return
                          setTooltip({
                            name: geo.properties.name,
                            value: entry?.value_kbd,
                            year: entry?.year,
                          })
                        }}
                        onMouseLeave={() => setTooltip(null)}
                      />
                    )
                  })
                }
              </Geographies>
            </ZoomableGroup>
          </ComposableMap>

          <Box
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              display: 'flex',
              flexDirection: 'column',
              gap: 0.5,
              bgcolor: 'background.paper',
              border: '1px solid',
              borderColor: 'divider',
              borderRadius: 1,
            }}
          >
            <IconButton size="small" onClick={handleZoomIn} aria-label="Zoom in">+</IconButton>
            <IconButton size="small" onClick={handleZoomOut} aria-label="Zoom out">−</IconButton>
            <IconButton size="small" onClick={handleReset} aria-label="Reset zoom" sx={{ fontSize: 12 }}>⟳</IconButton>
          </Box>

          {tooltip && !isDragging && (
            <Box
              sx={{
                position: 'absolute',
                bottom: 16,
                left: 16,
                bgcolor: 'background.paper',
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
                px: 1.5,
                py: 1,
                pointerEvents: 'none',
              }}
            >
              <Typography variant="body2" fontWeight={600}>{tooltip.name}</Typography>
              {tooltip.value != null ? (
                <Typography variant="caption" color="text.secondary">
                  {tooltip.value.toLocaleString()} kbd ({tooltip.year})
                </Typography>
              ) : (
                <Typography variant="caption" color="text.secondary">No data</Typography>
              )}
            </Box>
          )}
        </Box>
      </CardContent>
    </Card>
  )
}
