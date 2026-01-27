'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/lib/auth_context';
import { ArrowRight, ShieldCheck } from 'lucide-react';

export default function Home() {
    const router = useRouter();
    const { user, isLoading } = useAuth();

    useEffect(() => {
        if (!isLoading && user) {
            router.push(`/dashboard/${user.role}`);
        }
    }, [user, isLoading, router]);

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24 text-center">
            <div className="glass-card max-w-2xl py-12 px-16 space-y-8 animate-in zoom-in duration-1000">
                <div className="inline-flex p-3 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 mb-4">
                    <ShieldCheck size={40} />
                </div>
                <h1 className="text-6xl font-bold text-white tracking-tight">
                    HMTP <span className="text-indigo-500">Platform</span>
                </h1>
                <p className="text-xl text-gray-400">
                    Advanced Multi-Tenant Hospital Management Technology Platform.
                    Secured with Enterprise-grade RBAC and Cloud-Native Scalability.
                </p>
                <div className="pt-4">
                    <button
                        onClick={() => router.push('/login')}
                        className="btn-primary flex items-center gap-2 mx-auto px-10 py-5 text-lg"
                    >
                        Enter Platform
                        <ArrowRight size={20} />
                    </button>
                </div>
            </div>

            <div className="absolute bottom-10 text-gray-600 text-sm uppercase tracking-[0.3em]">
                Enterprise Version 1.0.0
            </div>
        </main>
    );
}
