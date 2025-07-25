"use client";
import React, { useState, useEffect } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  Slider,
} from "@mui/material";
import axios from "axios";
import toast from "react-hot-toast";

const SummaryComponent = ({ params }) => {
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [maxNumberOfUsers, setMaxNumberOfUsers] = useState(3);
  const [limitWords, setLimitWords] = useState(10);

  useEffect(() => {
    fetchSummaryData();
  }, []);

  useEffect(() => {
    if (summaryData) {
      fetchSummaryData();
    }
  }, [maxNumberOfUsers, limitWords]);

  const fetchSummaryData = async () => {
    try {
      setLoading(true);
      const backendDomain =
        process.env.NEXT_PUBLIC_BACKEND_DOMAIN || "http://167.172.181.29:5000";
      const response = await axios.get(`${backendDomain}/api/v1/summary`, {
        params: {
          max_number_of_users: maxNumberOfUsers,
          limit_words: limitWords,
        },
      });

      setSummaryData(response.data.data);
      toast.success("Summary data loaded successfully", { id: "success" });
    } catch (err) {
      toast.error("Failed to fetch summary data");
      console.error("Error fetching summary:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Typography variant="h5" mt={20}>
        Loading...
      </Typography>
    );
  }

  if (!summaryData) {
    return <Typography variant="h1">No summary data available</Typography>;
  }

  const DashBoardControls = () => {
    return (
      <Card elevation={2} sx={{ mb: 3, mt: 10 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            Dashboard Controls
          </Typography>

          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} sm={6}>
              <Typography>Max Number of Users: {maxNumberOfUsers}</Typography>
              <Slider
                value={maxNumberOfUsers}
                onChange={(e, newValue) => setMaxNumberOfUsers(newValue)}
                min={1}
                max={10}
                step={1}
                marks={[
                  { value: 1, label: "1" },
                  { value: 5, label: "5" },
                  { value: 10, label: "10" },
                ]}
                color="primary"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography>Word Limit: {limitWords}</Typography>
              <Slider
                value={limitWords}
                onChange={(e, newValue) => setLimitWords(newValue)}
                min={5}
                max={50}
                step={1}
                marks={[
                  { value: 5, label: "5" },
                  { value: 25, label: "25" },
                  { value: 50, label: "50" },
                ]}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const TopUsersSection = ({ topUsers }) => {
    return (
      <Card elevation={3}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Typography variant="h6" fontWeight="bold">
              Users by Unique Words
            </Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />

          <List
            sx={{
              overflow: "auto",
              maxHeight: "400px",
            }}
          >
            {topUsers.map((user, index) => (
              <ListItem key={user.user_id} sx={{ px: 0 }}>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography>Rank: {index + 1}</Typography>
                      <Typography variant="subtitle1" fontWeight="bold">
                        {user.user.name} [ID:{user.user_id}]
                      </Typography>
                    </Box>
                  }
                  secondary={
                    <Box>
                      <Typography variant="body2">
                        {user.unique_word_count} unique words across{" "}
                        {user.post_count} posts
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    );
  };

  const MostFrequentWordsSection = () => {
    return (
      <Card
        elevation={3}
        sx={{
          maxWidth: 500,
        }}
      >
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Typography variant="h6" fontWeight="bold">
              Top {limitWords} Most Frequent Words
            </Typography>
          </Box>
          <Divider sx={{ mb: 2 }} />

          <Box display="flex" flexWrap="wrap" gap={1}>
            {summaryData.most_frequent_words.map((word) => {
              return (
                <Chip
                  key={word.name}
                  label={`${word.name} (${word.count})`}
                  variant="outlined"
                />
              );
            })}
          </Box>
        </CardContent>
      </Card>
    );
  };

  return (
    <Box p={2} mt={4} mb={5}>
      <DashBoardControls />

      <Grid container spacing={3}>
        <Grid item xs={4} md={4}>
          <TopUsersSection topUsers={summaryData.top_users} />
        </Grid>

        <Grid item xs={4} md={4}>
          <MostFrequentWordsSection />
        </Grid>
      </Grid>
    </Box>
  );
};

export default SummaryComponent;
