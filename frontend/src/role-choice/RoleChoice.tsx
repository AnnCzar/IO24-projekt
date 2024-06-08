import React, { useState } from "react";
<<<<<<< HEAD
import { Button, FormControl, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import "./RoleChoice.css";
import RegistrationFormD from "../registration-form/RegistrationFormD";
import RegistrationFormP from "../registration-form/RegistrationFormP";

function RoleChoice() {
    const [selectedRole, setSelectedRole] = useState<string | null>(null);
    const [redirect, setRedirect] = useState<boolean>(false);
=======
import { useNavigate } from "react-router-dom";
import { Button, FormControl, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import "./RoleChoice.css";

function RoleChoice() {
    const [selectedRole, setSelectedRole] = useState<string | null>(null);
    const navigate = useNavigate();
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74

    const handleRoleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedRole(event.target.value);
    };

    const handleConfirmClick = () => {
        console.log("Role confirmed:", selectedRole);
<<<<<<< HEAD
        setRedirect(true);
    };

    if (redirect) {
        if (selectedRole === "doctor") {
            return <RegistrationFormD />;
        } else if (selectedRole === "patient") {
            return <RegistrationFormP />;
        }
    }

    return (
        <div className="background">
            <header className="header">CHOOSE YOUR ROLE</header>
=======
        if (selectedRole === "doctor") {
            navigate("/registrationD");
        } else if (selectedRole === "patient") {
            navigate("/registrationP");
        }
    };

    return (
        <div className="background_role">
            <header className="header_role">CHOOSE YOUR ROLE</header>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
            <div className="role-choice">
                <FormControl>
                    <RadioGroup aria-label="role" name="role" value={selectedRole} onChange={handleRoleChange}>
                        <FormControlLabel value="doctor" control={<Radio />} label="DOCTOR" />
                        <FormControlLabel value="patient" control={<Radio />} label="PATIENT" />
                    </RadioGroup>
                </FormControl>
                <Button variant="contained" type="submit" onClick={handleConfirmClick} disabled={!selectedRole}>
                    CONFIRM
                </Button>
            </div>
        </div>
    );
}

export default RoleChoice;
