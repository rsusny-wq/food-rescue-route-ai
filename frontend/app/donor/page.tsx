'use client'

import { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/navigation'
import AddressAutocomplete from '@/components/AddressAutocomplete'

export default function DonorPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    donor_id: 1, // In production, get from auth
    food_type: '',
    food_category: 'packaged',
    quantity_lbs: '',
    pickup_window_start: '',
    pickup_window_end: '',
    address: '',
    storage_requirement: 'shelf_stable',
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      
      const donationData = {
        ...formData,
        quantity_lbs: parseFloat(formData.quantity_lbs),
        pickup_window_start: new Date(formData.pickup_window_start).toISOString(),
        pickup_window_end: new Date(formData.pickup_window_end).toISOString(),
      }

      const response = await axios.post(`${apiUrl}/donation`, donationData)
      setResult(response.data)
    } catch (error: any) {
      console.error('Error creating donation:', error)
      setResult({ error: error.response?.data?.detail || 'Failed to create donation' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Donate Food</h1>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Food Type
              </label>
              <input
                type="text"
                required
                value={formData.food_type}
                onChange={(e) => setFormData({ ...formData, food_type: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="e.g., Fresh vegetables, Prepared meals, Bakery items"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Food Category
              </label>
              <select
                value={formData.food_category}
                onChange={(e) => setFormData({ ...formData, food_category: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="produce">Produce</option>
                <option value="bakery">Bakery</option>
                <option value="prepared">Prepared Meals</option>
                <option value="packaged">Packaged</option>
                <option value="frozen">Frozen</option>
                <option value="dairy">Dairy</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quantity (lbs)
              </label>
              <input
                type="number"
                required
                step="0.1"
                min="0"
                value={formData.quantity_lbs}
                onChange={(e) => setFormData({ ...formData, quantity_lbs: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pickup Window Start
                </label>
                <input
                  type="datetime-local"
                  required
                  value={formData.pickup_window_start}
                  onChange={(e) => setFormData({ ...formData, pickup_window_start: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pickup Window End
                </label>
                <input
                  type="datetime-local"
                  required
                  value={formData.pickup_window_end}
                  onChange={(e) => setFormData({ ...formData, pickup_window_end: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Address <span className="text-xs text-gray-500">(Start typing for suggestions)</span>
              </label>
              <AddressAutocomplete
                value={formData.address}
                onChange={(address) => setFormData({ ...formData, address })}
                placeholder="123 Broadway, New York, NY 10001"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Storage Requirement
              </label>
              <select
                value={formData.storage_requirement}
                onChange={(e) => setFormData({ ...formData, storage_requirement: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="hot">Hot</option>
                <option value="cold">Cold</option>
                <option value="frozen">Frozen</option>
                <option value="shelf_stable">Shelf Stable</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Submitting...' : 'Submit Donation'}
            </button>
          </form>

          {result && (
            <div className={`mt-6 p-4 rounded-lg ${result.error ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'}`}>
              {result.error ? (
                <div className="text-red-800">
                  <strong>Error:</strong> {result.error}
                </div>
              ) : (
                <div>
                  <h3 className="font-semibold text-green-800 mb-2">Donation Created Successfully!</h3>
                  <p className="text-green-700 mb-4">Donation ID: {result.donation_id}</p>
                  
                  {result.match_scores && result.match_scores.length > 0 && (
                    <div>
                      <p className="font-semibold text-green-800 mb-2">Top Matched Recipients:</p>
                      <ul className="list-disc list-inside space-y-1">
                        {result.match_scores.slice(0, 3).map((match: any, idx: number) => (
                          <li key={idx} className="text-green-700">
                            {match.recipient_name} - Score: {match.score.toFixed(2)} ({match.distance_miles.toFixed(1)} miles)
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

