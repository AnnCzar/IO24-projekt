import React from "react";
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { Link } from 'react-router-dom';
import "./LoginForm.css";
import logo from "../images/Logo1.svg";

interface FormValues {
    username: string;
    password: string;
}

const LoginForm: React.FC = () => {
    const [loginError, setLoginError] = React.useState<string>("");

    const onSubmit = async (values: FormValues) => {
        try {
            const response = await fetch('http://localhost:8000/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ login: values.username, password: values.password }),
            });

            if (response.ok) {
                try {
                    const data = await response.json();
                    const role = data.role;
                    console.log('Login successful:', role);
                    if (role == 'doctor') {
                        window.location.href = "/patients";
                    } else {
                        window.location.href = "/examination";
                    }
                } catch (error) {
                    console.error('Failed to parse JSON:', error);
                    setLoginError('An error occurred while logging in.');
                }
            } else {
                const errorText = await response.text();
                console.error('Login failed:', errorText);
                if (errorText.includes('Invalid login credentials')) {
                    setLoginError('Invalid login credentials. Please try again.');
                } else {
                    setLoginError('An error occurred while logging in.');
                }
            }
        } catch (error) {
            console.error('Error during login:', error);
            setLoginError('An error occurred while logging in.');
        }
    };

    const validationSchema = yup.object().shape({
        username: yup.string().required("Username is required"),
        password: yup.string().required("Password is required")
                    .min(6, "Password must be at least 6 characters long"),
    });

    return (
        <div className="background_login">
            <div className="login_container">
                <header className="header_login">SIGN IN</header>

                <Formik
                    initialValues={{ username: "", password: "" }}
                    onSubmit={onSubmit}
                    validationSchema={validationSchema}
                    validateOnChange
                    validateOnBlur
                >
                    {(formik) => (
                        <form
                            className="login_form"
                            id="signForm"
                            noValidate
                            onSubmit={formik.handleSubmit}
                        >
                            <TextField
                                id="username"
                                name="username"
                                className="login_text"
                                label="Login"
                                variant="standard"
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                error={formik.touched.username && !!formik.errors.username}
                                helperText={formik.touched.username && formik.errors.username}
                                InputLabelProps={{ style: { fontSize: "1.5rem" } }}
                                fullWidth
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
                                InputLabelProps={{ style: { fontSize: "1.5rem" } }}
                                fullWidth
                            />

                            <Button
                                variant="contained"
                                type="submit"
                                disabled={!(formik.isValid && formik.dirty)}
                                fullWidth
                                style={{ marginTop: '1rem' }}
                            >
                                SIGN IN
                            </Button>

                            <Button
                                variant="outlined"
                                component={Link}
                                to="/role-choice"
                                fullWidth
                                style={{ marginTop: '1rem' }}
                            >
                                Register
                            </Button>

                            {loginError && (
                                <div className="login_error">{loginError}</div>
                            )}
                        </form>
                    )}
                </Formik>

                <img src={logo} alt="Logo" className="logo_bottom" />
            </div>
        </div>
    );
}

export default LoginForm;
