import React, { useCallback, useMemo } from "react";
import {
    Button,
    TextField
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./PatientsId.css";

import { ReactComponent as GoBack } from "../images/back.svg";

interface FormValues {
  id: string;
}

function PatientsId() {
  const onSubmit = useCallback(
    (values: FormValues, formik: any) => {
      console.log(values);
    },
    [],
  );

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        id: yup.string().required("This field can't be empty"),
      }),
    [],
  );

  return (
    <div className="background">
      <header className="header">ADD PATIENT</header>
      <button className="go-back">
        <GoBack />
        <span>Go back</span>
      </button>
      <Formik
        initialValues={{ id: "" }}
        onSubmit={onSubmit}
        validationSchema={validationSchema}
        validateOnChange
        validateOnBlur
      >
        {(formik) => (
          <form
            className="patients-id"
            id="signForm"
            noValidate
            onSubmit={formik.handleSubmit}
          >
            <TextField
              id="id"
              name="id"
              label="ID"
              variant="standard"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.id && !!formik.errors.id}
              helperText={formik.touched.id && formik.errors.id}
              InputLabelProps={{ style: { fontSize: '25px' } }}
              inputProps={{ style: { fontSize: '25px' } }}
              style={{ width: '20%' }}
            />

            <Button
              variant="contained"
              type="submit"
              disabled={!(formik.isValid && formik.dirty)}
            >
              DELETE
            </Button>
          </form>
        )}
      </Formik>
    </div>
  );
}

export default PatientsId;
