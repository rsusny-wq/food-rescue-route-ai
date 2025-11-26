'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import axios from 'axios'

interface ImpactData {
  lbs_rescued: number
  meals: number
  co2e_avoided: number
  ch4_avoided_tons: number
  landfill_space_saved: number
}

export default function Home() {
  const [impact, setImpact] = useState<ImpactData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchImpact = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/impact`)
        setImpact(response.data)
      } catch (error) {
        console.error('Error fetching impact:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchImpact()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Food Rescue Route AI
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Intelligent Food Recovery & Route Optimization Platform for NYC
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/donor"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
            >
              Donate Food
            </Link>
            <Link
              href="/recipient"
              className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold border-2 border-primary-600 hover:bg-primary-50 transition"
            >
              Receive Food
            </Link>
            <Link
              href="/driver"
              className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold border-2 border-primary-600 hover:bg-primary-50 transition"
            >
              Volunteer to Drive
            </Link>
          </div>
        </div>

        {/* Impact Metrics */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            Our Impact
          </h2>
          {loading ? (
            <div className="text-center py-8">Loading impact metrics...</div>
          ) : impact ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-3xl font-bold text-primary-600">
                  {impact.lbs_rescued.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Lbs Rescued</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600">
                  {impact.meals.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Meals Provided</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-3xl font-bold text-purple-600">
                  {impact.co2e_avoided.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600 mt-2">Lbs CO₂e Avoided</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-3xl font-bold text-orange-600">
                  {impact.ch4_avoided_tons.toFixed(3)}
                </div>
                <div className="text-sm text-gray-600 mt-2">Tons CH₄ Avoided</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-3xl font-bold text-yellow-600">
                  {impact.landfill_space_saved.toFixed(1)}
                </div>
                <div className="text-sm text-gray-600 mt-2">Cubic Yards Saved</div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No impact data available yet. Start donating food to see impact!
            </div>
          )}
        </div>

        {/* How It Works */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-4">🍽️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Donors Post Food</h3>
            <p className="text-gray-600">
              Restaurants, groceries, and cafeterias list surplus food with pickup windows and quantities.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">AI Matches & Routes</h3>
            <p className="text-gray-600">
              Our AI matches donations with recipients and optimizes routes for volunteer drivers.
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-4">🚗</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Food Gets Delivered</h3>
            <p className="text-gray-600">
              Volunteers pick up and deliver food to food banks, shelters, and community fridges.
            </p>
          </div>
        </div>

        {/* Features */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
            Key Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex items-start">
              <div className="text-2xl mr-4">✅</div>
              <div>
                <h4 className="font-semibold text-gray-900">Intelligent Matching</h4>
                <p className="text-gray-600">AI matches food donations with recipients based on category, capacity, and distance.</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-4">🗺️</div>
              <div>
                <h4 className="font-semibold text-gray-900">Route Optimization</h4>
                <p className="text-gray-600">Optimized routes minimize travel time and maximize food saved.</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-4">📊</div>
              <div>
                <h4 className="font-semibold text-gray-900">Impact Tracking</h4>
                <p className="text-gray-600">Real-time metrics on meals provided, CO₂e avoided, and landfill space saved.</p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="text-2xl mr-4">⚡</div>
              <div>
                <h4 className="font-semibold text-gray-900">Real-Time Updates</h4>
                <p className="text-gray-600">Live tracking of donations, routes, and deliveries.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

