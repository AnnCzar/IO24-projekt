import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import {ReactComponent as GoBack} from "../images/back.svg";
import './Reports.css';
import {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import {number} from "yup";

interface Column {
    id: 'date' | 'score' | 'coords' | 'comment';
    label: string;
    minWidth?: number;
    align?: 'center';
    format?: (value: any) => string;
}

const columns: readonly Column[] = [
    {id: 'date', label: 'Date', minWidth: 170},
    {id: 'score', label: 'Score', minWidth: 100, align: 'center'},
    {
        id: 'coords',
        label: 'Coords',
        minWidth: 170,
        align: 'center',
        format: (value: string) => value,
    },
    {
        id: 'comment',
        label: 'Comment',
        minWidth: 170,
        align: 'center',
        format: (value: string) => value,
    },
];

interface Data {
    date: string;
    score: number;
    coords: string;
    comment: string;
}

// Example rows data
const rows: Data[] = [
    {date: '2024-05-24', score: 85, coords: '51.5074° N, 0.1278° W', comment: 'Good progress'},
    {date: '2024-05-23', score: 90, coords: '40.7128° N, 74.0060° W', comment: 'Excellent results'},
];

export default function Reports() {

    const navigate = useNavigate();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [error, setError] = useState<string | null>(null);

    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const patientId = params.get('patientId');
    const [reports, setReports] = useState([]);

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

    return (
        <div className="background_reports">
            <header className="header_reports">REPORTS</header>
            <button className="go-back" onClick={handleGoBack}>
                <GoBack/>
                <span>Go back</span>
            </button>
            <div className="table-container-wrapper">
                <Paper sx={{width: '100%', overflow: 'hidden'}}>
                    <TableContainer className="table-container" sx={{maxHeight: 440}}>
                        <Table stickyHeader aria-label="sticky table" className="table">
                            <TableHead>
                                <TableRow className="table-header">
                                    {columns.map((column, index) => (
                                        <TableCell
                                            key={column.id}
                                            align={index === 0 ? 'center' : column.align}
                                            style={{minWidth: column.minWidth}}
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
                                    .map((row, rowIndex) => (
                                        <TableRow hover role="checkbox" tabIndex={-1} key={rowIndex}>
                                            {columns.map((column) => {
                                                const value = row[column.id as keyof Data];
                                                return (
                                                    <TableCell key={column.id} align="center"
                                                               className="no-bottom-border">
                                                        {column.format && typeof value !== 'undefined' ? column.format(value) : value}
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
