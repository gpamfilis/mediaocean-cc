"use client";
import React from "react";
import { AppBar, Toolbar, Box, Button } from "@mui/material";
import { useRouter } from "next/navigation";

const Header = () => {
  const router = useRouter();

  return (
    <>
      <AppBar position="fixed">
        <Toolbar>
          <Button
            sx={{
              color: "primary.main",
              my: 2,
              display: "block",
              fontWeight: "bold",
              textTransform: "none",
            }}
            onClick={() => router.push("/")}
          >
            Ad Insights Home
          </Button>

          <Box sx={{ flexGrow: 1 }} />

          <Box
            sx={{
              display: { md: "flex" },
              flexGrow: 1,
              justifyContent: "flex-start",
            }}
          ></Box>
          <Box marginLeft="auto" display="flex" alignItems="center">
            <Button
              sx={{
                color: "#e4e5ea",
                my: 2,
                display: "block",
                fontWeight: "bold",
              }}
              onClick={() => router.push("/dashboard")}
            >
              Go to APP
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
};

export default Header;
