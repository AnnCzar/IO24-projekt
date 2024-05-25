import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { ReactComponent as GoBack } from "../images/back.svg";
import { ReactComponent as DeletePatient } from "../images/delete.svg";

import './AllPatients.css';

interface Column {
  id: 'patients_id' | 'name' | 'sex' | 'email' | 'date_of_last_exam';
  label: string;
  minWidth?: number;
  align?: 'center';
  format?: (value: any) => string;
}

const columns: readonly Column[] = [
  { id: 'patients_id', label: 'Patients ID', minWidth: 170 },
  { id: 'name', label: 'Name', minWidth: 100, align: 'center' },
  {
    id: 'sex',
    label: 'Sex',
    minWidth: 170,
    align: 'center',
    format: (value: string) => value,
  },
  {
    id: 'email',
    label: 'Email',
    minWidth: 170,
    align: 'center',
    format: (value: string) => value,
  },
  {
    id: 'date_of_last_exam',
    label: 'Date of the last examination',
    minWidth: 170,
    align: 'center',
    format: (value: string) => new Date(value).toLocaleDateString('en-US'),
  },
];

interface Data {
  patients_id: number;
  name: string;
  sex: string;
  email: string;
  date_of_last_exam: string;
}

// Example rows data
const rows: Data[] = [
  { patients_id: 1, name: 'John Doe', sex: 'Male', email: 'john.doe@example.com', date_of_last_exam: '2023-05-15' },
  { patients_id: 2, name: 'Jane Smith', sex: 'Female', email: 'jane.smith@example.com', date_of_last_exam: '2022-12-20' },
  // Add more rows as needed
];

export default function AllPatients() {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <div className="background">
      <header className="header">ALL PATIENTS</header>
      <button className="go-back" >
        <GoBack />
        <span>Go back</span>
      </button>
      <button className="delete-patient">
        <DeletePatient className="icon" />
        <span>Delete patient</span>
      </button>
      <div className="table-container-wrapper">
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer className="table-container" sx={{ maxHeight: 440 }}>
            <Table stickyHeader aria-label="sticky table" className="table">
              <TableHead>
                <TableRow className="table-header">
                  {columns.map((column, index) => (
                    <TableCell
                      key={column.id}
                      align={index === 0 ? 'center' : column.align}
                      style={{ minWidth: column.minWidth }}
                      className={`no-bottom-border`}
                    >
                      <b>{column.label}</b>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {rows
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row) => {
                    return (
                      <TableRow hover role="checkbox" tabIndex={-1} key={row.patients_id}>
                        {columns.map((column) => {
                          const value = row[column.id as keyof Data];
                          return (
                            <TableCell key={column.id} align="center" className="no-bottom-border">
                              {column.format && typeof value !== 'undefined'
                                ? column.format(value)
                                : value}
                            </TableCell>
                          );
                        })}
                      </TableRow>
                    );
                  })}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[10, 25, 100]}
            component="div"
            count={rows.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </div>
    </div>
  );
}
