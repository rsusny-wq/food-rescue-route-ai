import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import 'leaflet/dist/leaflet.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Food Rescue Route AI',
  description: 'Intelligent Food Recovery & Route Optimization Platform for NYC',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <Link href="/" className="flex items-center">
                  <span className="text-2xl font-bold text-primary-600">
                    🍎 Food Rescue Route AI
                  </span>
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/donor" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                  Donor
                </Link>
                <Link href="/recipient" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                  Recipient
                </Link>
                <Link href="/driver" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                  Driver
                </Link>
                <Link href="/admin" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                  Admin
                </Link>
                <Link href="/admin/sustainability" className="text-gray-700 hover:text-primary-600 px-3 py-2">
                  Sustainability
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}

