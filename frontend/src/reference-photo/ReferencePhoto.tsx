import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./ReferencePhoto.css";

function ReferencePhoto() {

  const navigate = useNavigate();
  const webRef = useRef<Webcam>(null);
  const [photoTaken, setPhotoTaken] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

   const handleConfirmClick = () => {
    navigate('/examination');
  }

  const showImage = useCallback(async () => {
    if (webRef.current) {
      const screenshot = webRef.current.getScreenshot();
      setImage(screenshot);
      setPhotoTaken(true);

      try {
        const response = await fetch('http://localhost:8000/capture-photo/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: screenshot }),
        });

        if (response.status === 201) {
          navigate('/examination');
        } else {
          setErrorMessage("Failed to upload the photo. Please try again.");
        }
      } catch (error) {
        setErrorMessage("An error occurred. Please try again.");
      }
    }
  }, [webRef, navigate]);

  return (
    <div className="background_photo">
      <header className="header_photo">TAKE A REFERENCE PHOTO</header>
      <div className="reference-photo">
        <div className="webcam-container">
          <Webcam ref={webRef} screenshotFormat="image/jpeg" />
        </div>
        <button onClick={showImage}>Picture</button>
        <Button
          variant="contained"
          type="submit"
          className="signin_reference_photo"
          onClick={handleConfirmClick}
          disabled={!photoTaken}
        >
          SIGN IN
        </Button>
        {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default ReferencePhoto;