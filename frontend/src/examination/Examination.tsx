import React, { useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";
import {
    Alert,
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Typography
} from "@mui/material";
import "./Examination.css";
import { ReactComponent as LogoutIcon } from "../images/logout.svg";
import { ReactComponent as ReportsIcon } from "../images/reports.svg";
import { useNavigate } from "react-router-dom";
import logo from "../images/Logo3.svg";
import axios from "axios";

function Examination() {
    const navigate = useNavigate();
    const webRef = useRef<Webcam>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [showInstruction, setShowInstruction] = useState(false);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);


    const handleLogOutClick = useCallback(() => {
        navigate('/login');
    }, [navigate]);

    const handleReportsClick = useCallback(() => {
        navigate('/reports-patient');
    }, [navigate]);

    const handleStartExamination = useCallback(() => {
        setShowInstruction(true);
    }, []);

    const startRecording = useCallback(() => {
        setShowInstruction(false);

        if (!webRef.current || !webRef.current.stream) return;
        setIsRecording(true);

        const videoConstraints = {
            width: 1280,
            height: 720,
            aspectRatio: 1.7778,
        };

        const recordedChunks: BlobPart[] = [];
        const mediaRecorder = new MediaRecorder(webRef.current.stream, {
            mimeType: "video/webm"
        });

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const blob = new Blob(recordedChunks, {type: 'video/webm'});
            const videoFile = new File([blob], "recording.webm", {type: "video/webm"});
            const formData = new FormData();
            formData.append('video', videoFile);

            try {
                const response = await axios.post('http://localhost:8000/add_recording/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    withCredentials: true
                });
                setSuccessMessage("Video uploaded successfully");
                console.log("Video uploaded successfully:", response.data);
            } catch (error) {
                setErrorMessage("Error occured during uploading a video");
                console.error("Error uploading video:", error);
            } finally {
                setIsRecording(false);
            }
        };

        mediaRecorder.start();
        setTimeout(() => {
            mediaRecorder.stop();
        }, 10000); // 10 seconds
    }, [webRef]);

    return (
        <div className="background_ex">
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
            <button className="myButton" onClick={handleLogOutClick}>
                <LogoutIcon />
                <span>Log out</span>
            </button>
            <button className="reportsButton" onClick={handleReportsClick}>
                <ReportsIcon className="icon" />
                <span>Reports</span>
            </button>
            <header className="header_ex">EXAMINATION</header>
            <img src={logo} alt="Logo" className="logo_bottom" />
            <div className="examination">
                <div className="webcam-container">
                    <Webcam audio={true} ref={webRef} />
                    <div className="overlay-square"></div>
                </div>
                <Button
                    variant="contained"
                    type="submit"
                    onClick={handleStartExamination}
                    disabled={isRecording}
                >
                    {isRecording ? 'RECORDING...' : 'START EXAMINATION'}
                </Button>
                <Dialog
                    open={showInstruction}
                    onClose={() => setShowInstruction(false)}
                >
                    <DialogTitle>Instructions</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            position your head so that it is as directly facing the camera as possible and fits entirely within the frame.
                            Then, smile as widely as you can until the end of the test (10 seconds).
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={startRecording} color="primary">
                            Start
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        </div>
    );
}

export default Examination;
