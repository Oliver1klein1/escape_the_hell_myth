/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Serve static files from root directory
  async rewrites() {
    return [
      {
        source: '/:path*.html',
        destination: '/api/html/:path*',
      },
    ];
  },
};

module.exports = nextConfig;

