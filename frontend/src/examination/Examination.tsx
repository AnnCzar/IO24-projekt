import React, {useRef, useState} from "react";
import Webcam from "react-webcam";
import WebcamRef from "react-webcam";
import { Button } from "@mui/material";
import "./Examination.css";
import { ReactComponent as LogoutIcon } from "../images/logout.svg";
import LoginForm from "../login-form/LoginForm";
import { ReactComponent as ReportsIcon } from "../images/reports.svg"

function Examination() {
    const webRef = useRef<WebcamRef>(null);
    const [redirect, setRedirect] = useState<boolean>(false);

    const showImage = async () => {
        if (webRef.current) {
            const screenshot = await webRef.current.getScreenshot();
            console.log(screenshot);
        }
    };

    function handleClick() {
        setRedirect(true);
    }
    if (redirect) {
    return <LoginForm />;
  }

    function handleReportsClick() {

    }

    return (
   <div className="background_ex">
  <button className="myButton" onClick={handleClick}>
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
