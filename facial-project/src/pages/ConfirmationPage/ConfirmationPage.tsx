import axios from 'axios'
import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Container from '../../components/Container'
import './ConfirmationPage.scss'

const ConfirmationPage: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  const data = location.state?.data

  if (!data) {
    return <div>Erro: Nenhum dado recebido.</div>
  }

  console.log(data)

  const handleYesClick = async () => {
    const response = await axios
      .post('http://localhost:5000/attendance', {
        label: data.label,
      })
      .catch((error) => {
        console.log(error.response.data)
        navigate('/badrequest')
      })

    if (response) console.log(response.data)

    navigate('/success', { state: { data } })
  }

  const handleNoClick = () => {
    navigate('/camera')
  }

  return (
    <Container>
      <div className='confirmation-page'>
        <h1>Olá</h1>
        <h2>{data.name}</h2>
        <p>RA: {data.label}</p>
        <div className='profile-pic-wrapper'>
          {data.encodedPicture ? (
            <img
              src={data.encodedPicture}
              alt='Foto do aluno'
              className='profile-pic'
            />
          ) : null}
        </div>
        <p>É você?</p>
        <div className='buttons'>
          <button onClick={handleYesClick} className='yes-button'>
            SIM
          </button>
          <button onClick={handleNoClick} className='no-button'>
            NÃO
          </button>
        </div>
      </div>
    </Container>
  )
}

export default ConfirmationPage
