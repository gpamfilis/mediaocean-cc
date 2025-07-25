"use client";
import SummaryComponent from "./SummaryComponent";

import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { useState } from "react";
import { usePathname, useRouter as useNextRouter } from "next/navigation";
import { Box, Container } from "@mui/material";
import AnomaliesComponent from "./Anomalies";
import Header from "@/components/header/Header";

// console.log(`BACKEND_DOMAIN: ${process.env.NEXT_PUBLIC_BACKEND_DOMAIN}`);

const DashboardPage = ({ params }) => {
  const [value, setValue] = useState("1");
  const pathname = usePathname();
  const nextRouter = useNextRouter();

  const handleChange = (event, newValue) => {
    setValue(newValue);
    // Update query param
    const url = `${pathname}?currentTab=${newValue}`;
    nextRouter.replace(url);
  };

  return (
    <Container>
      <Header />
      <TabContext value={value}>
        <Box
          sx={{
            position: "fixed",
            top: "80px", // Adjust based on the height of your header
            width: "100%",
            zIndex: 1000,
            borderBottom: 1,
            borderColor: "divider",
          }}
        >
          <TabList onChange={handleChange} aria-label="lab API tabs example">
            <Tab label="Summary" value="1" />
            <Tab label="Anomalies" value="2" />
          </TabList>
        </Box>
        <Box sx={{ mb: 4 }}>
          <TabPanel value="1">
            <SummaryComponent params={params} />
          </TabPanel>
          <TabPanel value="2">
            <AnomaliesComponent params={params} />
          </TabPanel>
        </Box>
      </TabContext>
    </Container>
  );
};

export default DashboardPage;
