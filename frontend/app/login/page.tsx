'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth_context';
import { authApi } from '@/lib/api';
import { Lock, Mail, User, ArrowRight, AlertCircle, Heart, Shield } from 'lucide-react';
import Image from 'next/image';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError('');

        try {
            const formData = new FormData();
            formData.append('username', email); // backend expects 'username' for OAuth2
            formData.append('password', password);

            const data = await authApi.login(formData);

            // Decode JWT to get user info
            const payload = JSON.parse(atob(data.access_token.split('.')[1]));

            login(data.access_token, {
                email: payload.sub,
                role: payload.role,
                hospital_id: payload.hospital_id,
                full_name: 'Logged In User'
            });
        } catch (err: any) {
            setError(err.message || 'Login failed. Please check your credentials.');
        } finally {
            setIsSubmitting(false);
        }
    };

    const useSampleCredentials = (email: string, password: string) => {
        setEmail(email);
        setPassword(password);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-teal-50 flex items-center justify-center p-4">
            <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
                {/* Left Side - Branding & Info */}
                <div className="hidden lg:block">
                    <div className="space-y-8">
                        <div>
                            <div className="flex items-center gap-3 mb-4">
                                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-600 to-teal-600 flex items-center justify-center">
                                    <Heart className="text-white" size={24} />
                                </div>
                                <div>
                                    <h1 className="text-3xl font-bold text-gray-900">HMTP</h1>
                                    <p className="text-sm text-gray-600">Hospital Management Platform</p>
                                </div>
                            </div>
                            <h2 className="text-4xl font-bold text-gray-900 mb-4">
                                Welcome to Your <span className="text-gradient-blue">Health Portal</span>
                            </h2>
                            <p className="text-xl text-gray-600 leading-relaxed">
                                Access your medical records, book appointments, and manage your healthcare journey all in one secure place.
                            </p>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-start gap-4">
                                <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                    <Shield className="text-blue-600" size={20} />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-gray-900 mb-1">Secure & Private</h3>
                                    <p className="text-gray-600 text-sm">Your health data is encrypted and protected with industry-leading security.</p>
                                </div>
                            </div>
                            <div className="flex items-start gap-4">
                                <div className="w-10 h-10 rounded-full bg-teal-100 flex items-center justify-center flex-shrink-0">
                                    <Heart className="text-teal-600" size={20} />
                                </div>
                                <div>
                                    <h3 className="font-semibold text-gray-900 mb-1">24/7 Access</h3>
                                    <p className="text-gray-600 text-sm">View your records and book appointments anytime, anywhere.</p>
                                </div>
                            </div>
                        </div>

                        {/* Sample Credentials */}
                        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
                            <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                                <AlertCircle size={18} className="text-blue-600" />
                                Test Patient Credentials
                            </h3>
                            <div className="space-y-3">
                                <div className="bg-white rounded-lg p-3">
                                    <p className="text-xs text-gray-600 mb-1">Patient 1</p>
                                    <div className="flex items-center justify-between">
                                        <div className="text-sm">
                                            <p className="font-mono text-gray-900">patient1@hospital.com</p>
                                            <p className="font-mono text-gray-600">password123</p>
                                        </div>
                                        <button
                                            onClick={() => useSampleCredentials('patient1@hospital.com', 'password123')}
                                            className="text-xs text-blue-600 hover:text-blue-700 font-semibold"
                                        >
                                            Use
                                        </button>
                                    </div>
                                </div>
                                <div className="bg-white rounded-lg p-3">
                                    <p className="text-xs text-gray-600 mb-1">Patient 2</p>
                                    <div className="flex items-center justify-between">
                                        <div className="text-sm">
                                            <p className="font-mono text-gray-900">patient2@hospital.com</p>
                                            <p className="font-mono text-gray-600">password123</p>
                                        </div>
                                        <button
                                            onClick={() => useSampleCredentials('patient2@hospital.com', 'password123')}
                                            className="text-xs text-blue-600 hover:text-blue-700 font-semibold"
                                        >
                                            Use
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Side - Login Form */}
                <div className="medical-card">
                    <div className="mb-8">
                        <h2 className="text-3xl font-bold text-gray-900 mb-2">Patient Login</h2>
                        <p className="text-gray-600">Sign in to access your health portal</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div>
                            <label className="label-medical">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="input-medical pl-12"
                                    placeholder="patient@hospital.com"
                                    required
                                />
                            </div>
                        </div>

                        <div>
                            <label className="label-medical">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input-medical pl-12"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="p-4 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm flex items-start gap-2">
                                <AlertCircle size={18} className="flex-shrink-0 mt-0.5" />
                                <span>{error}</span>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="btn-primary w-full py-4 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {isSubmitting ? (
                                <>
                                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                    Signing in...
                                </>
                            ) : (
                                <>
                                    Sign In
                                    <ArrowRight size={20} />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Mobile Sample Credentials */}
                    <div className="lg:hidden mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 mb-2 text-sm flex items-center gap-2">
                            <AlertCircle size={16} className="text-blue-600" />
                            Test Credentials
                        </h3>
                        <div className="space-y-2">
                            <button
                                onClick={() => useSampleCredentials('patient1@hospital.com', 'password123')}
                                className="w-full text-left bg-white rounded p-2 text-xs hover:bg-gray-50"
                            >
                                <p className="font-mono text-gray-900">patient1@hospital.com</p>
                                <p className="font-mono text-gray-600">password123</p>
                            </button>
                            <button
                                onClick={() => useSampleCredentials('patient2@hospital.com', 'password123')}
                                className="w-full text-left bg-white rounded p-2 text-xs hover:bg-gray-50"
                            >
                                <p className="font-mono text-gray-900">patient2@hospital.com</p>
                                <p className="font-mono text-gray-600">password123</p>
                            </button>
                        </div>
                    </div>

                    <div className="mt-6 text-center">
                        <p className="text-gray-600 text-sm">
                            Don't have an account?{' '}
                            <a href="/register" className="text-blue-600 hover:text-blue-700 font-semibold">
                                Register here
                            </a>
                        </p>
                        <p className="text-gray-500 text-xs mt-2">
                            <a href="/" className="hover:text-gray-700">
                                ← Back to Home
                            </a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
