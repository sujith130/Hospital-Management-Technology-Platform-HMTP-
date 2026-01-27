'use client';

import React, { useState } from 'react';
import { useAuth } from '@/lib/auth_context';
import { authApi } from '@/lib/api';
import { Lock, Mail, Building, ArrowRight } from 'lucide-react';
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

            // For this demo, we'll decode the JWT or fetch user profile
            // In a real app, you'd fetch the user profile here
            // We'll mock the user data from the JWT payload we know we sent
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

    return (
        <div className="flex min-h-screen items-center justify-center p-4">
            <div className="glass-card flex w-full max-w-5xl overflow-hidden !p-0">
                {/* Visual Side */}
                <div className="relative hidden w-1/2 lg:block">
                    <Image
                        src="/images/hero.png"
                        alt="Hospital Hero"
                        fill
                        className="object-cover"
                        priority
                    />
                    <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-transparent flex flex-col justify-end p-12">
                        <h1 className="text-4xl font-bold text-white mb-4">HMTP</h1>
                        <p className="text-gray-300 text-lg">
                            Enterprise Multi-Tenant Hospital Management Platform. Secure, Scalable, Compliant.
                        </p>
                    </div>
                </div>

                {/* Login Form Side */}
                <div className="w-full p-12 lg:w-1/2">
                    <div className="mb-10">
                        <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
                        <p className="text-gray-400">Sign in to your hospital dashboard</p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full glass bg-white/5 rounded-xl py-3 pl-12 pr-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                                    placeholder="name@hospital.com"
                                    required
                                />
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-300 ml-1">Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full glass bg-white/5 rounded-xl py-3 pl-12 pr-4 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
                                    placeholder="••••••••"
                                    required
                                />
                            </div>
                        </div>

                        {error && (
                            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-500 text-sm">
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={isSubmitting}
                            className="btn-primary w-full py-4 flex items-center justify-center gap-2 group disabled:opacity-50"
                        >
                            {isSubmitting ? 'Signing in...' : 'Sign In'}
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                    </form>

                    <div className="mt-8 text-center text-gray-500 text-sm">
                        Don't have an account? <span className="text-indigo-400 cursor-pointer hover:underline">Get started</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
