/** @type {import('next').NextConfig} */
const nextConfig = {
  // Only enable static export for production builds
  output: process.env.NODE_ENV === 'production' ? 'export' : undefined,
  distDir: process.env.NODE_ENV === 'production' ? 'out' : '.next',
  basePath: process.env.NODE_ENV === 'production' ? '/applicant-management-system' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/applicant-management-system/' : '',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

module.exports = nextConfig
