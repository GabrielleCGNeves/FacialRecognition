import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '../../components/Container';
import './SuccessPage.scss';

const SuccessPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
  
    const data = location.state?.data;

    if (!data) {
        return <div>Erro: Nenhum dado recebido.</div>;
    }

    const local_date = new Date(data.last_attendance).toLocaleString();

    const handleBackClick = () => {
        navigate('/');
    };

    return (
        <Container>
            <div className="success-page">
                <p>Registro anterior: {local_date}</p>
                <h1>Enviado com sucesso</h1>
                <img src='./images/Confirmed.svg'></img>
                <button onClick={handleBackClick} className="back-button">VOLTAR</button>
            </div>
        </Container>
    );
};

export default SuccessPage;
