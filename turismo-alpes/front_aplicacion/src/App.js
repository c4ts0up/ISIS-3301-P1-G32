import React from 'react';
import './App.css';
import { Form, Row, Button } from 'react-bootstrap';
import { useState } from "react";


function App() {

  const [resena, setResena] = useState("")

  const[terminado, setTerminado] = useState(false)


  const handleResena = (e) =>{
    const res = e.target.value;
    setResena(res)
  }

  const handlePredecir = (e)=>{
    
    console.log("ACA VA LO DE PREDDECIR")
    console.log(resena)
    setTerminado(true)

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
        {terminado && <h3> La reseña tiene es de la clase: Falta implementar</h3>}
      </Row>
      
    </div>
  );
}

export default App;
