import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import { Button } from "@mui/material";
import "./ReferencePhoto.css";
import {useNavigate} from "react-router-dom";
import logo from "../images/Logo3.svg";

function ReferencePhoto() {
  const navigate = useNavigate();
  const webRef = useRef<any>(null);
  const [photoTaken, setPhotoTaken] = useState<boolean>(false);

  const showImage = async () => {
    if (webRef.current) {
      const screenshot = webRef.current.getScreenshot();
      console.log(screenshot);
      setPhotoTaken(true);
    }
  };

  const handleConfirmClick = () => {
    navigate('/examination');
  }

  return (
    <div className="background_photo">
      <header className="header_photo">TAKE A REFERENCE PHOTO</header>
      <img src={logo} alt="Logo" className="logo_bottom" />
      <div className="reference-photo">
        <div className="webcam-container">
          <Webcam ref={webRef} />
        </div>
        <button onClick={showImage}>Picture</button>
        <Button variant="contained" type="submit" className="signin_reference_photo" onClick={handleConfirmClick} disabled={!photoTaken}>
          SIGN IN
        </Button>
      </div>
    </div>
  );
}

export default ReferencePhoto;
