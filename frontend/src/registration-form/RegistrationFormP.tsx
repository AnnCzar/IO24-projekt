import React, { useMemo } from "react";
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./RegistrationForm.css";
import { useNavigate } from "react-router-dom";
import logo from "../images/Logo3.svg";

interface FormValues {
  name: string;
  surname: string;
  email: string;
  pesel: string;
  login: string;
  password: string;
}

function RegistrationFormP() {
  const navigate = useNavigate();

  const onSubmit = async (values: FormValues) => {
    try {
      const response = await fetch("http://localhost:8000/registerPatient/", {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(values),
      });

      if (response.ok) {
        console.log("Registration successful");
        navigate("/reference-photo");
      } else {
        const errorText = await response.text();
        console.error("Registration failed:", errorText);
      }
    } catch (error) {
      console.error("Error during registration:", error);
    }
  };

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),
        email: yup.string().required("This field can't be empty").email("Invalid email address"),
        pesel: yup.string().required("This field can't be empty").length(11, "Incorrect PESEL"),
        login: yup.string().required("This field can't be empty"),
        password: yup
          .string()
          .required("This field can't be empty")
          .min(5, "Password has to be at least 5 characters long"),
      }),
    []
  );

  return (
    <div className="background_register">
      <header className="header_register">SIGN UP</header>
        <img src={logo} alt="Logo" className="logo_bottom" />
      <Formik
        initialValues={{ name: "", surname: "", email: "", pesel: "", login: "", password: "" }}
        onSubmit={onSubmit}
        validationSchema={validationSchema}
        validateOnChange
        validateOnBlur
      >
        {(formik) => (
          <form className="registration-form" id="signForm" noValidate onSubmit={formik.handleSubmit}>
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
    </div>
  );
}

export default RegistrationFormP;
