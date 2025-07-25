"use client";
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#e4e5ea",
    },
    secondary: {
      main: "#f48fb1",
    },
    error: {
      main: "#ff6b6b",
    },
    success: {
      main: "#4caf50",
    },
    background: {
      default: "black",
    },
  },
});

export default theme;
