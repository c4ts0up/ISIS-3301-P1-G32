import React from 'react';
import './App.css';
import { Form, Row, Button } from 'react-bootstrap';
import { useState } from "react";


function App() {

  const [resena, setResena] = useState("");
  const[terminado, setTerminado] = useState(true);
  const[prediccion, setPrediccion] = useState(null);
  const[score, setScore] = useState(null);
  const[file, setFile] = useState(null);
  const[termiandoFile, setTerminadoFile] = useState(true);


  const handleResena = (e) =>{
    const res = e.target.value;
    setResena(res)
  }

  const handleFileChange = (e)=>{

    setFile(e.target.files[0]);

  }

  const handlePredecir = async (e)=>{

    setTerminado(false);

    const requestBody = {
      // Example data fields
      res: resena
    };


    try {
      const response = await fetch('http://localhost:8000/a', {
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
          setScore(responseData.score)
      } else {
          console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  }

  const handlePredecir2 = async (e) => {

    setTerminadoFile(false);
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/b', {
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
    <div style={{backgroundColor:'#F6F5EB'}}>
    <div className="container">
      <Row>
        <div className='centrar'>
          <h1 className='titulo'>Clasificador de reseñas</h1>
          <h1>Universidad de los Andes</h1>
          <h2>Inteligencia de negocios</h2>
          <h3>Proyecto 1</h3>
          <h3>Grupo 32</h3>
        </div>
      </Row>

      <Row>
        <p className='descripcion'>
          Esta aplicación fue desarrollada para el proyecto 1 de la clase de Inteligencia de Negocios de La Universidad de los Andes. Se utilizaron métodos de inteligencia artificial de procesamiento de textos para crear un modelo que prediga si una reseña es positiva o negativa, asignándole una clasificación de 1 a 5. Puedes hacer la predicción de una única reseña o ingresar un archivo .csv con un banco grande de reseñas, las cuales serán clasificadas y podrás descargar un archivo con las predicciones.
        </p>

      </Row>

      <Row>
        <div className='centrar'>
          <h1>Procesar una unica reseña</h1>
        </div>
      </Row>
      <Row>
        <div className='formpadd'>
        <Form>
          <Form.Group>
            <Form.Control  id="Resena"  as="textarea" rows={5} placeholder='Ingrese su reseña aca'  value={resena} onChange={handleResena}/>
          </Form.Group>
        </Form>
        </div>
      </Row>

      <Row>
        <div className='centrarbot'>
        <Button className='bot' variant="primary" type="submit" onClick={handlePredecir}>
          Predecir
        </Button>
        </div>
      </Row>

      <Row>
        <div className='centres'>
          {!terminado && <h3> CARGANDO, ESPERE UNOS SEGUNDOS... </h3>}
          <h3> La reseña es de la clase: {prediccion} </h3>
          <h3> Con un score de: {score}</h3>
        </div>
      
      </Row>

      <Row>
        <div className='centrar'>
          <h1>Procesar un CSV con muchas reseñas</h1>
        </div>
      </Row>

      <Row>
        <div className='formpadd'>
        <Form>
          <Form.Group>
            <Form.Control type="file" onChange={handleFileChange}/>
          </Form.Group>
        </Form>
        </div>
      </Row>

      <Row>
        <div className='centrarbot'>
        <Button className='bot' variant="primary" type="submit" onClick={handlePredecir2}>
          Predecir
        </Button>
        </div>
      </Row>

      <Row>
        <div className='centres'>
          {!termiandoFile && <h3> CARGANDO, ESPERE UNOS SEGUNDOS... </h3>}
          <h3> Descargue el archivo </h3>
        </div>
      </Row>

      <Row>
        <div style={{padding:'50px'}}></div>
      </Row>
    </div>
    </div>
  );
}

export default App;
