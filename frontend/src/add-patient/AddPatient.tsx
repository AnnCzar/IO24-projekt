import React, { useCallback, useMemo } from "react";
import {
    Button,
    FormControl,
    FormControlLabel,
    FormLabel,
    Grid,
    Link,
    Radio,
    RadioGroup,
    TextField
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
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
  const onSubmit = useCallback(
    (values: FormValues, formik: any) => {
      console.log(values);
    },
    [],
  );

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        email: yup.string().required("This field can't be empty"),
        name: yup.string().required("This field can't be empty"),
        surname: yup.string().required("This field can't be empty"),

        pesel: yup.string().required("This field can't be empty").length(11, "Incorrect PESEL"),
        date_of_birth: yup.string().required("This field can't be empty").length(7, "Incorrect Medical license"),
        sex: yup.string().required("This field can't be empty"),
      }),
    [],
  );

  return (
    <div className="background">
      <header className="header">ADD PATIENT</header>
        <button className="go-back" >
        <GoBack />
        <span>Go back</span>
      </button>
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              style={{ width: '20%' }}
              inputProps={{ style: { fontSize: '25px' } }}
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              style={{ width: '20%' }}
              inputProps={{ style: { fontSize: '25px' } }}
            />
           <FormControl component="fieldset" style={{ textAlign: 'left', width: '20%' }}>
  <FormLabel component="legend" style={{ fontSize: '25px', marginLeft: 0, marginTop: '10px' }}>Sex</FormLabel>
  <Grid container direction="row" alignItems="center" spacing={4}>
    <Grid item xs={12}>
      <RadioGroup row>
        <FormControlLabel value="female" control={<Radio />}  label={<span style={{ fontSize: '25px' }}>F</span>} style={{ marginTop: '10px' }} />
        <FormControlLabel value="male" control={<Radio />} label={<span style={{ fontSize: '25px' }}>M</span>} style={{ marginTop: '10px' }} />
      </RadioGroup>
    </Grid>
  </Grid>
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              inputProps={{ style: { fontSize: '25px' } }}
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              inputProps={{ style: { fontSize: '25px' } }}
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              inputProps={{ style: { fontSize: '25px' } }}
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
              InputLabelProps={{ style: { fontSize: '25px' } }}
              inputProps={{ style: { fontSize: '25px' } }}
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
