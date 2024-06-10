import axios from 'axios'
import { useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import Webcam from 'react-webcam'
import './Camera.scss'

const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: 'user',
}

const Camera = () => {
  const navigate = useNavigate()

  const webcamRef = useRef<Webcam>(null)

  const capture = useCallback(async () => {
    const imageSrc = webcamRef.current?.getScreenshot()
    const response = await axios
      .post('http://localhost:5000/upload', {
        encodedPicture: imageSrc,
      })
      .catch((error) => {
        console.log(error.response.data);
        
        navigate('/badrequest')
      })
      
      if (response) {
        navigate('/confirmation', { state: { data: response.data }})
      }
      
  }, [webcamRef, navigate])

  return (
    <>
      <Webcam
        audio={false}
        height={300}
        forceScreenshotSourceSize={true}
        ref={webcamRef}
        screenshotFormat='image/jpeg'
        width={300}
        videoConstraints={videoConstraints}
      />

      <button className='capture-button' onClick={capture}>
        Capture photo
      </button>
    </>
  )
}

export default Camera
