'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface SustainabilityData {
  lbs_rescued: number
  meals: number
  co2e_avoided: number
  ch4_avoided_tons: number
  landfill_space_saved: number
  potential_impact: any
  pending_donations: number
  active_routes: number
  total_donations: number
  ai_insight: string
  sustainability_score: number
}

const COLORS = ['#22c55e', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444']

export default function SustainabilityPage() {
  const [data, setData] = useState<SustainabilityData | null>(null)
  const [loading, setLoading] = useState(true)
  const [historicalData, setHistoricalData] = useState<any[]>([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/impact/realtime`)
        setData(response.data)
        
        // Generate historical data for visualization
        const historical = []
        for (let i = 6; i >= 0; i--) {
          const date = new Date()
          date.setDate(date.getDate() - i)
          historical.push({
            date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            co2e: (response.data.co2e_avoided / 7) * (7 - i) + Math.random() * 100,
            meals: (response.data.meals / 7) * (7 - i) + Math.random() * 50,
            lbs: (response.data.lbs_rescued / 7) * (7 - i) + Math.random() * 20
          })
        }
        setHistoricalData(historical)
      } catch (error) {
        console.error('Error fetching sustainability data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Update every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="text-center py-12">Loading sustainability metrics...</div>
  }

  if (!data) {
    return <div className="text-center py-12">No data available</div>
  }

  const impactBreakdown = [
    { name: 'CO₂e Avoided', value: data.co2e_avoided, color: '#22c55e' },
    { name: 'Meals Provided', value: data.meals, color: '#3b82f6' },
    { name: 'Landfill Space Saved', value: data.landfill_space_saved, color: '#8b5cf6' }
  ]

  const netZeroProgress = [
    { name: 'Current Impact', value: data.sustainability_score, color: '#22c55e' },
    { name: 'Remaining to Net Zero', value: 100 - data.sustainability_score, color: '#e5e7eb' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Sustainability & Net Zero Impact</h1>
          <p className="text-gray-600">Real-time environmental impact metrics aligned with SDG goals</p>
        </div>

        {/* Sustainability Score */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-sm font-semibold mb-2">Sustainability Score</div>
            <div className="text-4xl font-bold mb-2">{data.sustainability_score.toFixed(1)}/100</div>
            <div className="text-sm opacity-90">Progress to Net Zero</div>
            <div className="mt-4 bg-white bg-opacity-20 rounded-full h-2">
              <div 
                className="bg-white rounded-full h-2 transition-all duration-500"
                style={{ width: `${data.sustainability_score}%` }}
              ></div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-sm font-semibold mb-2">CO₂e Avoided</div>
            <div className="text-4xl font-bold mb-2">{data.co2e_avoided.toLocaleString()}</div>
            <div className="text-sm opacity-90">Pounds of CO₂ Equivalent</div>
            <div className="mt-2 text-xs opacity-75">
              Equivalent to {((data.co2e_avoided / 2000) * 0.45).toFixed(2)} tons CH₄ avoided
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <div className="text-sm font-semibold mb-2">Meals Provided</div>
            <div className="text-4xl font-bold mb-2">{data.meals.toLocaleString()}</div>
            <div className="text-sm opacity-90">From {data.lbs_rescued.toLocaleString()} lbs rescued</div>
          </div>
        </div>

        {/* AI Insight */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">AI-Powered Insights</h2>
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
            <p className="text-gray-800">{data.ai_insight}</p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Historical Trend */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">7-Day Impact Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="co2e" stroke="#22c55e" name="CO₂e (lbs)" />
                <Line type="monotone" dataKey="meals" stroke="#3b82f6" name="Meals" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Impact Breakdown */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Impact Breakdown</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={impactBreakdown}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value.toFixed(0)}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {impactBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* SDG Alignment */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">UN Sustainable Development Goals (SDG) Alignment</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">SDG 2</div>
              <div className="text-sm text-gray-700 mt-1">Zero Hunger</div>
              <div className="text-xs text-gray-500 mt-1">{data.meals.toLocaleString()} meals</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">SDG 12</div>
              <div className="text-sm text-gray-700 mt-1">Responsible Consumption</div>
              <div className="text-xs text-gray-500 mt-1">{data.lbs_rescued.toLocaleString()} lbs</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">SDG 13</div>
              <div className="text-sm text-gray-700 mt-1">Climate Action</div>
              <div className="text-xs text-gray-500 mt-1">{data.co2e_avoided.toLocaleString()} lbs CO₂e</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">SDG 11</div>
              <div className="text-sm text-gray-700 mt-1">Sustainable Cities</div>
              <div className="text-xs text-gray-500 mt-1">{data.landfill_space_saved.toFixed(1)} cu yds</div>
            </div>
          </div>
        </div>

        {/* Net Zero Progress */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Net Zero Carbon Progress</h2>
          <div className="mb-4">
            <div className="flex justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Progress to Net Zero</span>
              <span className="text-sm font-bold text-green-600">{data.sustainability_score.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div 
                className="bg-gradient-to-r from-green-500 to-green-600 h-4 rounded-full transition-all duration-500"
                style={{ width: `${data.sustainability_score}%` }}
              ></div>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4 mt-6">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-sm text-gray-600">Carbon Offset</div>
              <div className="text-2xl font-bold text-green-600">
                {(data.co2e_avoided / 2000).toFixed(2)} tons
              </div>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm text-gray-600">Methane Avoided</div>
              <div className="text-2xl font-bold text-blue-600">
                {data.ch4_avoided_tons.toFixed(3)} tons
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

