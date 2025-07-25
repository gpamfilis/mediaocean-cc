import React from "react";
import { Typography, Box } from "@mui/material";

const HeroSection = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: { xs: "space-evenly", sm: "center" },
        height: "100vh",
        padding: { xs: 2, md: 0 },
      }}
      id="herosection"
    >
      <Box sx={{ maxWidth: { xs: "90vw", md: "50vw" } }}>
        <Typography
          variant="h2"
          gutterBottom
          color="primary"
          sx={{
            fontSize: { xs: "2rem", md: "3rem" },
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          Protect the Digital Advertising Ecosystem.{"\n"}
          Detect Fraud with Precision.
        </Typography>
        <Typography
          variant="h3"
          gutterBottom
          color="primary"
          sx={{ fontSize: { xs: "1.5rem", md: "2rem" } }}
        >
          Analyze ad content, uncover anomalies, and ensure brand safety with
          advanced detection tools.
        </Typography>
        <Typography
          variant="subtitle1"
          gutterBottom
          color="primary"
          sx={{ fontSize: { xs: "1rem", md: "1.25rem" } }}
        >
          Identify suspicious patterns, flag potential bots, and maintain trust
          in digital advertising campaigns.
        </Typography>
      </Box>
    </Box>
  );
};

export default HeroSection;
