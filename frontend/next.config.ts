import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 1) Disable ESLint errors during builds:
  eslint: {
    ignoreDuringBuilds: true,
  },

  // 2) Disable TypeScript type‑checking errors during builds:
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
