<<<<<<< HEAD
import React from "react";
import "./App.css";
import LoginForm from "./login-form/LoginForm";
function App() {
  return (
    <>
      <LoginForm></LoginForm>
    </>
=======
import React from 'react';
import './App.css';
import LoginForm from './login-form/LoginForm';
import Examination from './examination/Examination';
import ReferencePhoto from './reference-photo/ReferencePhoto';
import RoleChoice from './role-choice/RoleChoice';
import { Route, Navigate, BrowserRouter } from 'react-router-dom';
import { Routes } from 'react-router-dom';
import RegistrationFormP from "./registration-form/RegistrationFormP";
import RegistrationFormD from "./registration-form/RegistrationFormD";
import AddPatient from "./add-patient/AddPatient";
import AllPatients from "./all-patients/AllPatients";
import PatientsId from "./patients-id/PatientsId";
import Patients from "./patients/Patients";
import Reports from "./reports/Reports";
// import ApiProvider from './api/ApiProvider';

function App() {
  return (
    <BrowserRouter>
      {/*<ApiProvider>*/}
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/examination" element={<Examination />} />
        <Route path="/reference-photo" element={<ReferencePhoto />} />
        <Route path="/registrationP" element={<RegistrationFormP />} />
        <Route path="/registrationD" element={<RegistrationFormD />} />
        <Route path="/addpatient" element={<AddPatient />} />
        <Route path="/role-choice" element={<RoleChoice />} />
        <Route path="/allpatients" element={<AllPatients />} />
        <Route path="/patientsid" element={<PatientsId />} />
        <Route path="/patients" element={<Patients />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
      {/*</ApiProvider>*/}
    </BrowserRouter>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
  );
}

export default App;
<<<<<<< HEAD
=======

>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
