import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ConfirmationPage.scss';
import Container from '../../components/Container';

const ConfirmationPage: React.FC = () => {
    const navigate = useNavigate();

    const handleYesClick = () => {
        navigate('/success');
    };

    const handleNoClick = () => {
        navigate('/badrequest');
    };

    return (
        <Container>
            <div className="confirmation-page">
                <h1>Olá</h1>
                <h2>Gabrielle C G Neves</h2>
                <p>RA: 131792212026</p>
                <img src="./images/gani.svg" alt="Gani foto" className="profile-pic" />
                <p>É você?</p>
                <div className="buttons">
                    <button onClick={handleYesClick} className="yes-button">SIM</button>
                    <button onClick={handleNoClick} className="no-button">NÃO</button>
                </div>
            </div>
        </Container>
    );
};

export default ConfirmationPage;
