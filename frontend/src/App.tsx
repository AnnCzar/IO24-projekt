import React from 'react';
import './App.css';
import LoginForm from './login-form/LoginForm';
import Examination from './examination/Examination';
import PatientsTable from './patients-table/PatientsTable';
import ReferencePhoto from './reference-photo/ReferencePhoto';
import RoleChoice from './role-choice/RoleChoice';
import { Route, Navigate, BrowserRouter } from 'react-router-dom';
import { Routes } from 'react-router-dom';
import RegistrationForm from "./registration-form/RegistrationForm";
import RegistrationFormP from "./registration-form/RegistrationFormP";
import RegistrationFormD from "./registration-form/RegistrationFormD";
// import ApiProvider from './api/ApiProvider';

function App() {
  return (
    <BrowserRouter>
      {/*<ApiProvider>*/}
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginForm />} />
        <Route path="/examination" element={<Examination />} />
        <Route path="/patients-table" element={<PatientsTable />} />
        <Route path="/reference-photo" element={<ReferencePhoto />} />
        <Route path="/registration" element={<RegistrationForm />} />
        <Route path="/registrationP" element={<RegistrationFormP />} />
        <Route path="/registrationD" element={<RegistrationFormD />} />
        <Route path="/role-choice" element={<RoleChoice />} />
      </Routes>
      {/*</ApiProvider>*/}
    </BrowserRouter>
  );
}

export default App;

