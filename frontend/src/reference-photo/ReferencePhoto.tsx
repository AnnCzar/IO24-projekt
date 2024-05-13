import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import { Button } from "@mui/material";
import "./ReferencePhoto.css";
import Examination from "../examination/Examination";

function ReferencePhoto() {
  const webRef = useRef<any>(null);
  const [redirect, setRedirect] = useState<boolean>(false);
  const [photoTaken, setPhotoTaken] = useState<boolean>(false);

  const showImage = async () => {
    if (webRef.current) {
      const screenshot = webRef.current.getScreenshot();
      console.log(screenshot);
      setPhotoTaken(true);
    }
  };

  const handleConfirmClick = () => {
    setRedirect(true);
  };

  if (redirect) {
    return <Examination />;
  }

  return (
    <div className="background">
      <header className="header">TAKE A REFERENCE PHOTO</header>
      <div className="reference-photo">
        <div className="webcam-container">
          <Webcam ref={webRef} />
        </div>
        <button onClick={showImage}>Picture</button>
        <Button variant="contained" type="submit" onClick={handleConfirmClick} disabled={!photoTaken}>
          SIGN IN
        </Button>
      </div>
    </div>
  );
}

export default ReferencePhoto;
