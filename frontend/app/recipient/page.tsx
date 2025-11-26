'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

interface Donation {
  donation_id: number
  food_type: string
  quantity_lbs: number
  address: string
  match_scores: Array<{
    recipient_id: number
    recipient_name: string
    score: number
    distance_miles: number
  }>
}

export default function RecipientPage() {
  const [donations, setDonations] = useState<Donation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDonations = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const response = await axios.get(`${apiUrl}/donations?status=pending`)
        setDonations(response.data)
      } catch (error) {
        console.error('Error fetching donations:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDonations()
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Available Donations</h1>
          <p className="text-gray-600">View and accept food donations matched to your organization</p>
        </div>

        {loading ? (
          <div className="text-center py-12">Loading donations...</div>
        ) : donations.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <p className="text-gray-600">No available donations at this time.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {donations.map((donation) => (
              <div key={donation.donation_id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-gray-900">{donation.food_type}</h3>
                  <span className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-semibold">
                    {donation.quantity_lbs} lbs
                  </span>
                </div>
                
                <div className="space-y-2 mb-4">
                  <p className="text-gray-600">
                    <span className="font-semibold">Location:</span> {donation.address}
                  </p>
                  
                  {donation.match_scores && donation.match_scores.length > 0 && (
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Match Score: {donation.match_scores[0].score.toFixed(2)}</p>
                      <p className="text-sm text-gray-500">Distance: {donation.match_scores[0].distance_miles.toFixed(1)} miles</p>
                    </div>
                  )}
                </div>

                <div className="flex space-x-2">
                  <button className="flex-1 bg-primary-600 text-white py-2 rounded-lg font-semibold hover:bg-primary-700 transition">
                    Accept
                  </button>
                  <button className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300 transition">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

