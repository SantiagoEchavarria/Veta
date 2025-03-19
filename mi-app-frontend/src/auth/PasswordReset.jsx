import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../api/auth';

export default function PasswordReset() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await authService.passwordReset(email);
      setMessage('Instrucciones enviadas a tu correo electrónico');
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setMessage(err.response?.data?.detail || 'Error al procesar la solicitud');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>Recuperar Contraseña</h2>
      {message && <div className="info-message">{message}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email registrado:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Enviando...' : 'Enviar Instrucciones'}
        </button>
      </form>
      
      <div className="auth-links">
        <button onClick={() => navigate('/login')}>Volver al login</button>
      </div>
    </div>
  );
}