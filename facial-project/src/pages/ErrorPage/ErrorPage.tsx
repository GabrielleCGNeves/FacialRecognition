import React from "react";
import "./ErrorPage.scss";
import { useNavigate } from 'react-router-dom';
import Container from "../../components/Container";

const ErrorPage: React.FC = () => {
    const navigate = useNavigate();

    const handleStartClick = () => {
        navigate('/camera');
    };

    return (
        <Container>
            <div className="badrequest-page">
                <img src="./images/Error404.svg" alt="Landing Page" className="errorpage-img" />
                <button onClick={handleStartClick} className="back-button">VOLTAR</button>
            </div>
        </Container>
    );
};

export default ErrorPage;
