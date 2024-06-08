import React, { useCallback, useMemo } from "react";
<<<<<<< HEAD
import {Button, Link, TextField} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./RegistrationForm.css";

interface FormValues {
  username: string;
  password: string;
  name: string;
  surname: string;
  pesel: string;
  pwz: string;
}

function RegistrationFormD() {
  const onSubmit = useCallback(
    (values: FormValues, formik: any) => {
      console.log(values);
    },
    [],
=======
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import { useNavigate } from "react-router-dom";
import * as yup from "yup";
import "./RegistrationForm.css";

// interface FormValues {
//   username: string;
//   password: string;
//   name: string;
//   surname: string;
//   pesel: string;
//   pwz: string;
// }

function RegistrationFormD() {
  const navigate = useNavigate();
  const onSubmit = useCallback(
     (values: { username: string, password: string, name: string, surname: string, pesel: string, pwz: string }, formik: any) => {
      // apiClient.login(values).then((response) => {
      //   console.log(response);
      //   if (response.success) {
      navigate('/patients');
      //   } else {
      //     formik.setFieldError('username', 'Invalid username or password');
      //   }
      // });
    },
    [navigate],
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
  );

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        username: yup.string().required("This field can't be empty"),
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),

        pesel: yup.string().required("This field can't be empty")
            .length(11, "Incorrect PESEL"),
        pwz: yup.string().required("This field can't be empty")
            .length(7, "Incorrect Medical license"),
        password: yup
          .string()
          .required("This field can't be empty")
          .min(5, "Password has to be at least 5 characters long"),

      }),
    [],
  );

  return (
<<<<<<< HEAD
    <div className="background">
        <header className="header">SIGN UP</header>
=======
    <div className="background_register">
        <header className="header_register">SIGN UP</header>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
      <Formik
        initialValues={{ username: "", password: "", name: "", surname: "", pesel: "", pwz: ""}}
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
<<<<<<< HEAD
              <TextField
=======
            <TextField
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
              id="name"
              name="name"
              label="Name"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.name && !!formik.errors.name}
              helperText={formik.touched.name && formik.errors.name}
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}

            />
               <TextField
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}

            />
           <TextField
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
              id="surname"
              name="surname"
              label="Surname"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.surname && !!formik.errors.surname}
              helperText={formik.touched.surname && formik.errors.surname}
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
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
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
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
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
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
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
            />

            <TextField
              id="pwz"
              name="pwz"
              label="Medical license"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.pwz && !!formik.errors.pwz}
              helperText={formik.touched.pwz && formik.errors.pwz}
<<<<<<< HEAD
              InputLabelProps={{ style: { fontSize: '30px' } }}
              InputProps={{ style: { fontSize: '30px' } }}
=======
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              InputProps={{ style: { fontSize: '1.25rem' } }}
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
            />

            <Button
              variant="contained"
              type="submit"
              disabled={!(formik.isValid && formik.dirty)}
            >
              CONFIRM
            </Button>
<<<<<<< HEAD

=======
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
          </form>
        )}
      </Formik>
    </div>
  );
}

<<<<<<< HEAD
export default RegistrationFormD;
=======
export default RegistrationFormD;
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
