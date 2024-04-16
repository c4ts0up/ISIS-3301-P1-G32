import React from 'react';
import './App.css';
import { Form, Row, Button } from 'react-bootstrap';
import { useState } from "react";


function App() {

  const [resena, setResena] = useState("")
  const[terminado, setTerminado] = useState(false)
  const[prediccion, setPrediccion] = useState(0);


  const handleResena = (e) =>{
    const res = e.target.value;
    setResena(res)
  }

  const handlePredecir = async (e)=>{

    const requestBody = {
      // Example data fields
      res: resena
    };


    try {
      const response = await fetch('http://127.0.0.1:8000/a', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody),
      });

      if (response.ok) {
          const responseData = await response.json();
          console.log(responseData);
          setTerminado(true);
          setPrediccion(responseData.pred)
      } else {
          console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  }

  return (
    <div className="container">
      <Row>
        <h1>SOY UNA APLICACION DE BI</h1>
      </Row>
      <Row>
        <Form>
          <Form.Group>
            <Form.Label>
              Ingrese la reseña
            </Form.Label>
            <Form.Control  id="Resena"  as="textarea" rows={5} placeholder='Ingrese su reseña aca'  value={resena} onChange={handleResena}></Form.Control>
          </Form.Group>
        </Form>
      </Row>

      <Row>
        <Button variant="primary" type="submit" onClick={handlePredecir}>
          Predecir
        </Button>
      </Row>

      <Row>
        {terminado && <h3> La reseña tiene es de la clase: {prediccion}</h3>}
      </Row>
      
    </div>
  );
}

export default App;
