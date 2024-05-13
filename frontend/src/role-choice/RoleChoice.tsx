import React, { useState } from "react";
import { Button, FormControl, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import "./RoleChoice.css";
import RegistrationFormD from "../registration-form/RegistrationFormD";
import RegistrationFormP from "../registration-form/RegistrationFormP";

function RoleChoice() {
    const [selectedRole, setSelectedRole] = useState<string | null>(null);
    const [redirect, setRedirect] = useState<boolean>(false);

    const handleRoleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedRole(event.target.value);
    };

    const handleConfirmClick = () => {
        console.log("Role confirmed:", selectedRole);
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
