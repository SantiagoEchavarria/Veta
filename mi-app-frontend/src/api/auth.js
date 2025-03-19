import api from './axios';

export const authService = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  getCsrfToken: () => api.get('/auth/csrf/'),
  getProfile: () => api.get('/usuarios/me/'),
  updateProfile: (data) => api.patch('/usuarios/me/', data),
  passwordReset: (email) => api.post('/auth/password-reset/', { email }),
  passwordResetConfirm: (data) => api.post('/auth/password-reset/confirm/', data),
};