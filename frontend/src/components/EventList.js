import { React } from "react";
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography } from "@mui/material";

const EventList = ({events}) => {


  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString(); // 
  };

  return (
    <TableContainer component={Paper}>
      <Table aria-label="event table">
        <TableHead>
          <TableRow>
            <TableCell><strong>Event Name</strong></TableCell>
            <TableCell><strong>Start Time</strong></TableCell>
            <TableCell><strong>End Time</strong></TableCell>
            <TableCell><strong>Duration</strong></TableCell>
            <TableCell><strong>Repeat Days</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {events.map((event) => (
            <TableRow key={event.id}>
              <TableCell>{event.name}</TableCell>
              <TableCell>{formatDate(event.start_time)}</TableCell>
              <TableCell>{formatDate(event.end_time)}</TableCell>
              <TableCell>{event.duration}</TableCell>
              <TableCell>
                {event.repeat_days ? event.repeat_days : "Once"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default EventList;
