"use client";
import { Box } from "@mui/material";
import HeroSection from "@/components/landing/heroSection";
import Header from "../components/header/Header";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <Header />
      <HeroSection />
      <Footer />
    </Box>
  );
}
