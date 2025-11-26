'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import dynamic from 'next/dynamic'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for default marker icons in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

const MapContainer = dynamic(() => import('react-leaflet').then(mod => mod.MapContainer), { ssr: false })
const TileLayer = dynamic(() => import('react-leaflet').then(mod => mod.TileLayer), { ssr: false })
const Marker = dynamic(() => import('react-leaflet').then(mod => mod.Marker), { ssr: false })
const Popup = dynamic(() => import('react-leaflet').then(mod => mod.Popup), { ssr: false })
const Polyline = dynamic(() => import('react-leaflet').then(mod => mod.Polyline), { ssr: false })

// NYC default center
const NYC_CENTER: [number, number] = [40.7128, -74.0060]

export default function AdminMapPage() {
  const [donations, setDonations] = useState<any[]>([])
  const [routes, setRoutes] = useState<any[]>([])
  const [routeDetails, setRouteDetails] = useState<Map<number, any>>(new Map())
  const [loading, setLoading] = useState(true)
  const [selectedRoute, setSelectedRoute] = useState<number | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        
        const [donationsRes, routesRes] = await Promise.all([
          axios.get(`${apiUrl}/donations`),
          axios.get(`${apiUrl}/routes`)
        ])

        setDonations(donationsRes.data)
        setRoutes(routesRes.data)

        // Fetch route details for visualization
        const detailsMap = new Map()
        for (const route of routesRes.data) {
          try {
            const routeDetail = await axios.get(`${apiUrl}/routes/${route.route_id}/map`)
            detailsMap.set(route.route_id, routeDetail.data)
          } catch (e) {
            console.error(`Error fetching route ${route.route_id}:`, e)
          }
        }
        setRouteDetails(detailsMap)
      } catch (error) {
        console.error('Error fetching map data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const getRoutePolyline = (routeId: number) => {
    const detail = routeDetails.get(routeId)
    if (detail && detail.start && detail.end) {
      return [
        [detail.start.lat, detail.start.lng],
        [detail.end.lat, detail.end.lng]
      ] as [number, number][]
    }
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Real-Time Route Visualization</h1>
          <p className="text-gray-600">Live map showing donations, recipients, and optimized routes</p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading map data...</div>
        ) : (
          <div className="bg-white rounded-xl shadow-lg p-4">
            <MapContainer
              center={NYC_CENTER}
              zoom={12}
              style={{ height: '700px', width: '100%' }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {/* Route polylines */}
              {routes.map((route) => {
                const polyline = getRoutePolyline(route.route_id)
                if (polyline) {
                  return (
                    <Polyline
                      key={`route-${route.route_id}`}
                      positions={polyline}
                      color={selectedRoute === route.route_id ? '#ef4444' : '#3b82f6'}
                      weight={4}
                      opacity={0.7}
                    />
                  )
                }
                return null
              })}
              
              {/* Donation markers (pickup points) */}
              {donations.map((donation) => {
                const lat = donation.latitude || NYC_CENTER[0] + (Math.random() - 0.5) * 0.1
                const lng = donation.longitude || NYC_CENTER[1] + (Math.random() - 0.5) * 0.1
                
                return (
                  <Marker 
                    key={`donation-${donation.donation_id}`} 
                    position={[lat, lng]}
                    icon={L.icon({
                      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                      iconSize: [25, 41],
                      iconAnchor: [12, 41],
                    })}
                  >
                    <Popup>
                      <div>
                        <strong>Donation #{donation.donation_id}</strong>
                        <p className="text-sm mt-1">{donation.food_type}</p>
                        <p className="text-sm font-semibold text-green-600">{donation.quantity_lbs} lbs</p>
                        <p className="text-xs text-gray-500 mt-1">Status: {donation.status}</p>
                        {donation.match_scores && donation.match_scores.length > 0 && (
                          <p className="text-xs text-blue-600 mt-1">
                            Top match: {donation.match_scores[0].recipient_name}
                          </p>
                        )}
                      </div>
                    </Popup>
                  </Marker>
                )
              })}

              {/* Route start/end markers */}
              {Array.from(routeDetails.entries()).map(([routeId, detail]) => {
                if (!detail.start || !detail.end) return null
                
                return (
                  <div key={`route-markers-${routeId}`}>
                    <Marker 
                      position={[detail.start.lat, detail.start.lng]}
                      icon={L.icon({
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                      })}
                    >
                      <Popup>
                        <div>
                          <strong>Route #{routeId} - Start</strong>
                          <p className="text-sm">{detail.start.address}</p>
                          <p className="text-xs text-gray-500">Distance: {detail.distance_miles?.toFixed(1)} miles</p>
                          <p className="text-xs text-gray-500">Duration: {detail.duration_minutes?.toFixed(0)} min</p>
                        </div>
                      </Popup>
                    </Marker>
                    <Marker 
                      position={[detail.end.lat, detail.end.lng]}
                      icon={L.icon({
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                      })}
                    >
                      <Popup>
                        <div>
                          <strong>Route #{routeId} - End</strong>
                          <p className="text-sm">{detail.end.address}</p>
                        </div>
                      </Popup>
                    </Marker>
                  </div>
                )
              })}
            </MapContainer>
          </div>
        )}

        {/* Route List */}
        <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Active Routes</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {routes.map((route) => {
              const detail = routeDetails.get(route.route_id)
              return (
                <div
                  key={route.route_id}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition ${
                    selectedRoute === route.route_id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedRoute(route.route_id)}
                >
                  <div className="font-semibold text-gray-900">Route #{route.route_id}</div>
                  <div className="text-sm text-gray-600 mt-1">
                    {detail?.distance_miles ? `${detail.distance_miles.toFixed(1)} miles` : 'N/A'}
                  </div>
                  <div className="text-sm text-gray-600">
                    {detail?.duration_minutes ? `${detail.duration_minutes.toFixed(0)} min` : 'N/A'}
                  </div>
                  <div className="text-xs text-gray-500 mt-2">Status: {route.status}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
