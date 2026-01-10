"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token in cookie/localStorage (simplified for MVP)
        localStorage.setItem("todo_token", data.access_token);
        router.push("/tasks");
      } else {
        setError(data.detail || "Login failed");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 -left-20 w-96 h-96 bg-violet-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float"></div>
        <div className="absolute top-1/3 -right-20 w-96 h-96 bg-cyan-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style={{animationDelay: "1s"}}></div>
        <div className="absolute -bottom-20 left-1/3 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-float" style={{animationDelay: "2s"}}></div>
      </div>

      <div className="w-full max-w-md space-y-8 glass p-10 rounded-3xl shadow-2xl backdrop-blur-xl border border-white/40 animate-scale-in relative z-10">
        <div className="text-center space-y-2">
          <div className="inline-block p-3 bg-gradient-to-r from-violet-500 to-cyan-500 rounded-2xl shadow-lg mb-2 animate-float">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h1 className="text-4xl font-black text-gradient">Welcome Back</h1>
          <p className="text-gray-600 font-medium">Continue your productivity journey</p>
        </div>

        {error && (
          <div className="p-4 text-sm text-red-600 bg-red-50/80 backdrop-blur-sm border border-red-200 rounded-2xl flex items-center space-x-3 animate-slide-down">
            <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
            </svg>
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="block text-sm font-bold text-gray-700 ml-1">Email Address</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/>
                </svg>
              </div>
              <input
                type="email"
                required
                className="w-full pl-12 pr-4 py-3.5 bg-white/50 backdrop-blur-sm border-2 border-gray-200 rounded-xl focus:bg-white focus:border-violet-400 focus:ring-4 focus:ring-violet-100 outline-none transition-all duration-300 font-medium"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-bold text-gray-700 ml-1">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>
              <input
                type="password"
                required
                className="w-full pl-12 pr-4 py-3.5 bg-white/50 backdrop-blur-sm border-2 border-gray-200 rounded-xl focus:bg-white focus:border-violet-400 focus:ring-4 focus:ring-violet-100 outline-none transition-all duration-300 font-medium"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 px-6 bg-gradient-to-r from-violet-600 via-blue-600 to-cyan-600 text-white rounded-xl font-bold text-base shadow-lg shadow-violet-200 hover:shadow-xl hover:shadow-violet-300 transition-all duration-300 disabled:opacity-50 disabled:shadow-none flex items-center justify-center space-x-2 active:scale-95 hover:scale-[1.02] relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 via-blue-600 to-violet-600 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin relative z-10" />
                <span className="relative z-10">Signing in...</span>
              </>
            ) : (
              <span className="relative z-10">Sign In</span>
            )}
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-white/70 backdrop-blur-sm text-gray-600 rounded-full font-medium">New to our platform?</span>
          </div>
        </div>

        <Link
          href="/register"
          className="block w-full py-3 px-6 text-center bg-white/50 backdrop-blur-sm border-2 border-gray-300 text-gray-700 rounded-xl font-bold hover:bg-white hover:border-gray-400 hover:shadow-lg transition-all duration-300 active:scale-95"
        >
          Create Free Account
        </Link>
      </div>
    </div>
  );
}
