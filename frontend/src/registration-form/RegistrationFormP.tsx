import React, { useCallback, useMemo, useState } from "react";
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./RegistrationForm.css";
import ReferencePhoto from "../reference-photo/ReferencePhoto";

interface FormValues {
  username: string;
  password: string;
  name: string;
  surname: string;
  pesel: string;
}

function RegistrationFormP() {
  const [redirect, setRedirect] = useState<boolean>(false);

  const onSubmit = (values: FormValues, formik: any) => {
    console.log(values);
    setRedirect(true);
  };

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        username: yup.string().required("This field can't be empty"),
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),

        pesel: yup.string().required("This field can't be empty").length(11, "Incorrect PESEL"),
        password: yup
          .string()
          .required("This field can't be empty")
          .min(5, "Password has to be at least 5 characters long"),
      }),
    []
  );

  if (redirect) {
    return <ReferencePhoto />;
  }

  return (
    <div className="background_register">
      <header className="header_register">SIGN UP</header>
      <Formik
        initialValues={{ username: "", password: "", name: "", surname: "", pesel: "" }}
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
              id="username"
              name="username"
              label="Login"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.username && !!formik.errors.username}
              helperText={formik.touched.username && formik.errors.username}
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

export default RegistrationFormP;
