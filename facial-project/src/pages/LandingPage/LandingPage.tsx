import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.scss';
import Container from '../../components/Container';

const LandingPage: React.FC = () => {
    const navigate = useNavigate();

    const handleStartClick = () => {
        navigate('/camera');
    };

    return (
        <Container>
            <div className="landing-page">
                <div className="header">
                    <h1>Bem-vindo!</h1>
                    <p>Registre a sua presença</p>
                    <img src='./images/LandingPage.svg' className='landingpage-img'></img>
                </div>
                <button onClick={handleStartClick} className="start-button">COMEÇAR</button>
            </div>
        </Container>
    );
};

export default LandingPage;
