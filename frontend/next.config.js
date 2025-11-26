/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  webpack: (config) => {
    // Fix for Leaflet icons
    config.resolve.alias = {
      ...config.resolve.alias,
    };
    return config;
  },
  // For Netlify deployment
  images: {
    unoptimized: true,
  },
  // Ensure static export works if needed
  trailingSlash: false,
}

module.exports = nextConfig
