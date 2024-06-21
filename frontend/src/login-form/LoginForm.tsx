import React from "react";
import { Button, TextField } from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { Link } from 'react-router-dom';
import "./LoginForm.css";
import logo from "../images/Logo1.svg";
import { useNavigate } from 'react-router-dom';

interface FormValues {
    username: string;
    password: string;
}

const LoginForm: React.FC = () => {
    const [loginError, setLoginError] = React.useState<string>("");
    const navigate = useNavigate();

    const onSubmit = async (values: FormValues) => {
        try {
            const response = await fetch('http://localhost:8000/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ login: values.username, password: values.password }),
            });

            if (response.ok) {
                const data = await response.json();
                const role = data.role;
                console.log('Login successful:', role);
                if (role === 'doctor') {
                    navigate('/patients');
                } else if (role === 'patient') {
                    navigate('/examination');
                } else if (role === 'admin') {
                    navigate('/allpatients');
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
            <header className="header_login">SIGN IN</header>
            <div className="login_container">
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
                                 style={{ marginBottom: '1rem' }}
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
                <img src={logo} alt="Logo" className="logo_bottom_log" />
            </div>
        </div>
    );
}

export default LoginForm;
