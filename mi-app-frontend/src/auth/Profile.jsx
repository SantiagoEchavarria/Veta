import { useEffect, useState } from 'react';
import { authService } from '../api/auth';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    nombre: '',
    telefono: '',
    fecha_nacimiento: ''
  });

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await authService.getProfile();
        setUser(response.data);
        setFormData({
          nombre: response.data.nombre,
          telefono: response.data.telefono,
          fecha_nacimiento: response.data.fecha_nacimiento
        });
      } catch (err) {
        console.error('Error loading profile:', err);
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await authService.updateProfile(formData);
      setUser(response.data);
      alert('Perfil actualizado correctamente');
    } catch (err) {
      console.error('Error updating profile:', err);
    }
  };

  if (loading) return <div>Cargando perfil...</div>;

  return (
    <div className="profile-container">
      <div className="gravatar-section">
        <img 
          src={user.gravatar_url} 
          alt="Avatar" 
          className="gravatar-img"
        />
        <h2>{user.nombre}</h2>
        <p>{user.email}</p>
      </div>

      <form onSubmit={handleUpdate} className="profile-form">
        <div className="form-group">
          <label>Nombre:</label>
          <input
            type="text"
            value={formData.nombre}
            onChange={(e) => setFormData({...formData, nombre: e.target.value})}
          />
        </div>

        <div className="form-group">
          <label>Teléfono:</label>
          <input
            type="tel"
            value={formData.telefono}
            onChange={(e) => setFormData({...formData, telefono: e.target.value})}
          />
        </div>

        <div className="form-group">
          <label>Fecha de Nacimiento:</label>
          <input
            type="date"
            value={formData.fecha_nacimiento}
            onChange={(e) => setFormData({...formData, fecha_nacimiento: e.target.value})}
          />
        </div>

        <button type="submit">Actualizar Perfil</button>
      </form>
    </div>
  );
}