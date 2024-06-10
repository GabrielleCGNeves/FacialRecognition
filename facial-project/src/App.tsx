import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage/LandingPage';
import CameraPage from './pages/CameraPage/CameraPage';
import ConfirmationPage from './pages/ConfirmationPage/ConfirmationPage';
import SuccessPage from './pages/SuccessPage/SuccessPage';
import ErrorPage from './pages/ErrorPage/ErrorPage';
import './App.scss';


const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/camera" element={<CameraPage />} />
                <Route path="/confirmation" element={<ConfirmationPage />} />  
                <Route path="/success" element={<SuccessPage />} />
                <Route path='/badrequest' element={<ErrorPage/>}/>
            </Routes>
        </Router>
    );
};

export default App;