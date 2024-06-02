import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { ReactComponent as LogoutIcon } from "../images/logout.svg";
import { ReactComponent as AddPatient } from "../images/add_patient.svg";
import './Patients.css';
import {useNavigate} from "react-router-dom";
import {useCallback} from "react";

interface Column {
  id: 'patients_id' | 'sex' | 'date_of_birth' | 'pesel' | 'date_of_diagnosis';
  label: string;
  minWidth?: number;
  align?: 'center';
  format?: (value: any) => string;

}

const columns: readonly Column[] = [
  { id: 'patients_id', label: 'Patients ID', minWidth: 170 },
  { id: 'sex', label: 'Sex', minWidth: 100,align: "center" },
  {
    id: 'date_of_birth',
    label: 'Date of Birth',
    minWidth: 170,
    align: 'center',
    format: (value: string) => new Date(value).toLocaleDateString('en-US'),
  },
  {
    id: 'pesel',
    label: 'PESEL',
    minWidth: 170,
    align: 'center',
    format: (value: number) => value.toString(),
  },
  {
    id: 'date_of_diagnosis',
    label: 'Date of Diagnosis',
    minWidth: 170,
    align: 'center',
    format: (value: string) => new Date(value).toLocaleDateString('en-US'),
  },
];

interface Data {
  patients_id: number;
  sex: string;
  date_of_birth: string;
  pesel: number;
  date_of_diagnosis: string;
}

// Example rows data
const rows: Data[] = [
  { patients_id: 1, sex: 'Male', date_of_birth: '1980-01-01', pesel: 80010112345, date_of_diagnosis: '2020-01-01' },
  { patients_id: 2, sex: 'Female', date_of_birth: '1990-05-23', pesel: 90052312345, date_of_diagnosis: '2021-02-10' },
  // Add more rows as needed
];

export default function Patients() {
  const navigate = useNavigate();
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const handleLogOutClick = useCallback(() => {
    navigate('/login');
    }, [navigate]);

  const handleAddPatientClick = useCallback(() => {
    navigate('/addpatient');
    }, [navigate]);

  return (
    <div className="background_patients">
      <header className="header_patients">PATIENTS</header>
      <button className="log_out" onClick={handleLogOutClick}>
      <LogoutIcon />
      <span>Log out</span>
  </button>
  <button className="new_patient" onClick={handleAddPatientClick}>
    <AddPatient className="icon" />
    <span>Add patient</span>
  </button>
      <div className="table-container-wrapper">
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer className="table-container" sx={{ maxHeight: 440 }}>
           <Table stickyHeader aria-label="sticky table" className="table">
  <TableRow className="table-header">
    {columns.map((column, index) => (
      <TableCell
        key={column.id}
        align={index === 0 ? 'center' : column.align}
        style={{ minWidth: column.minWidth }}
        className={`no-bottom-border`}
      >
        {column.label}
      </TableCell>
    ))}
  </TableRow>

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
