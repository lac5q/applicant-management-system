/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  output: 'export',
  distDir: 'out',
  images: {
    domains: ['localhost'],
    unoptimized: true
  },
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/applicant-management-system' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/applicant-management-system/' : ''
}

module.exports = nextConfig
