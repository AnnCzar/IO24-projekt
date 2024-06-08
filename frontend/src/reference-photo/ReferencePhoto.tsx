import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import { Button } from "@mui/material";
import "./ReferencePhoto.css";
<<<<<<< HEAD
import Examination from "../examination/Examination";

function ReferencePhoto() {
  const webRef = useRef<any>(null);
  const [redirect, setRedirect] = useState<boolean>(false);
=======
import {useNavigate} from "react-router-dom";

function ReferencePhoto() {
  const navigate = useNavigate();
  const webRef = useRef<any>(null);
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
  const [photoTaken, setPhotoTaken] = useState<boolean>(false);

  const showImage = async () => {
    if (webRef.current) {
      const screenshot = webRef.current.getScreenshot();
      console.log(screenshot);
      setPhotoTaken(true);
    }
  };

  const handleConfirmClick = () => {
<<<<<<< HEAD
    setRedirect(true);
  };

  if (redirect) {
    return <Examination />;
  }

  return (
    <div className="background">
      <header className="header">TAKE A REFERENCE PHOTO</header>
=======
    navigate('/examination');
  }

  return (
    <div className="background_photo">
      <header className="header_photo">TAKE A REFERENCE PHOTO</header>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
      <div className="reference-photo">
        <div className="webcam-container">
          <Webcam ref={webRef} />
        </div>
        <button onClick={showImage}>Picture</button>
<<<<<<< HEAD
        <Button variant="contained" type="submit" onClick={handleConfirmClick} disabled={!photoTaken}>
=======
        <Button variant="contained" type="submit" className="signin_reference_photo" onClick={handleConfirmClick} disabled={!photoTaken}>
>>>>>>> 4f8e8928bd28cb793509ea012c132fe2d42fba74
          SIGN IN
        </Button>
      </div>
    </div>
  );
}

export default ReferencePhoto;
