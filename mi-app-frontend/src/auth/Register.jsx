import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../api/auth';
import DatePicker from '../components/DatePicker';

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    nombre: '',
    password: '',
    telefono: '',
    fecha_nacimiento: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await authService.getCsrfToken();
      await authService.register(formData);
      navigate('/login?registered=true');
    } catch (err) {
      if(err.response?.data) {
        setErrors(err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDateChange = (date) => {
    setFormData({...formData, fecha_nacimiento: date.toISOString().split('T')[0]});
  };

  return (
    <div className="auth-container">
      <h2>Registro de Usuario</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className={errors.email ? 'error' : ''}
          />
          {errors.email && <span className="error-message">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label>Nombre Completo:</label>
          <input
            type="text"
            value={formData.nombre}
            onChange={(e) => setFormData({...formData, nombre: e.target.value})}
            className={errors.nombre ? 'error' : ''}
          />
          {errors.nombre && <span className="error-message">{errors.nombre}</span>}
        </div>

        <div className="form-group">
          <label>Contraseña:</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className={errors.password ? 'error' : ''}
          />
          {errors.password && <span className="error-message">{errors.password}</span>}
        </div>

        <div className="form-group">
          <label>Teléfono:</label>
          <input
            type="tel"
            value={formData.telefono}
            onChange={(e) => setFormData({...formData, telefono: e.target.value})}
            className={errors.telefono ? 'error' : ''}
          />
          {errors.telefono && <span className="error-message">{errors.telefono}</span>}
        </div>

        <div className="form-group">
          <label>Fecha de Nacimiento:</label>
          <DatePicker 
            selectedDate={formData.fecha_nacimiento} 
            onChange={handleDateChange}
          />
          {errors.fecha_nacimiento && <span className="error-message">{errors.fecha_nacimiento}</span>}
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Registrando...' : 'Crear Cuenta'}
        </button>
      </form>
    </div>
  );
}