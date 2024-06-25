import React, {useMemo, useState} from "react";
import {Alert, Button, Dialog, DialogActions, DialogContent, DialogContentText, TextField} from "@mui/material";
import { Formik } from "formik";
import { useNavigate } from "react-router-dom";
import * as yup from "yup";
import "./RegistrationForm.css";
import logo from "../images/Logo3.svg";

interface FormValues {
    name: string;
    surname: string;
    email: string;
    pesel: string;
    login: string;
    password: string;
    pwz_pwzf: string;
}

function RegistrationFormD() {
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [open, setOpen] = useState(false); // Initially set to false

  const onSubmit = async (values: FormValues) => {
    try {
        const response = await fetch('http://localhost:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(values), // directly use values object
        });

        if (response.ok) {
            console.log('Registration successful');
            setSuccessMessage("User has been successfully registered! Please log in to app now.");
            setOpen(true); // Show the dialog box
        } else {
            const errorText = await response.text();
            setErrorMessage("Failed to register user. Please try again.");
            console.error('Registration failed:', errorText);
        }
    } catch (error) {
        setErrorMessage("An error occurred. Please try again.");
        console.error('Error during registration:', error);
    }
  };

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        login: yup.string().required("This field can't be empty"),
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),
        pesel: yup.string().required("This field can't be empty").length(11, "Incorrect PESEL"),
        pwz_pwzf: yup.string().required("This field can't be empty").length(7, "Incorrect Medical license"),
        email: yup.string().required("This field can't be empty")
                .email("Invalid email address"),
        password: yup
          .string()
          .required("This field can't be empty")
          .min(5, "Password has to be at least 5 characters long"),
      }),
    [],
  );

  const handleClose = () => {
    setOpen(false);
    navigate('/login');
  };

  return (
    <div className="background_register">
      <header className="header_register">SIGN UP</header>
        <img src={logo} alt="Logo" className="logo_bottom" />
        {successMessage && <Alert severity="success" style={{
              position: 'fixed',
              bottom: 0,
              width: '100%',
              textAlign: 'center',
              zIndex: 9999
          }}>{successMessage}</Alert>}
           {errorMessage && <Alert severity="error" style={{
        position: 'fixed',
        bottom: 0,
        width: '100%',
        textAlign: 'center',
        zIndex: 9999
      }}>{errorMessage}</Alert>}
      <Formik
        initialValues={{ name: "", surname: "", email: "", pesel: "", login: "", password: "", pwz_pwzf:"" }}
        onSubmit={onSubmit}
        validationSchema={validationSchema}
        validateOnChange
        validateOnBlur
      >
        {(formik) => (
          <form
            className="registration-form"
            id="signForm"
            noValidate
            onSubmit={formik.handleSubmit}
          >
            <TextField
              id="name"
              name="name"
              label="Name"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.name && !!formik.errors.name}
              helperText={formik.touched.name && formik.errors.name}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="surname"
              name="surname"
              label="Surname"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.surname && !!formik.errors.surname}
              helperText={formik.touched.surname && formik.errors.surname}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="email"
              name="email"
              label="Email"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.email && !!formik.errors.email}
              helperText={formik.touched.email && formik.errors.email}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="login"
              name="login"
              label="Login"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.login && !!formik.errors.login}
              helperText={formik.touched.login && formik.errors.login}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="password"
              name="password"
              label="Password"
              variant="standard"
              type="password"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.password && !!formik.errors.password}
              helperText={formik.touched.password && formik.errors.password}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="pesel"
              name="pesel"
              label="PESEL"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.pesel && !!formik.errors.pesel}
              helperText={formik.touched.pesel && formik.errors.pesel}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <TextField
              id="pwz"
              name="pwz_pwzf"
              label="Medical license"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.pwz_pwzf && !!formik.errors.pwz_pwzf}
              helperText={formik.touched.pwz_pwzf && formik.errors.pwz_pwzf}
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <Button
              variant="contained"
              type="submit"
              disabled={!(formik.isValid && formik.dirty)}
            >
              CONFIRM
            </Button>
          </form>
        )}
      </Formik>
      <Dialog open={open} onClose={handleClose}>
        <DialogContent>
          <DialogContentText>
            User has been successfully registered! Please log in to app now.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default RegistrationFormD;
