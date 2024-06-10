import { useState, useRef, useCallback } from "react";
import Webcam from "react-webcam";
import './Camera.scss'

const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
};

const Camera = () => {
    const webcamRef = useRef<Webcam>(null);
    const [imgSrc, setImgSrc] = useState<string | null>(null)
    const capture = useCallback(
        () => {
            const imageSrc = webcamRef.current?.getScreenshot();
            if (imageSrc) setImgSrc(imageSrc)
        },
        [webcamRef]
    );
    
    return (
        <>
            {imgSrc ? (
                <img src={imgSrc} />
            ) : <Webcam
                audio={false}
                height={300}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={300}
                videoConstraints={videoConstraints} />
            }

            <button className="capture-button" onClick={capture}>Capture photo</button>
        </>
    );
};

export default Camera