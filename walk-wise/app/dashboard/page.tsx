"use client"
import Image from "next/image"
//import styles from "./page.module.css"
import React, { useState, useEffect } from "react";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import Breadcrumbs from "@mui/joy/Breadcrumbs";
import Link from "@mui/joy/Link";
import Typography from "@mui/joy/Typography";
import Card from "@mui/joy/Card";

import HomeRoundedIcon from "@mui/icons-material/HomeRounded";
import ChevronRightRoundedIcon from "@mui/icons-material/ChevronRightRounded";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";

//import useScript from "./useScript";
import Sidebar from "../../components/Sidebar";
import OrderTable from "../../components/OrderTable";
import OrderList from "../../components/OrderList";
import DataCard from "../../components/DataCard";
import { Sheet } from "@mui/joy";

export default function dashboard() {
  const startScript = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/connectArduino");
    } catch (error) {
      console.error("Error:", error);
    }
  };

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
              <Link
                underline="hover"
                color="neutral"
                href="#Dashboard"
                fontSize={12}
                fontWeight={500}
              >
                Dashboard
              </Link>
            </Breadcrumbs>
          </Box>
          <Sheet>
            <Button
              color="primary"
              size="lg"
              onClick={startScript}
              sx={{margin: "2.5% 42.5%"}}
            >
              Start IMU Stream
            </Button>
            <DataCard></DataCard>
          </Sheet>
        </Box>
      </Box>
    </CssVarsProvider>
  );
}