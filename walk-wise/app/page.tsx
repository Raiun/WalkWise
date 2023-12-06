"use client"
import Image from "next/image"
//import styles from "./page.module.css"
import React, { useState, useEffect } from "react";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Box from "@mui/joy/Box";
import Card from "@mui/joy/Card";
import Button from "@mui/joy/Button";
import Breadcrumbs from "@mui/joy/Breadcrumbs";
import Link from "@mui/joy/Link";
import Typography from "@mui/joy/Typography";

import HomeRoundedIcon from "@mui/icons-material/HomeRounded";
import ChevronRightRoundedIcon from "@mui/icons-material/ChevronRightRounded";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";

//import useScript from "./useScript";
import Sidebar from "../components/Sidebar";
import OrderTable from "../components/OrderTable";
import OrderList from "../components/OrderList";

import animation from "../public/walking.gif"

export default function Home() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/authorizedUsers");
        const jsonData = await response.json();
        console.log(jsonData);
        setData(JSON.parse(jsonData));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();

    return () => {
      // Cleanup logic here (if needed)
    };
  }, []);

  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Box sx={{ display: "flex", minHeight: "100dvh" }}>
        <Sidebar />
        <Box
          component="main"
          className="MainContent"
          sx={{
            px: { xs: 2, md: 6 },
            pt: {
              xs: "calc(12px + var(--Header-height))",
              sm: "calc(12px + var(--Header-height))",
              md: 3,
            },
            pb: { xs: 2, sm: 2, md: 3 },
            flex: 1,
            display: "flex",
            flexDirection: "column",
            minWidth: 0,
            height: "100dvh",
            gap: 1,
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center" }}>
            <Breadcrumbs
              size="sm"
              aria-label="breadcrumbs"
              separator={<ChevronRightRoundedIcon fontSize="sm" />}
              sx={{ pl: 0 }}
            >
              <Link
                underline="none"
                color="neutral"
                href="#Home"
                aria-label="Home"
              >
                <HomeRoundedIcon />
              </Link>
            </Breadcrumbs>
          </Box>
          <Card>
            <h1>Welcome to WalkWise!</h1>
            <p>WalkWise utilizes Arduino streamed IMU data to recognize and identify users by
              their stride patterns to unlock smart locked doors automatically.</p>
            <img style={{margin: "auto", width: "500px", height: "400px"}} src="https://mir-s3-cdn-cf.behance.net/project_modules/hd/72f02440701089.57894e458a58b.gif"></img>
            {data[0] ? <p>{data[0]["name"]}</p> : <p></p>}
          </Card>
        </Box>
      </Box>
    </CssVarsProvider>
  );
}