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

  const handleGoBack = () => {
    navigate(-1);
  };

  const onSubmit = useCallback(
    (values: FormValues, formik: any) => {
      console.log(values);
      setSuccessMessage("User has been successfully added!");
      formik.resetForm();
    },
    [],
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
      }),
    [],
  );

  return (
    <div className="background">
      <header className="header">ADD PATIENT</header>
      <button className="go-back" onClick={handleGoBack}>
        <GoBack />
        <span>Go back</span>
      </button>
      {successMessage && <Alert severity="success" style={{ position: 'fixed', bottom: 0, width: '100%', textAlign: 'center', zIndex: 9999 }}>{successMessage}</Alert>}
      <Formik
        initialValues={{ name: "", surname: "", email: "", date_of_birth: "", pesel: "", date_of_diagnosis: "", sex: "" }}
        onSubmit={onSubmit}
        validationSchema={validationSchema}
        validateOnChange
        validateOnBlur
      >
        {(formik) => (
          <form
            className="add-patient"
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
              style={{ width: '20%' }}
              inputProps={{ style: { fontSize: '1.25rem' } }}
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
              style={{ width: '20%' }}
              inputProps={{ style: { fontSize: '1.25rem' } }}
            />
            <FormControl component="fieldset" style={{ textAlign: 'left', width: '20%' }}>
              <FormLabel component="legend" style={{ fontSize: '1.25rem', marginLeft: 0, marginTop: '0.625rem' }}>Sex</FormLabel>
              <Grid container direction="row" alignItems="center" spacing={4}>
                <Grid item xs={12}>
                  <RadioGroup
                    row
                    name="sex"
                    value={formik.values.sex}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                  >
                    <FormControlLabel value="female" control={<Radio />} label={<span style={{ fontSize: '1.25rem' }}>F</span>} style={{ marginTop: '0.625rem' }} />
                    <FormControlLabel value="male" control={<Radio />} label={<span style={{ fontSize: '1.25rem' }}>M</span>} style={{ marginTop: '0.625rem' }} />
                  </RadioGroup>
                </Grid>
              </Grid>
              {formik.touched.sex && formik.errors.sex && <div style={{ color: 'red', fontSize: '0.875rem' }}>{formik.errors.sex}</div>}
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
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              inputProps={{ style: { fontSize: '1.25rem' } }}
              style={{ width: '20%' }}
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
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              inputProps={{ style: { fontSize: '1.25rem' } }}
              style={{ width: '20%' }}
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
              inputProps={{ style: { fontSize: '1.25rem' } }}
              style={{ width: '20%' }}
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
              InputLabelProps={{ style: { fontSize: '1.25rem' } }}
              inputProps={{ style: { fontSize: '1.25rem' } }}
              style={{ width: '20%' }}
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

export default AddPatient;
