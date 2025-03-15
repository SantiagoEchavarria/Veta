import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from '../features/auth/pages/LoginPage';
import HomePage from '../features/dashboard/pages/HomePage';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRouter;