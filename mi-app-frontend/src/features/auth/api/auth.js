import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
});

export const getCSRFToken = async () => {
  try {
    await api.get('/api/auth/csrf/');
  } catch (error) {
    console.error('Error obteniendo CSRF:', error);
  }
};

// src/features/auth/api/auth.js
export const login = async (credentials) => {
  await getCSRFToken();
  return axios.post('/api/auth/login/', credentials);
};

export default api;