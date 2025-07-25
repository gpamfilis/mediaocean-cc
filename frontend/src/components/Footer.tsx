import React from "react";
import { Box, Typography, Link } from "@mui/material";
import { useRouter } from "next/navigation";

const FOOTER_HEIGHT = "60px"; // Constant for the footer height

const Footer = () => {
  const router = useRouter();

  return (
    <Box
      style={{
        minHeight: FOOTER_HEIGHT,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        position: "fixed",
        bottom: 0,
        width: "100%",
        backgroundColor: "black",
      }}
    >
      <Typography variant="body2" color={"white"} align="center">
        © 2025{" "}
        <Link
          href="https://mediaocean.com"
          target="_blank"
          rel="noopener noreferrer"
          sx={{ color: "white" }}
        >
          mediaocean.com
        </Link>
      </Typography>
      <Typography variant="body2" color="text.primary" align="center">
        <Link
          href="/terms"
          onClick={() => router.push("/terms")}
          sx={{ color: "white", marginLeft: "10px", cursor: "pointer" }}
        >
          Terms
        </Link>
        <Link
          href="/privacy"
          onClick={() => router.push("/privacy")}
          sx={{ color: "white", marginLeft: "10px", cursor: "pointer" }}
        >
          Privacy
        </Link>
      </Typography>
    </Box>
  );
};

export default Footer;
