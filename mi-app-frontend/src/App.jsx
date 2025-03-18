import { useEffect } from 'react';
import api from './api/axios';

function App() {
  const initializeCSRF = async () => {
    try {
      await api.get('/auth/csrf/');
      console.log('CSRF token obtenido');
    } catch (error) {
      console.error('Error al obtener CSRF:', error);
    }
  };

  const sendPostRequest = async () => {
    try {
      const response = await api.post('/mi-endpoint/', {
        nombre: 'Ejemplo'
      });
      console.log('Respuesta POST:', response.data);
    } catch (error) {
      console.error('Error POST:', error.response?.data);
    }
  };

  useEffect(() => {
    initializeCSRF();
  }, []);

  return (
    <div>
      <button onClick={sendPostRequest}>Enviar POST</button>
    </div>
  );
}

export default App;