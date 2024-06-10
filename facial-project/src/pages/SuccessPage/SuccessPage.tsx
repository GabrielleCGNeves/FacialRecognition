import React from 'react';
import { useNavigate } from 'react-router-dom';
import './SuccessPage.scss';
import Container from '../../components/Container';

const SuccessPage: React.FC = () => {
    const navigate = useNavigate();

    const handleBackClick = () => {
        navigate('/');
    };

    return (
        <Container>
            <div className="success-page">
                <p>Registro anterior: 28/05/2024</p>
                <h1>Enviado com sucesso</h1>
                <img src='./images/Confirmed.svg'></img>
                <button onClick={handleBackClick} className="back-button">VOLTAR</button>
            </div>
        </Container>
    );
};

export default SuccessPage;
