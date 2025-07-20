/** @type {import('next').NextConfig} */
const nextConfig = {
  // Vercel deployment configuration
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
