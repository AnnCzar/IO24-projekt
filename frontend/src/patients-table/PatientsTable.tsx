import React, { useState } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Paper } from "@mui/material";
import "./PatientsTable.css"

interface Patient {
  id: number;
  sex: string;
  date_of_birth: string;
  PESEL: string;
  date_of_diagnosis: string;
}

const rows: Patient[] = [
  { id: 1, sex: "Male", date_of_birth: "1990-01-01", PESEL: "12345678901", date_of_diagnosis: "2020-01-01" },
    { id: 2, sex: "Male", date_of_birth: "1990-01-01", PESEL: "12345678901", date_of_diagnosis: "2020-01-01" },
  // Dodaj więcej danych w razie potrzeby
];

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'sex', headerName: 'Sex', width: 150 },
  { field: 'date_of_birth', headerName: 'Date of Birth', width: 150 },
  { field: 'PESEL', headerName: 'PESEL', width: 150 },
  { field: 'date_of_diagnosis', headerName: 'Date of Diagnosis', width: 150 },
];

function PatientsTable() {
  const [paginationModel, setPaginationModel] = useState({ page: 0, pageSize: 5 });

  return (
      <div className="background_patientstab">
        <header className="header_patientstab">PATIENTS</header>
        <div className={"container"}>
          <Paper className={"table-wrapper"}>
            <DataGrid
                rows={rows}
                columns={columns}
                paginationModel={paginationModel}
                onPaginationModelChange={setPaginationModel}
                checkboxSelection
                disableRowSelectionOnClick // Poprawiona właściwość
                sortingOrder={['asc', 'desc']}
            />

          </Paper>
        </div>
      </div>
  );
}

export default PatientsTable;
