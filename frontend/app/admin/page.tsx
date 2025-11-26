'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'

interface ImpactData {
  lbs_rescued: number
  meals: number
  co2e_avoided: number
  ch4_avoided_tons: number
  landfill_space_saved: number
}

interface Donation {
  donation_id: number
  food_type: string
  quantity_lbs: number
  status: string
}

interface Route {
  route_id: number
  status: string
  estimated_duration_minutes: number
  estimated_distance_miles: number
}

export default function AdminPage() {
  const [impact, setImpact] = useState<ImpactData | null>(null)
  const [donations, setDonations] = useState<Donation[]>([])
  const [routes, setRoutes] = useState<Route[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        
        const [impactRes, donationsRes, routesRes] = await Promise.all([
          axios.get(`${apiUrl}/impact`),
          axios.get(`${apiUrl}/donations`),
          axios.get(`${apiUrl}/routes`)
        ])

        setImpact(impactRes.data)
        setDonations(donationsRes.data)
        setRoutes(routesRes.data)
      } catch (error) {
        console.error('Error fetching admin data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const pendingDonations = donations.filter(d => d.status === 'pending').length
  const activeRoutes = routes.filter(r => r.status === 'in_progress').length
  const completedRoutes = routes.filter(r => r.status === 'completed').length

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Real-time monitoring and optimization</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-3xl font-bold text-primary-600">{pendingDonations}</div>
            <div className="text-sm text-gray-600 mt-2">Pending Donations</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-3xl font-bold text-blue-600">{activeRoutes}</div>
            <div className="text-sm text-gray-600 mt-2">Active Routes</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-3xl font-bold text-green-600">{completedRoutes}</div>
            <div className="text-sm text-gray-600 mt-2">Completed Routes</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-3xl font-bold text-purple-600">
              {loading ? '...' : impact?.meals.toLocaleString() || 0}
            </div>
            <div className="text-sm text-gray-600 mt-2">Total Meals</div>
          </div>
        </div>

        {/* Impact Metrics */}
        {impact && (
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Impact Metrics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">
                  {impact.lbs_rescued.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Lbs Rescued</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {impact.meals.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Meals Provided</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {impact.co2e_avoided.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Lbs CO₂e Avoided</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-600">
                  {impact.ch4_avoided_tons.toFixed(3)}
                </div>
                <div className="text-sm text-gray-600 mt-2">Tons CH₄ Avoided</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">
                  {impact.landfill_space_saved.toFixed(1)}
                </div>
                <div className="text-sm text-gray-600 mt-2">Cubic Yards Saved</div>
              </div>
            </div>
          </div>
        )}

        {/* Recent Donations */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Recent Donations</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-4">ID</th>
                  <th className="text-left py-2 px-4">Food Type</th>
                  <th className="text-left py-2 px-4">Quantity (lbs)</th>
                  <th className="text-left py-2 px-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {donations.slice(0, 10).map((donation) => (
                  <tr key={donation.donation_id} className="border-b">
                    <td className="py-2 px-4">{donation.donation_id}</td>
                    <td className="py-2 px-4">{donation.food_type}</td>
                    <td className="py-2 px-4">{donation.quantity_lbs}</td>
                    <td className="py-2 px-4">
                      <span className={`px-2 py-1 rounded text-sm ${
                        donation.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        donation.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {donation.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Routes */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Recent Routes</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-2 px-4">Route ID</th>
                  <th className="text-left py-2 px-4">Distance (miles)</th>
                  <th className="text-left py-2 px-4">Duration (min)</th>
                  <th className="text-left py-2 px-4">Status</th>
                </tr>
              </thead>
              <tbody>
                {routes.slice(0, 10).map((route) => (
                  <tr key={route.route_id} className="border-b">
                    <td className="py-2 px-4">{route.route_id}</td>
                    <td className="py-2 px-4">{route.estimated_distance_miles?.toFixed(1) || 'N/A'}</td>
                    <td className="py-2 px-4">{route.estimated_duration_minutes?.toFixed(0) || 'N/A'}</td>
                    <td className="py-2 px-4">
                      <span className={`px-2 py-1 rounded text-sm ${
                        route.status === 'assigned' ? 'bg-yellow-100 text-yellow-800' :
                        route.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {route.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Links */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link href="/admin/map" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
            <h3 className="text-xl font-bold text-gray-900 mb-2">🗺️ View Real-Time Map</h3>
            <p className="text-gray-600">See all routes and donations visualized on an interactive map</p>
          </Link>
          <Link href="/admin/sustainability" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
            <h3 className="text-xl font-bold text-gray-900 mb-2">🌱 Sustainability Metrics</h3>
            <p className="text-gray-600">View Net Zero impact, CO₂e avoided, and SDG alignment</p>
          </Link>
        </div>
      </div>
    </div>
  )
}

