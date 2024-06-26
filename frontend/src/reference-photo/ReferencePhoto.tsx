import React, { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import {Button, Dialog, DialogContent, DialogContentText, DialogActions, Alert} from "@mui/material";
import { useNavigate } from "react-router-dom";
import "./ReferencePhoto.css";
import logo from "../images/Logo3.svg";

function ReferencePhoto() {
  const navigate = useNavigate();
  const webRef = useRef<Webcam>(null);
  const [photoTaken, setPhotoTaken] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [open, setOpen] = useState(true);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

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
          credentials: 'include',
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

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div className="background_photo">
      <header className="header_photo">TAKE A REFERENCE PHOTO</header>
      {successMessage && <Alert severity="success" style={{
              position: 'fixed',
              bottom: 0,
              width: '100%',
              textAlign: 'center',
              zIndex: 9999
          }}>{successMessage}</Alert>}
           {errorMessage && <Alert severity="error" style={{
        position: 'fixed',
        bottom: 0,
        width: '100%',
        textAlign: 'center',
        zIndex: 9999
      }}>{errorMessage}</Alert>}
      <img src={logo} alt="Logo" className="logo_bottom" />
      <div className="reference-photo">
        <div className="webcam-container">
          <Webcam ref={webRef} screenshotFormat="image/jpeg" />
          <div className="overlay-square"></div>
        </div>
        <Button onClick={showImage} variant="contained" color="primary" className="picture-button">
          Picture
        </Button>
        <Button
          variant="contained"
          type="submit"
          className="signin_reference_photo"
          onClick={handleConfirmClick}
          disabled={!photoTaken}
        >
          SIGN IN
        </Button>
        {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      </div>
      <Dialog open={open} onClose={handleClose}>
        <DialogContent>
          <DialogContentText>
            Position your head so that it is as directly facing the camera as possible and fits entirely within the frame.
            Then, make a neutral face and click the button to take a reference photo.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default ReferencePhoto;
