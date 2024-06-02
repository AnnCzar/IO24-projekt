import React, { useCallback, useMemo, useState } from "react";
import { Alert, Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import "./PatientsId.css";
import { ReactComponent as GoBack } from "../images/back.svg";
import {useNavigate} from "react-router-dom";

interface FormValues {
  id: string;
}

function PatientsId() {
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const onSubmit = useCallback(
    (values: FormValues, formik: any) => {
      console.log(values);
      setSuccessMessage("User has been successfully deleted!");
    },
    [],
  );

  const handleGoBack = () => {
    navigate(-1);
  };

  const validationSchema = useMemo(
    () =>
      yup.object().shape({
        id: yup.string().required("This field can't be empty"),
      }),
    [],
  );

  return (
    <div className="background_id">
      <header className="header_id">DELETE PATIENT</header>
      <button className="goback_id" onClick={handleGoBack}>
        <GoBack />
        <span>Go back</span>
      </button>
        {successMessage && <Alert severity="success" style={{ position: 'fixed', bottom: 0, width: '100%', textAlign: 'center', zIndex: 9999 }}>{successMessage}</Alert>}
      <Formik
        initialValues={{ id: "" }}
        onSubmit={onSubmit}
        validationSchema={validationSchema}
        validateOnChange
        validateOnBlur
      >
        {(formik) => (
          <form
            className="patients_id"
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
              InputLabelProps={{ style: { fontSize: '1.75rem' } }}
              inputProps={{ style: { fontSize: '1.75rem' } }}
              style={{ width: '15%' }}
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
