import React from 'react';
import './App.css';
import { Form, Row, Button } from 'react-bootstrap';
import { useState } from "react";


function App() {

  const [resena, setResena] = useState("");
  const[terminado, setTerminado] = useState(false);
  const[prediccion, setPrediccion] = useState(0);
  const[file, setFile] = useState(null);
  const[termiandoFile, setTerminadoFile] = useState(false);


  const handleResena = (e) =>{
    const res = e.target.value;
    setResena(res)
  }

  const handleFileChange = (e)=>{

    setFile(e.target.files[0]);

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

  const handlePredecir2 = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/b', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "Predicciones"
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      setTerminadoFile(true);

    } catch (error) {
      console.error('Error:', error);
    }
  }



  return (
    <div className="container">
      <Row>
        <h1>SOY UNA APLICACION DE BI SOLO UNA RESENA</h1>
      </Row>
      <Row>
        <Form>
          <Form.Group>
            <Form.Label>
              Ingrese la reseña
            </Form.Label>
            <Form.Control  id="Resena"  as="textarea" rows={5} placeholder='Ingrese su reseña aca'  value={resena} onChange={handleResena}/>
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

      <Row>
        <h1>SOY UNA APLICACION DE BI UN ARCHIVO CSV PARA CLASIFICAR RESENAS</h1>
      </Row>

      <Row>
        <Form>
          <Form.Group>
            <Form.Label>
              Archivo CSV con resenas a predecir
            </Form.Label>
            <Form.Control type="file" onChange={handleFileChange}/>
          </Form.Group>
        </Form>
      </Row>

      <Row>
        <Button variant="primary" type="submit" onClick={handlePredecir2}>
          Predecir
        </Button>
      </Row>

      <Row>
        {termiandoFile && <h3> Descargue el archivo</h3>}
      </Row>


      
    </div>
  );
}

export default App;
