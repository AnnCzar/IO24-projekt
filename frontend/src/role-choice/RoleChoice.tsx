import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, FormControl, FormControlLabel, Radio, RadioGroup } from "@mui/material";
import "./RoleChoice.css";

function RoleChoice() {
    const [selectedRole, setSelectedRole] = useState<string | null>(null);
    const navigate = useNavigate();

    const handleRoleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedRole(event.target.value);
    };

    const handleConfirmClick = () => {
        console.log("Role confirmed:", selectedRole);
        if (selectedRole === "doctor") {
            navigate("/registrationD");
        } else if (selectedRole === "patient") {
            navigate("/registrationP");
        }
    };

    return (
        <div className="background_role">
            <header className="header_role">CHOOSE YOUR ROLE</header>
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
