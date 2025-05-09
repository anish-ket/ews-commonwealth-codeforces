'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

const users = [
  { email: 'parth@somaiya.edu', password: 'parth1' },
  { email: 'ritul@somaiya.edu', password: 'ritul1' },
  { email: 'anish@somaiya.edu', password: 'anish1' },
];

export default function AuthPage() {

  
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isLogin) {
      const user = users.find(
        (u) => u.email === form.email && u.password === form.password
      );
      if (user) {
        setError('');
        router.push('/dashboard'); // Redirect after successful login
      } else {
        setError('Invalid credentials.');
      }
    } else {
      setError('Sign Up is disabled for now.');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  return (

    <>
    <div 
            className="fixed top-0 left-0 w-full h-full z-[-1]"
            style={{
                backgroundImage: "url('/images/backgrounds/event-bg.jpeg')",
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundRepeat: "no-repeat",
                filter: "blur(15px) brightness(0.9)"
            }}
            />


    <div className="min-h-screen flex items-center justify-center text-white transition-all overflow-hidden">
      <div className="w-full max-w-md p-8 shadow-xl bg-[rgba(64,61,61,0.75)] rounded-[17.617px] overflow-hidden">
        <h1 className="text-2xl font-bold mb-6 text-center">
          {isLogin
            ? 'Login to Commonwealth Early Warning Dashboard'
            : 'Sign Up for CommonWealth Early Warning Dashboard'}
        </h1>
        <form onSubmit={handleSubmit} className="space-y-5 overflow-hidden">
          <div>
            <label className="block mb-1 text-sm text-gray-300">Email</label>
            <input
              type="email"
              name="email"
              required
              value={form.email}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-gray-600 transition"
            />
          </div>
          <div>
            <label className="block mb-1 text-sm text-gray-300">Password</label>
            <input
              type="password"
              name="password"
              required
              value={form.password}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-gray-600 transition"
            />
          </div>
          {error && (
            <div className="text-red-500 text-sm text-center">{error}</div>
          )}
          <button
            type="submit"
            className="w-full py-2 px-4 bg-white text-black font-semibold rounded-lg hover:bg-gray-300 transition"
          >
            {isLogin ? 'Log In' : 'Sign Up'}
          </button>
        </form>
        <div className="mt-6 text-center">
          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setForm({ email: '', password: '' });
              setError('');
            }}
            className="text-sm text-white hover:text-gray-200 transition"
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : 'Already have an account? Log in'}
          </button>
        </div>
      </div>
    </div>
    </>
  );
}