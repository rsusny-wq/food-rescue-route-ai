'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

interface Route {
  route_id: number
  status: string
  estimated_duration_minutes: number
  estimated_distance_miles: number
  instructions: Array<{
    instruction: string
    distance: string
    duration: string
  }>
}

export default function DriverPage() {
  const [routes, setRoutes] = useState<Route[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedRoute, setSelectedRoute] = useState<Route | null>(null)

  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/routes?status=assigned`)
        setRoutes(response.data)
      } catch (error) {
        console.error('Error fetching routes:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchRoutes()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Available Routes</h1>
          <p className="text-gray-600">Accept routes to pick up and deliver food donations</p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading routes...</div>
        ) : routes.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <p className="text-gray-600">No available routes at this time.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {routes.map((route) => (
              <div key={route.route_id} className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-gray-900">Route #{route.route_id}</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    route.status === 'assigned' ? 'bg-yellow-100 text-yellow-800' :
                    route.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {route.status.replace('_', ' ')}
                  </span>
                </div>

                <div className="space-y-2 mb-4">
                  <p className="text-gray-600">
                    <span className="font-semibold">Distance:</span> {route.estimated_distance_miles.toFixed(1)} miles
                  </p>
                  <p className="text-gray-600">
                    <span className="font-semibold">Estimated Time:</span> {route.estimated_duration_minutes.toFixed(0)} minutes
                  </p>
                </div>

                {route.instructions && route.instructions.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Route Instructions:</h4>
                    <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                      {route.instructions.slice(0, 3).map((instruction, idx) => (
                        <li key={idx}>{instruction.instruction}</li>
                      ))}
                      {route.instructions.length > 3 && (
                        <li className="text-primary-600">...and {route.instructions.length - 3} more steps</li>
                      )}
                    </ol>
                  </div>
                )}

                <div className="flex space-x-2">
                  <button
                    onClick={() => setSelectedRoute(route)}
                    className="flex-1 bg-primary-600 text-white py-2 rounded-lg font-semibold hover:bg-primary-700 transition"
                  >
                    Accept Route
                  </button>
                  <button className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300 transition">
                    View Map
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {selectedRoute && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-xl shadow-xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Route Details</h2>
              
              {selectedRoute.instructions && (
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Turn-by-Turn Directions:</h3>
                  <ol className="list-decimal list-inside space-y-2">
                    {selectedRoute.instructions.map((instruction, idx) => (
                      <li key={idx} className="text-gray-700">
                        <div dangerouslySetInnerHTML={{ __html: instruction.instruction }} />
                        <span className="text-sm text-gray-500 ml-2">
                          ({instruction.distance} • {instruction.duration})
                        </span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}

              <div className="mt-6 flex space-x-2">
                <button
                  onClick={() => setSelectedRoute(null)}
                  className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300 transition"
                >
                  Close
                </button>
                <button className="flex-1 bg-primary-600 text-white py-2 rounded-lg font-semibold hover:bg-primary-700 transition">
                  Start Route
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

