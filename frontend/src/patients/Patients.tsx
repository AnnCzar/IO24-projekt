
import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableHead from '@mui/material/TableHead';
import { ReactComponent as LogoutIcon } from "../images/logout.svg";
import { ReactComponent as AddPatient } from "../images/add_patient.svg";
import './Patients.css';
import { useNavigate } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";

interface Column {
  id: 'patients_id' | 'sex' | 'date_of_birth' | 'pesel' | 'date_of_diagnosis';
  label: string;
  minWidth?: number;
  align?: 'center';
  format?: (value: any) => string;
}

interface Data {
  patients_id: number;
  sex: string;
  date_of_birth: string;
  pesel: number;
  date_of_diagnosis: string;
}

const columns: readonly Column[] = [
  { id: 'patients_id', label: 'Patients ID', minWidth: 170 },
  { id: 'sex', label: 'Sex', minWidth: 100, align: "center" },
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

const Patients: React.FC = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [rows, setRows] = useState<Data[]>([]); // Explicitly define the type as Data[]
  const [error, setError] = useState<string | null>(null);

  const fetchPatients = async () => {
  try {
    const response = await fetch('http://localhost:8000/patients/by-doctor/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });
    console.log(response)

    if (!response.ok) {
      throw new Error('Failed to fetch patients');
    }

    const data: Data[] = await response.json();
    setRows(data);
  } catch (error:any) {
    setError(error.message);
  }
};

  useEffect(() => {
    fetchPatients();
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

 const handleLogOutClick = useCallback(async () => {

    try {
      const response = await fetch('http://localhost:8000/logout/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

      navigate('/login');
      console.log(response)
    } catch (error) {
      console.error('Error logging out:', error);
    }
  }, [navigate]);

  const handleAddPatientClick = useCallback(() => {
    navigate('/addpatient');
  }, [navigate]);

  return (
    <div className="background_patients">
      <header className="header_patients">PATIENTS</header>
      {error && <p className="error">{error}</p>}
      <button className="log_out" onClick={handleLogOutClick}>
        <LogoutIcon />
        <span>Log out</span>
      </button>
      <button className="new_patient" onClick={() => navigate('/addpatient')}>
        <AddPatient className="icon" />
        <span>Add patient</span>
      </button>
      <div className="table-container-wrapper">
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
          <TableContainer sx={{ maxHeight: 440 }}>
            <Table stickyHeader aria-label="sticky table">
              <TableHead>
                <TableRow>
                  {columns.map((column) => (
                    <TableCell key={column.id} align={column.align} style={{ minWidth: column.minWidth }}>
                      {column.label}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => (
                  <TableRow hover tabIndex={-1} key={row.patients_id}>
                    {columns.map((column) => (
                      <TableCell key={column.id} align={column.align}>
                        {column.format && typeof row[column.id] === 'string' ? column.format(row[column.id]) : row[column.id]}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
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
};

export default Patients;