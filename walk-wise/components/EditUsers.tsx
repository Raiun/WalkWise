"use client"
import Image from "next/image"
//import styles from "./page.module.css"
import React, { useState, useEffect } from "react";
import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Box from "@mui/joy/Box";
import Avatar from '@mui/joy/Avatar';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import ListItemContent from '@mui/joy/ListItemContent';
import ListItemDecorator from '@mui/joy/ListItemDecorator';
import Typography from '@mui/joy/Typography';
import Card from "@mui/joy/Card";
import Button from '@mui/joy/Button';

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
  }, [data]);

  const updatePermissions = async (user: string) => {
    try {
      const response = await fetch("http://127.0.0.1:8000/updateAuthorizations/" + user, {method: "PUT"});
      const jsonData = await response.json();
      console.log(jsonData);
      setData(JSON.parse(jsonData));
      console.log(data)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <CssVarsProvider disableTransitionOnChange>
      <CssBaseline />
      <Box sx={{ width: "100%", display: "flex", flexWrap: "wrap" }}>
          {data.map((row) => (
              <Card sx={{width: "400px", margin: "10px 10px"}}>
                <ListItemDecorator>
                  <Avatar variant="outlined" />
                </ListItemDecorator>
                <ListItemContent>
                  <Typography level="title-sm">{row["name"]}</Typography>
                  <Typography level="body-sm" noWrap>
                    Auto-Unlock: {row["permitted"] ? "True" : "False"}
                    <Button 
                      sx={{marginLeft: "80px"}}
                      onClick={() => updatePermissions(row["name"])}
                      color={row["permitted"] ? "danger" : "success"}
                    >
                      {row["permitted"] ? "Disable Auto-Unlock" : "Enable Auto-Unlock"}
                    </Button>
                  </Typography>
                </ListItemContent>
              </Card>
          ))}
      </Box>
    </CssVarsProvider>
  );
}