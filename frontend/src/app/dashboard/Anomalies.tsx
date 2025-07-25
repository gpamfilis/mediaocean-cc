"use client";
import React, { useState, useEffect } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Paper,
  Chip,
  TextField,
  Grid,
  Slider,
  Button,
} from "@mui/material";
import axios from "axios";
import toast from "react-hot-toast";

const AnomaliesTable = ({ params }) => {
  const [anomaliesData, setAnomaliesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState("post_id");
  const [sortOrder, setSortOrder] = useState("asc");

  // Search filters
  const [searchUserId, setSearchUserId] = useState("");
  const [searchTitle, setSearchTitle] = useState("");
  const [searchPostId, setSearchPostId] = useState("");

  // Slider controls
  const [characterLimit, setCharacterLimit] = useState(15);
  const [similarityThreshold, setSimilarityThreshold] = useState(50);

  useEffect(() => {
    fetchAnomaliesData();
  }, []);

  // Auto-refresh when slider values change
  useEffect(() => {
    if (anomaliesData.length > 0) {
      fetchAnomaliesData();
    }
  }, [characterLimit, similarityThreshold, sortBy, sortOrder]);

  const fetchAnomaliesData = async () => {
    try {
      setLoading(true);
      const backendDomain =
        process.env.NEXT_PUBLIC_BACKEND_DOMAIN || "http://167.172.181.29:5000";
      const response = await axios.get(`${backendDomain}/api/v1/anomalies`, {
        params: {
          anomalies_character_limit: characterLimit,
          post_similarity_threshold: similarityThreshold,
          sort_by: sortBy,
          sort_order: sortOrder,
        },
      });

      setAnomaliesData(response.data.data.anomalies || []);
      toast.success("Anomalies data loaded successfully", {
        id: "success anomalies",
      });
    } catch (err) {
      const errorMessage =
        err.response?.data?.message || "Failed to fetch anomalies data";
      toast.error(errorMessage);
      console.error("Error fetching anomalies:", err);
    } finally {
      setLoading(false);
    }
  };

  const filteredData = anomaliesData.filter((item) => {
    const userIdMatch =
      searchUserId === "" ||
      item.user_id
        .toString()
        .toLowerCase()
        .includes(searchUserId.toLowerCase());

    const titleMatch =
      searchTitle === "" ||
      item.post_title.toLowerCase().includes(searchTitle.toLowerCase());

    const postIdMatch =
      searchPostId === "" ||
      item.post_id
        .toString()
        .toLowerCase()
        .includes(searchPostId.toLowerCase());

    return userIdMatch && titleMatch && postIdMatch;
  });

  const handleSort = (column) => {
    const isAsc = sortBy === column && sortOrder === "asc";
    setSortOrder(isAsc ? "desc" : "asc");
    setSortBy(column);
  };

  if (loading) {
    return (
      <Typography variant="h5" mt={20}>
        Loading...
      </Typography>
    );
  }

  return (
    <Box sx={{ p: 3, mt: 12 }}>
      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            Detection Parameters
          </Typography>

          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} sm={6}>
              <Typography>Character Limit: {characterLimit}</Typography>
              <Slider
                value={characterLimit}
                onChange={(e, newValue) => setCharacterLimit(newValue)}
                min={5}
                max={30}
                step={1}
                marks={[
                  { value: 5, label: "5" },
                  { value: 15, label: "15" },
                  { value: 30, label: "30" },
                ]}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography>
                Similarity Threshold: {similarityThreshold}%
              </Typography>
              <Slider
                value={similarityThreshold}
                onChange={(e, newValue) => setSimilarityThreshold(newValue)}
                min={10}
                max={90}
                step={1}
                marks={[
                  { value: 10, label: "10%" },
                  { value: 50, label: "50%" },
                  { value: 100, label: "90%" },
                ]}
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Showing {filteredData.length} of {anomaliesData.length} anomalies
        </Typography>
        <Button
          variant="outlined"
          size="small"
          onClick={() => {
            setSearchUserId("");
            setSearchTitle("");
            setSearchPostId("");
          }}
        >
          Clear All Filters
        </Button>
      </Box>

      {/* Anomalies Table */}
      <Card elevation={3}>
        <TableContainer
          component={Paper}
          sx={{
            overflow: "auto",
            maxHeight: "50vh",
          }}
        >
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell sx={{ py: 1 }}>
                  <TextField
                    fullWidth
                    value={searchUserId}
                    onChange={(e) => setSearchUserId(e.target.value)}
                    placeholder="Search User ID..."
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell sx={{ py: 1 }}>
                  <TextField
                    fullWidth
                    value={searchPostId}
                    onChange={(e) => setSearchPostId(e.target.value)}
                    placeholder="Search Post ID..."
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell sx={{ py: 1 }}>
                  <TextField
                    fullWidth
                    value={searchTitle}
                    onChange={(e) => setSearchTitle(e.target.value)}
                    placeholder="Search Title..."
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
              </TableRow>
              <TableRow>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === "user_id"}
                    direction={sortBy === "user_id" ? sortOrder : "asc"}
                    onClick={() => handleSort("user_id")}
                  >
                    User ID
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === "post_id"}
                    direction={sortBy === "post_id" ? sortOrder : "asc"}
                    onClick={() => handleSort("post_id")}
                  >
                    Post ID
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === "post_title"}
                    direction={sortBy === "post_title" ? sortOrder : "asc"}
                    onClick={() => handleSort("post_title")}
                  >
                    Title
                  </TableSortLabel>
                </TableCell>
                <TableCell>
                  <TableSortLabel
                    active={sortBy === "flag_reason"}
                    direction={sortBy === "flag_reason" ? sortOrder : "asc"}
                    onClick={() => handleSort("flag_reason")}
                  >
                    Flag Reason
                  </TableSortLabel>
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredData.map((item, index) => (
                <TableRow key={`${index}`} hover>
                  <TableCell>
                    <Chip
                      label={item.user_id}
                      variant="outlined"
                      size="small"
                      color="primary"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={item.post_id}
                      variant="outlined"
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography
                      variant="body2"
                      sx={{
                        maxWidth: 300,
                        overflow: "hidden",
                        textOverflow: "ellipsis",
                        whiteSpace: "nowrap",
                      }}
                      title={item.post_title}
                    >
                      {item.post_title}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={item.flag_reason}
                      size="small"
                      variant="outlined"
                    />
                  </TableCell>
                </TableRow>
              ))}
              {filteredData.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} align="center">
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ py: 3 }}
                    >
                      No anomalies found with current filters
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Card>
    </Box>
  );
};

export default AnomaliesTable;
