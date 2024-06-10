import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CameraPage.scss';
import Container from '../../components/Container';
import Camera from '../../components/Camera';

const CameraPage: React.FC = () => {
    const navigate = useNavigate();

    const handleStartClick = () => {
        navigate('/confirmation');
    };
    return (
        <Container>
            <div className="camera-page">
                <p>Centralize seu rosto. Quando estiver pronto,</p>
                <p>clique no botão</p>
                {/* <div className="camera-frame"></div>
                <button onClick={handleStartClick} className="capture-button">Capturar</button> */}
                <Camera />
            </div>
        </Container>
    );
};

export default CameraPage;
