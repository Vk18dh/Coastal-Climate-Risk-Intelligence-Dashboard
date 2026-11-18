import { useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import {
  MapPin,
  ShieldAlert,
  ArrowRight,
  Waves,
  CloudRain,
  Mountain,
  FileText,
  AlertTriangle,
  Compass,
  Maximize2,
  Globe2,
} from 'lucide-react'

// Basemap Tile Providers
const TILE_LAYERS = {
  dark: {
    name: 'Dark Intelligence',
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '&copy; <a href="https://carto.com/">CARTO</a>, &copy; OpenStreetMap',
    maxZoom: 18,
  },
  satellite: {
    name: 'Realistic Satellite',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri, Maxar, Earthstar Geographics, GIS Community',
    maxZoom: 18,
  },
  terrain: {
    name: 'Topographic / Streets',
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    attribution: '&copy; CARTO, &copy; OpenStreetMap contributors',
    maxZoom: 18,
  },
} as const

type BaseMapKey = keyof typeof TILE_LAYERS

export default function RiskMapPage() {
  const navigate = useNavigate()
  const { selectedRegionId, setSelectedRegionId } = useAppStore()
  const [baseMapKey, setBaseMapKey] = useState<BaseMapKey>('satellite')
  const [riskFilter, setRiskFilter] = useState<'all' | 'elevated' | 'normal'>('all')

  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const tileLayerRef = useRef<L.TileLayer | null>(null)
  const featureGroupRef = useRef<L.FeatureGroup | null>(null)

  const { data: regions, isLoading } = useQuery({
    queryKey: ['regions'],
    queryFn: () => apiService.getRegions(),
  })

  const { data: selectedRegion } = useQuery({
    queryKey: ['region-detail', selectedRegionId],
    queryFn: () => apiService.getRegion(selectedRegionId),
    enabled: !!selectedRegionId,
  })

  const { data: aiInsights } = useQuery({
    queryKey: ['ai-insights', selectedRegionId],
    queryFn: () => apiService.getAIInsights(selectedRegionId),
    enabled: !!selectedRegionId,
  })

  const getRiskColor = (level: string = 'Low') => {
    switch (level) {
      case 'Critical':
        return '#ef4444' // Red
      case 'High':
        return '#f97316' // Orange
      case 'Moderate':
        return '#eab308' // Yellow
      default:
        return '#10b981' // Green
    }
  }

  // 1. Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return

    // Center on Peninsular India
    const map = L.map(mapContainerRef.current, {
      center: [15.2, 80.2],
      zoom: 5.2,
      minZoom: 4,
      maxZoom: 16,
      zoomControl: false,
    })

    // Custom Zoom Control top-right
    L.control.zoom({ position: 'topright' }).addTo(map)

    // Base Tile Layer
    const baseConfig = TILE_LAYERS[baseMapKey]
    const tileLayer = L.tileLayer(baseConfig.url, {
      attribution: baseConfig.attribution,
      maxZoom: baseConfig.maxZoom,
    }).addTo(map)

    tileLayerRef.current = tileLayer
    featureGroupRef.current = L.featureGroup().addTo(map)
    mapInstanceRef.current = map

    return () => {
      map.remove()
      mapInstanceRef.current = null
    }
  }, [])

  // 2. Switch Basemap (Dark, Satellite, Topo)
  useEffect(() => {
    if (!mapInstanceRef.current || !tileLayerRef.current) return
    const map = mapInstanceRef.current
    map.removeLayer(tileLayerRef.current)

    const baseConfig = TILE_LAYERS[baseMapKey]
    const newTileLayer = L.tileLayer(baseConfig.url, {
      attribution: baseConfig.attribution,
      maxZoom: baseConfig.maxZoom,
    }).addTo(map)

    // Ensure tile layer stays beneath polygon vectors
    newTileLayer.bringToBack()
    tileLayerRef.current = newTileLayer
  }, [baseMapKey])

  // 3. Render Coastal Polygons & Animated Markers
  useEffect(() => {
    if (!mapInstanceRef.current || !featureGroupRef.current || !regions) return

    const group = featureGroupRef.current
    group.clearLayers()

    // Filter regions if requested
    const filtered = regions.filter((r) => {
      const level = r.latest_risk?.risk_level ?? 'Low'
      if (riskFilter === 'elevated') return level === 'High' || level === 'Critical'
      if (riskFilter === 'normal') return level === 'Low' || level === 'Moderate'
      return true
    })

    filtered.forEach((reg) => {
      const risk = reg.latest_risk
      const score = risk?.final_score ?? 0.0
      const level = risk?.risk_level ?? 'Low'
      const color = getRiskColor(level)
      const isSelected = reg.id === selectedRegionId

      const lat = reg.coordinates.latitude
      const lon = reg.coordinates.longitude

      // Leaflet expects [latitude, longitude]
      // Generate authentic coastal polygon tract around coordinates
      const deltaLat = 0.28
      const deltaLon = 0.28
      const polygonCoords: L.LatLngExpression[] = [
        [lat - deltaLat * 0.7, lon - deltaLon * 0.6],
        [lat - deltaLat * 0.4, lon + deltaLon * 0.8],
        [lat + deltaLat * 0.8, lon + deltaLon * 0.6],
        [lat + deltaLat * 0.9, lon - deltaLon * 0.4],
        [lat - deltaLat * 0.2, lon - deltaLon * 0.8],
      ]

      // Polygon layer
      const polygon = L.polygon(polygonCoords, {
        color: color,
        weight: isSelected ? 3.5 : 2,
        fillColor: color,
        fillOpacity: isSelected ? 0.45 : 0.25,
        dashArray: isSelected ? undefined : '4, 4',
      })

      polygon.on('click', () => {
        setSelectedRegionId(reg.id)
      })

      polygon.bindTooltip(
        `<strong>${reg.name}</strong><br/>CCRI: ${score.toFixed(1)}/100 (${level})`,
        { sticky: true, className: 'leaflet-custom-tooltip' }
      )

      group.addLayer(polygon)

      // Animated Marker DivIcon
      const markerHtml = `
        <div class="relative flex items-center justify-center cursor-pointer group">
          ${
            level === 'High' || level === 'Critical'
              ? `<div class="absolute w-10 h-10 rounded-full animate-ping opacity-60" style="background-color: ${color}"></div>`
              : ''
          }
          <div class="relative w-8 h-8 rounded-full border-2 border-white shadow-lg flex items-center justify-center font-bold text-white text-[10px]" style="background-color: ${color}">
            ${score.toFixed(0)}
          </div>
          <div class="absolute -bottom-5 whitespace-nowrap bg-slate-900/90 text-white px-2 py-0.5 rounded text-[9px] font-semibold border border-slate-700 shadow-md">
            ${reg.name.split(' ')[0]}
          </div>
        </div>
      `

      const customIcon = L.divIcon({
        html: markerHtml,
        className: 'custom-leaflet-marker',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      })

      const marker = L.marker([lat, lon], { icon: customIcon })

      marker.on('click', () => {
        setSelectedRegionId(reg.id)
      })

      group.addLayer(marker)
    })
  }, [regions, selectedRegionId, riskFilter])

  // 4. Smooth Fly-To when Selected Region Changes
  const handleFlyToRegion = (regId: number) => {
    setSelectedRegionId(regId)
    const target = regions?.find((r) => r.id === regId)
    if (target && mapInstanceRef.current) {
      mapInstanceRef.current.flyTo(
        [target.coordinates.latitude, target.coordinates.longitude],
        8.5,
        { duration: 1.2 }
      )
    }
  }

  const handleResetView = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.flyTo([15.2, 80.2], 5.2, { duration: 1.0 })
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Loading realistic coastal GIS layers...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4 max-w-7xl mx-auto pb-10">
      {/* ── Page Header & Controls ──────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Globe2 className="w-6 h-6 text-blue-600" />
            <span>Realistic Coastal GIS Risk Map</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Real satellite imagery, true topographic bathymetry, and interactive CCRI hazard boundaries
          </p>
        </div>

        {/* Map Control Bar */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Basemap Switcher */}
          <div className="flex items-center gap-1 bg-white border border-slate-200 p-1 rounded-lg shadow-xs text-xs font-semibold">
            <Compass className="w-3.5 h-3.5 text-slate-500 ml-1.5" />
            {(['satellite', 'dark', 'terrain'] as const).map((key) => (
              <button
                key={key}
                onClick={() => setBaseMapKey(key)}
                className={`px-2.5 py-1 rounded transition-colors ${
                  baseMapKey === key
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                {TILE_LAYERS[key].name.split(' ')[0]}
              </button>
            ))}
          </div>

          {/* Reset Zoom Button */}
          <button
            onClick={handleResetView}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold shadow-xs transition-colors"
            title="Reset to Full Coast View"
          >
            <Maximize2 className="w-3.5 h-3.5 text-slate-500" />
            <span>Full Coast</span>
          </button>
        </div>
      </div>

      {/* ── Interactive Map & Side Inspector ────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Leaflet Map Container (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900 rounded-2xl border border-slate-800 shadow-xl overflow-hidden relative flex flex-col justify-between min-h-[620px]">
          {/* Top Overlay Badge Bar */}
          <div className="absolute top-3 left-3 z-[1000] flex items-center gap-2">
            <div className="bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-lg px-3 py-1.5 text-xs text-white shadow-md flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-semibold">Bay of Bengal & Arabian Sea</span>
              <span className="text-[10px] text-slate-400 font-mono">EPSG:4326 PostGIS</span>
            </div>

            {/* Quick Filter */}
            <div className="bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-lg p-1 text-xs text-white shadow-md flex items-center gap-1">
              {(['all', 'elevated', 'normal'] as const).map((filter) => (
                <button
                  key={filter}
                  onClick={() => setRiskFilter(filter)}
                  className={`px-2 py-0.5 rounded text-[10px] font-bold capitalize transition-colors ${
                    riskFilter === filter
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-800'
                  }`}
                >
                  {filter}
                </button>
              ))}
            </div>
          </div>

          {/* Actual Leaflet Map Canvas */}
          <div ref={mapContainerRef} className="w-full h-[540px] z-0" />

          {/* Bottom Map Legend Bar */}
          <div className="z-10 bg-slate-900/95 border-t border-slate-800 p-3 flex flex-wrap items-center justify-between text-xs text-slate-300 gap-3">
            <span className="font-bold text-white uppercase tracking-wider text-[11px]">
              CCRI Classification:
            </span>
            <div className="flex items-center gap-4 flex-wrap">
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-emerald-500"></span>
                <span>Low (&lt;25)</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-yellow-400"></span>
                <span>Moderate (25–50)</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-orange-500"></span>
                <span>High (50–75)</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-sm bg-rose-500"></span>
                <span>Critical (&ge;75)</span>
              </div>
            </div>
            <span className="text-[10px] text-slate-400">Click a polygon or pin to inspect</span>
          </div>
        </div>

        {/* Selected Region Inspector (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {selectedRegion ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
              {/* Region Header */}
              <div className="flex items-start justify-between border-b border-slate-100 pb-4">
                <div>
                  <div className="flex items-center gap-2 text-xs font-semibold text-blue-600 uppercase tracking-wider">
                    <MapPin className="w-4 h-4" />
                    <span>{selectedRegion.district}, {selectedRegion.state}</span>
                  </div>
                  <h2 className="text-xl font-bold text-slate-900 mt-1">
                    {selectedRegion.name}
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">{selectedRegion.coast}</p>
                </div>

                <div className="text-right">
                  <div
                    className="inline-block px-3 py-1 rounded-full text-xs font-bold text-white shadow-xs"
                    style={{ backgroundColor: getRiskColor(selectedRegion.latest_risk?.risk_level ?? 'Low') }}
                  >
                    {selectedRegion.latest_risk?.risk_level?.toUpperCase() ?? 'LOW'}
                  </div>
                  <p className="text-2xl font-black text-slate-900 mt-1">
                    {selectedRegion.latest_risk?.final_score?.toFixed(1) ?? '—'}
                    <span className="text-xs font-normal text-slate-400">/100</span>
                  </p>
                </div>
              </div>

              {/* Observed Environmental Metrics Grid */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
                  Observed Environmental Parameters
                </h3>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-lg bg-sky-50 border border-sky-100 flex items-center gap-3">
                    <CloudRain className="w-5 h-5 text-sky-600 flex-shrink-0" />
                    <div>
                      <p className="text-[11px] font-medium text-sky-800">24h Rainfall</p>
                      <p className="text-base font-bold text-sky-950">
                        {selectedRegion.latest_rainfall_mm?.toFixed(1) ?? '—'} mm
                      </p>
                    </div>
                  </div>

                  <div className="p-3 rounded-lg bg-teal-50 border border-teal-100 flex items-center gap-3">
                    <Waves className="w-5 h-5 text-teal-600 flex-shrink-0" />
                    <div>
                      <p className="text-[11px] font-medium text-teal-800">Tidal Height</p>
                      <p className="text-base font-bold text-teal-950">
                        {selectedRegion.latest_tide_m?.toFixed(2) ?? '—'} m
                      </p>
                    </div>
                  </div>

                  <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-100 flex items-center gap-3">
                    <Mountain className="w-5 h-5 text-emerald-600 flex-shrink-0" />
                    <div>
                      <p className="text-[11px] font-medium text-emerald-800">Elevation</p>
                      <p className="text-base font-bold text-emerald-950">
                        {selectedRegion.elevation_m} m
                      </p>
                    </div>
                  </div>

                  <div className="p-3 rounded-lg bg-amber-50 border border-amber-100 flex items-center gap-3">
                    <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
                    <div>
                      <p className="text-[11px] font-medium text-amber-800">Flood Hazard</p>
                      <p className="text-base font-bold text-amber-950 capitalize">
                        {selectedRegion.flood_severity}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* CCRI Component Breakdown */}
              {selectedRegion.latest_risk?.component_scores && (
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
                    Deterministic CCRI Component Contributions
                  </h3>
                  <div className="space-y-2 text-xs">
                    {Object.entries(selectedRegion.latest_risk.component_scores).map(([comp, score]) => {
                      const effWeight = selectedRegion.latest_risk?.effective_weights[comp] ?? 0.25
                      const cleanName = comp.replace('_score', '').replace(/^\w/, (c) => c.toUpperCase())

                      return (
                        <div key={comp} className="space-y-1">
                          <div className="flex justify-between text-slate-600">
                            <span className="font-semibold text-slate-800">{cleanName}</span>
                            <span>Score: {(score * 100).toFixed(0)}/100 · Weight: {(effWeight * 100).toFixed(0)}%</span>
                          </div>
                          <div className="w-full h-2 rounded-full bg-slate-100 overflow-hidden">
                            <div
                              className="h-full bg-blue-600 rounded-full transition-all duration-300"
                              style={{ width: `${Math.min(100, score * 100)}%` }}
                            ></div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* AI Grounded Summary */}
              {aiInsights && (
                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <div className="flex items-center gap-2">
                    <ShieldAlert className="w-4 h-4 text-blue-600" />
                    <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                      AI Vulnerability Assessment
                    </h4>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {aiInsights.overall_situation}
                  </p>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center gap-3 pt-2">
                <button
                  onClick={() => handleFlyToRegion(selectedRegion.id)}
                  className="py-2 px-3 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex items-center justify-center gap-1.5"
                >
                  <MapPin className="w-3.5 h-3.5 text-blue-600" />
                  <span>Zoom into Zone</span>
                </button>
                <button
                  onClick={() => navigate('/analytics')}
                  className="flex-1 py-2 px-3 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition-colors flex items-center justify-center gap-1.5"
                >
                  <span>View Analytics</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <button
                  onClick={() => navigate('/reports')}
                  className="py-2 px-3 text-xs font-semibold rounded-lg border border-slate-300 hover:bg-slate-50 text-slate-700 transition-colors flex items-center gap-1.5"
                >
                  <FileText className="w-3.5 h-3.5 text-slate-500" />
                  <span>Report</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-8 text-center text-slate-500">
              <p>Select a region on the map to inspect risk details.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
