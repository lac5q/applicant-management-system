/** @type {import('next').NextConfig} */
const nextConfig = {
  // Vercel deployment configuration
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  // Enable experimental features for better performance
  experimental: {
    optimizeCss: true
  }
}

module.exports = nextConfig
