import React, { useCallback, useMemo, useState } from "react";
import {
    Button,
    FormControl,
    FormControlLabel,
    FormLabel,
    Grid,
    Radio,
    RadioGroup,
    TextField,
    Alert
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { useNavigate } from 'react-router-dom';
import "./AddPatient.css";

import { ReactComponent as GoBack } from "../images/back.svg";
import axios from "axios";
import logo from "../images/Logo3.svg";

interface FormValues {
  name: string;
  surname: string;
  email: string;
  date_of_birth: string;
  pesel: string;
  date_of_diagnosis: string;
  sex: string;
}

function AddPatient() {
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleGoBack = () => {
    navigate(-1);
  };


    const onSubmit = useCallback(
  async (values: FormValues, formik: any) => {
    console.log(values);

    try {
      const response = await fetch('http://localhost:8000/addPatient/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          name: values.name,
          surname: values.surname,
          email: values.email,
          pesel: values.pesel,
          date_of_birth: values.date_of_birth,
          date_of_diagnosis: values.date_of_diagnosis || null,
          sex: values.sex
        }),
      });

      console.log(response.url);
      if (response.status === 201) {
        setSuccessMessage("User has been successfully added!");
        formik.resetForm();
      } else {
        setErrorMessage("Failed to add user. Please try again.");
      }
    } catch (error) {
      setErrorMessage("An error occurred. Please try again.");
    }
  },
  []
);


  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        email: yup.string().required("This field can't be empty").email("Invalid email format"),
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),
        pesel: yup.string().required("This field can't be empty").length(11, "Incorrect PESEL"),
        date_of_birth: yup.string().required("This field can't be empty"),
        sex: yup.string().required("This field can't be empty"),
        date_of_diagnosis: yup.string().nullable(),
      }),
    [],
  );

  const handleBackToPatients = () => {
    navigate("/patients");
  };

  return (
      <div className="background_add_patient">
          <header className="header_add_patient">ADD PATIENT</header>
          <img src={logo} alt="Logo" className="logo_bottom" />
          <button className="goback_add_patient" onClick={handleGoBack}>
              <GoBack/>
              <span>Go back</span>
          </button>
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
                  initialValues={{
                      name: "",
                      surname: "",
                      email: "",
                      date_of_birth: "",
                      pesel: "",
                      date_of_diagnosis: "",
                      sex: ""
                  }}
                  onSubmit={onSubmit}
                  validationSchema={validationSchema}
                  validateOnChange
                  validateOnBlur
              >
                  {(formik) => (
                      <form
                          className="add_patient"
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
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
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
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
                          />
                          <FormControl component="fieldset" style={{textAlign: 'left', width: '20%'}}>
                              <FormLabel component="legend" style={{
                                  fontSize: '1.25rem',
                                  marginLeft: 0,
                                  marginTop: '0.625rem'
                              }}>Sex</FormLabel>
                              <Grid container direction="row" alignItems="center" spacing={4}>
                                  <Grid item xs={12}>
                                      <RadioGroup
                                          row
                                          name="sex"
                                          value={formik.values.sex}
                                          onChange={formik.handleChange}
                                          onBlur={formik.handleBlur}
                                      >
                                          <FormControlLabel value="FEMALE" control={<Radio/>}
                                                            label={<span style={{fontSize: '1.25rem'}}>F</span>}
                                                            style={{marginTop: '0.625rem'}}/>
                                          <FormControlLabel value="MALE" control={<Radio/>}
                                                            label={<span style={{fontSize: '1.25rem'}}>M</span>}
                                                            style={{marginTop: '0.625rem'}}/>
                                      </RadioGroup>
                                  </Grid>
                              </Grid>
                              {formik.touched.sex && formik.errors.sex &&
                                  <div style={{color: 'red', fontSize: '0.875rem'}}>{formik.errors.sex}</div>}
                          </FormControl>
                          <TextField
                              id="email"
                              name="email"
                              label="Email"
                              variant="standard"
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              error={formik.touched.email && !!formik.errors.email}
                              helperText={formik.touched.email && formik.errors.email}
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
                          />
                          <TextField
                              id="date_of_birth"
                              name="date_of_birth"
                              label="Date of Birth"
                              variant="standard"
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              error={formik.touched.date_of_birth && !!formik.errors.date_of_birth}
                              helperText={formik.touched.date_of_birth && formik.errors.date_of_birth}
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
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
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
                          />
                          <TextField
                              id="date_of_diagnosis"
                              name="date_of_diagnosis"
                              label="Date of Diagnosis (optional)"
                              variant="standard"
                              onChange={formik.handleChange}
                              onBlur={formik.handleBlur}
                              error={formik.touched.date_of_diagnosis && !!formik.errors.date_of_diagnosis}
                              helperText={formik.touched.date_of_diagnosis && formik.errors.date_of_diagnosis}
                              InputLabelProps={{style: {fontSize: '1.25rem'}}}
                              inputProps={{style: {fontSize: '1.25rem'}}}
                              style={{width: '20%'}}
                          />
                          <Button
                              className="button_add_patient"
                              variant="contained"
                              type="submit"
                              disabled={!(formik.isValid && formik.dirty)}
                          >
                              CONFIRM
                          </Button>

                          <Button
                variant="outlined"
                onClick={handleBackToPatients}
                style={{ fontSize: '1rem' }}
              >
                Back to patients list
              </Button>
                      </form>
                  )}
              </Formik>
      </div>
  );
}

export default AddPatient;