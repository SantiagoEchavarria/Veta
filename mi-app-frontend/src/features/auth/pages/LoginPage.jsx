const LoginPage = () => {
    return (
      <div className="max-w-md mx-auto mt-10 p-4">
        <h2 className="text-2xl font-bold mb-4">Iniciar Sesión</h2>
        {/* Formulario básico temporal */}
        <form>
          <input
            type="email"
            placeholder="Email"
            className="w-full mb-4 p-2 border rounded"
          />
          <input
            type="password"
            placeholder="Contraseña"
            className="w-full mb-4 p-2 border rounded"
          />
          <button className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
            Ingresar
          </button>
        </form>
      </div>
    );
  };
  
  export default LoginPage;