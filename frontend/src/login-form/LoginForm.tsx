import React, { useCallback, useMemo, useState } from "react";
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { Link } from 'react-router-dom';
import RoleChoice from "../role-choice/RoleChoice";
import "./LoginForm.css";

interface FormValues {
  username: string;
  password: string;
}

function LoginForm() {
  const [showRoleChoice, setShowRoleChoice] = useState(false);

  const onSubmit = useCallback((values: FormValues, formik: any) => {
    console.log(values);
  }, []);

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        username: yup.string().required("This field can't be empty"),
        password: yup
          .string()
          .required("This field can't be empty")
          .min(5, "Password has to be at least 5 characters long"),
      }),
    []
  );

  const handleRegistrationLinkClick = () => {
    setShowRoleChoice(true);
  };

  return (
    <div className="background">
      {showRoleChoice ? (
        <RoleChoice />
      ) : (
        <div>
          <header className="header">SIGN IN</header>
          <Formik
            initialValues={{ username: "", password: "" }}
            onSubmit={onSubmit}
            validationSchema={validationSchema}
            validateOnChange
            validateOnBlur
          >
            {(formik) => (
              <form
                className="login-form"
                id="signForm"
                noValidate
                onSubmit={formik.handleSubmit}
              >
                <TextField
                  id="username"
                  name="username"
                  className="login-text"
                  label="Login"
                  variant="standard"
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.username && !!formik.errors.username}
                  helperText={
                    formik.touched.username && formik.errors.username
                  }
                  InputLabelProps={{ style: { fontSize: "25px" } }}
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
                  helperText={
                    formik.touched.password && formik.errors.password
                  }
                  InputLabelProps={{ style: { fontSize: "25px" } }}
                />

                <Button
                  variant="contained"
                  type="submit"
                  disabled={!(formik.isValid && formik.dirty)}
                  className="login-button" // Poprawna klasa dla przycisku logowania
                  component={Link}
                  to={"/patients-table"}
                >
                  SIGN IN
                </Button>

                <Button
                  variant="outlined"
                  className="register-button" // Poprawna klasa dla przycisku rejestracji
                  component={Link}
                  to="/role-choice"
                >
                  Register
                </Button>
              </form>
            )}
          </Formik>
        </div>
      )}
    </div>
  );
}

export default LoginForm;
