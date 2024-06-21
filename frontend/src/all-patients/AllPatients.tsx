import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  id: 'id' | 'name' | 'surname' | 'sex' | 'email' | 'date_of_last_exam';
  label: string;
  minWidth?: number;
  align?: 'center';
  format?: (value: any) => string;
}

const columns: readonly Column[] = [
  { id: 'id', label: 'Patients ID', minWidth: 170 },
  { id: 'name', label: 'Name', minWidth: 100, align: 'center' },
  { id: 'surname', label: 'Surname', minWidth: 100, align: 'center' },
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
    format: (value: string | null | undefined) => value ? new Date(value).toLocaleDateString('en-US') : '-',
  },
];

interface Data {
  id: number;
  name: string;
  surname: string;
  sex: string;
  email: string;
  date_of_last_exam: string;
}

export default function AllPatients() {
  const navigate = useNavigate();
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [patients, setPatients] = useState<Data[]>([]); // Użyj Data[] jako typu generycznego dla useState

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await fetch('http://localhost:8000/patients/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch patients');
      }
      const data = await response.json();
      const formattedPatients = data.map((patient: any) => ({
        id: Number(patient.id), // Konwersja na number
        name: patient.name,
        surname: patient.surname,
        sex: patient.sex,
        email: patient.email,
        date_of_last_exam: patient.date_of_last_exam,
      }));
      setPatients(formattedPatients);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  const handleDeletePatient = useCallback(() => {
    navigate('/patientsid');
  }, [navigate]);

  return (
    <div className="background_all_patients">
      <header className="header_all_patients">ALL PATIENTS</header>
      <button className="goback_all_patients" onClick={handleGoBack}>
        <GoBack />
        <span>Go back</span>
      </button>
      <button className="delete-patient" onClick={handleDeletePatient}>
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
                      style={{ minWidth: `${column.minWidth}px` }}
                      className={`no-bottom-border`}
                    >
                      <b>{column.label}</b>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>

              <TableBody>
                {patients
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((patient) => (
                    <TableRow key={patient.id} hover role="checkbox" tabIndex={-1}>
                      {columns.map((column) => {
                        const value = patient[column.id as keyof Data];
                        return (
                          <TableCell key={column.id} align={column.align} className="no-bottom-border">
                            {column.format ? column.format(value) : value}
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[10, 25, 100]}
            component="div"
            count={patients.length}
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
