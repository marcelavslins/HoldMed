import React, { useState } from 'react';
import '../App.css';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simular autenticação
    setTimeout(() => {
      if (email === 'admin@holdmed.com' && password === 'admin123') {
        onLogin({ email, name: 'Dr. Carlos Silva' });
      } else {
        setError('Email ou senha incorretos. Use admin@holdmed.com / admin123');
      }
      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <img 
            src="/holdmed-logo.jpg" 
            alt="HoldMed Logo" 
            className="h-16 w-auto mx-auto mb-4"
          />
          <h1 className="text-3xl font-bold text-gray-900 mb-2">HoldMed</h1>
          <p className="text-gray-600">Plataforma de IA para Monitoramento Pós-Operatório</p>
        </div>

        <div className="login-form">
          <h2 className="text-2xl text-center mb-6">Entrar</h2>
          <p className="text-center text-gray-600 mb-6">
            Acesse sua conta para monitorar pacientes
          </p>
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Senha</label>
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="Sua senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{ 
                  position: 'absolute', 
                  right: '10px', 
                  top: '50%', 
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>

            {error && (
              <div className="error">
                {error}
              </div>
            )}

            <button 
              type="submit" 
              className="btn-primary" 
              disabled={loading}
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Credenciais de demonstração:
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Email: admin@holdmed.com<br />
              Senha: admin123
            </p>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2024 HoldMed. Todos os direitos reservados.</p>
          <p className="mt-1">Transformando dados clínicos em decisões que salvam vidas</p>
        </div>
      </div>
    </div>
  );
};

export default Login;

