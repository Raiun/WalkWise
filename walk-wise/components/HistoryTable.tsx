/* eslint-disable jsx-a11y/anchor-is-valid */
"use client"

import React, { useState, useEffect } from "react";
import { ColorPaletteProp } from '@mui/joy/styles';
import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Chip from '@mui/joy/Chip';
import Divider from '@mui/joy/Divider';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Link from '@mui/joy/Link';
import Input from '@mui/joy/Input';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import ModalClose from '@mui/joy/ModalClose';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';
import Checkbox from '@mui/joy/Checkbox';
import IconButton, { iconButtonClasses } from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import Menu from '@mui/joy/Menu';
import MenuButton from '@mui/joy/MenuButton';
import MenuItem from '@mui/joy/MenuItem';
import Dropdown from '@mui/joy/Dropdown';

import FilterAltIcon from '@mui/icons-material/FilterAlt';
import SearchIcon from '@mui/icons-material/Search';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import BlockIcon from '@mui/icons-material/Block';
import AutorenewRoundedIcon from '@mui/icons-material/AutorenewRounded';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import MoreHorizRoundedIcon from '@mui/icons-material/MoreHorizRounded';
import { Card } from "@mui/joy";

const HistoryTable = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await fetch("http://127.0.0.1:8000/allUnlocks");
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

    const getStatusSymbol = (status: string) => {
      let statusSymbol;

      if (status == "Unlock") {
        statusSymbol = <CheckRoundedIcon></CheckRoundedIcon>
      }
      else if (status == "Lock") {
        statusSymbol = <BlockIcon></BlockIcon>
      }
      else {
        statusSymbol = <AutorenewRoundedIcon></AutorenewRoundedIcon>
      }

      return statusSymbol
    }

    return (
      <Sheet variant="soft" sx={{ pt: 1, borderRadius: 'sm', fontWeight: "bold" }}>
          <Table
            hoverRow
          >
          <thead>
          <tr>
              <th>Name</th>
              <th>Date</th>
              <th>Status</th>
          </tr>
          </thead>
          <tbody>
            {data.map((row) => (
                <tr key={row["name"]}>
                <td>{row["name"]}</td>
                <td>{row["date"]}</td>
                <td>{getStatusSymbol(row["status"])}{row["status"]}</td>
                </tr>
            ))}
          </tbody>
          </Table>
      </Sheet>
    )
} 

export default HistoryTable;