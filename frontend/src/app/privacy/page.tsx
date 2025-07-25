"use client";
import { Button, Container } from "@mui/material";
import Markdown from "react-markdown";
import { ArrowBack } from "@mui/icons-material";
import { useRouter } from "next/navigation";

const privacy = "# Privacy Statement for Ad Insights Explorer Lite";

const Page = () => {
  const router = useRouter();
  return (
    <Container sx={{ mt: "4rem" }}>
      <Button startIcon={<ArrowBack />} onClick={() => router.back()}>
        Go Back
      </Button>
      <div style={{ color: "#fff" }}>
        <Markdown>{privacy}</Markdown>
      </div>
    </Container>
  );
};

export default Page;
