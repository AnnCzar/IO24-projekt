import React, {useCallback, useRef, useState} from "react";
import Webcam from "react-webcam";
import WebcamRef from "react-webcam";
import { Button } from "@mui/material";
import "./Examination.css";
import { ReactComponent as LogoutIcon } from "../images/logout.svg";
import { ReactComponent as ReportsIcon } from "../images/reports.svg"
import {useNavigate} from "react-router-dom";

function Examination() {
    const navigate = useNavigate();
    const webRef = useRef<WebcamRef>(null);
    const [redirect, setRedirect] = useState<boolean>(false);

    const showImage = async () => {
        if (webRef.current) {
            const screenshot = await webRef.current.getScreenshot();
            console.log(screenshot);
        }
    };

    const handleLogOutClick = useCallback(() => {
        navigate('/login');
    }, [navigate]);

    const handleReportsClick = useCallback(() => {
        navigate('/reports');
    }, [navigate]);

    return (
   <div className="background_ex">
  <button className="myButton" onClick={handleLogOutClick}>
    <LogoutIcon />
    <span>Log out</span>
  </button>
  <button className="reportsButton" onClick={handleReportsClick}>
    <ReportsIcon className="icon" />
    <span>Reports</span>
  </button>
      <header className="header_ex">EXAMINATION</header>
      <div className="examination">
        <div className="webcam-container">
          <Webcam ref={webRef} />
        </div>
        <Button variant="contained" type="submit">
          START EXAMINATION
        </Button>
      </div>
    </div>
  );
}

export default Examination;
