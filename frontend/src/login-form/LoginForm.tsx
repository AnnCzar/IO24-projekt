import React, { useCallback, useMemo, useState } from "react";
<<<<<<< HEAD
import { Button, Link, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./LoginForm.css";
import RoleChoice from "../role-choice/RoleChoice";
=======
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { Link } from 'react-router-dom';
import RoleChoice from "../role-choice/RoleChoice";
import "./LoginForm.css";
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74

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

<<<<<<< HEAD
  const handleRegistrationLinkClick = () => {
    setShowRoleChoice(true);
  };

  return (
    <div className="background">
=======
  // const handleRegistrationLinkClick = () => {
  //   setShowRoleChoice(true);
  // };

  return (
    <div className="background_login">
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
      {showRoleChoice ? (
        <RoleChoice />
      ) : (
        <div>
<<<<<<< HEAD
          <header className="header">SIGN IN</header>
=======
          <header className="header_login">SIGN IN</header>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
          <Formik
            initialValues={{ username: "", password: "" }}
            onSubmit={onSubmit}
            validationSchema={validationSchema}
            validateOnChange
            validateOnBlur
          >
            {(formik) => (
              <form
<<<<<<< HEAD
                className="login-form"
=======
                className="login_form"
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
                id="signForm"
                noValidate
                onSubmit={formik.handleSubmit}
              >
                <TextField
                  id="username"
                  name="username"
<<<<<<< HEAD
=======
                  className="login_text"
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
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
<<<<<<< HEAD
=======
                  component={Link}
                  to={"/patients"}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
                >
                  SIGN IN
                </Button>

<<<<<<< HEAD
                <Link
                  href="#"
                  style={{ fontSize: "25px" }}
                  onClick={handleRegistrationLinkClick}
                >
                  Register
                </Link>
=======
                <Button
                  variant="outlined"
                  component={Link}
                  to="/role-choice"
                >
                  Register
                </Button>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
              </form>
            )}
          </Formik>
        </div>
      )}
    </div>
  );
}

export default LoginForm;
