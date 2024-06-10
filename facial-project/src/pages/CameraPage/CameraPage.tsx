import React from 'react';
import Camera from '../../components/Camera';
import Container from '../../components/Container';
import './CameraPage.scss';

const CameraPage: React.FC = () => {
    // const navigate = useNavigate();

    // const handleStartClick = () => {
    //     navigate('/confirmation');
    // };
    return (
        <Container>
            <div className="camera-page">
                <p>Centralize seu rosto. Quando estiver pronto,</p>
                <p>clique no botão</p>
                {/* <div className="camera-frame"></div>
                <button onClick={handleStartClick} className="capture-button">Capturar</button> */}
                <div className="camera-frame">
                    <Camera />
                </div>
            </div>
        </Container>
    );
};

export default CameraPage;
