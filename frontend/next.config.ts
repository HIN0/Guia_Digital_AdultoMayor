import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Genera en .next/standalone un servidor Node autocontenido, con solo las
  // dependencias que la app usa realmente. Lo necesita frontend/Dockerfile
  // para producir una imagen pequeña (~200 MB en vez de ~1,5 GB).
  output: "standalone",
  turbopack: {
    root: path.resolve(__dirname),
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
      },
    ],
  },
};

export default nextConfig;
