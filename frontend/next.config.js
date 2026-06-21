/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  // Prevent Next.js from redirecting /api/users/ → /api/users (308)
  trailingSlash: false,
  async rewrites() {
    return [
      // Match with trailing slash — forward as-is to FastAPI
      {
        source: '/api/:path*/',
        destination: 'http://localhost:8000/api/:path*/',
      },
      // Match without trailing slash — append slash for FastAPI
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*/',
      },
    ];
  },
};

module.exports = nextConfig;
