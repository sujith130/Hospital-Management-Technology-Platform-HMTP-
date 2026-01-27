'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/lib/auth_context';
import { useRouter, usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    Users,
    Calendar,
    Activity,
    Package,
    CreditCard,
    LogOut,
    Bell,
    Search,
    Settings
} from 'lucide-react';
import Link from 'next/link';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const { user, logout, isLoading } = useAuth();
    const router = useRouter();
    const pathname = usePathname();

    useEffect(() => {
        if (!isLoading && !user) {
            router.push('/login');
        }
    }, [user, isLoading, router]);

    if (isLoading || !user) {
        return (
            <div className="flex h-screen items-center justify-center">
                <div className="h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent"></div>
            </div>
        );
    }

    const menuItems = [
        { name: 'Dashboard', icon: LayoutDashboard, href: `/dashboard/${user.role}`, roles: ['admin', 'doctor', 'patient'] },
        { name: 'Patients', icon: Users, href: '/dashboard/patients', roles: ['admin', 'doctor'] },
        { name: 'Appointments', icon: Calendar, href: '/dashboard/appointments', roles: ['admin', 'doctor', 'patient'] },
        { name: 'Medical Records', icon: Activity, href: '/dashboard/records', roles: ['doctor', 'patient'] },
        { name: 'Pharmacy', icon: Package, href: '/dashboard/pharmacy', roles: ['admin'] },
        { name: 'Billing', icon: CreditCard, href: '/dashboard/billing', roles: ['admin', 'patient'] },
    ].filter(item => item.roles.includes(user.role));

    return (
        <div className="flex h-screen overflow-hidden text-white">
            {/* Sidebar */}
            <aside className="w-64 glass m-4 mr-0 rounded-3xl flex flex-col">
                <div className="p-8">
                    <h1 className="text-2xl font-bold text-gradient">HMTP</h1>
                    <p className="text-xs text-gray-500 mt-1 uppercase tracking-widest">{user.hospital_id}</p>
                </div>

                <nav className="flex-1 px-4 space-y-2">
                    {menuItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${pathname === item.href ? 'btn-primary' : 'hover:bg-white/5 text-gray-400 hover:text-white'
                                }`}
                        >
                            <item.icon size={20} />
                            <span className="font-medium">{item.name}</span>
                        </Link>
                    ))}
                </nav>

                <div className="p-4 border-t border-white/10">
                    <button
                        onClick={logout}
                        className="flex w-full items-center gap-3 px-4 py-3 rounded-xl text-red-400 hover:bg-red-500/10 transition-all duration-300"
                    >
                        <LogOut size={20} />
                        <span className="font-medium">Logout</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col overflow-hidden p-4">
                {/* Header */}
                <header className="flex h-16 items-center justify-between px-8 glass rounded-3xl mb-4">
                    <div className="flex items-center gap-4 flex-1">
                        <div className="relative w-96">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-4 h-4" />
                            <input
                                type="text"
                                placeholder="Search anything..."
                                className="w-full bg-white/5 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            />
                        </div>
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="relative text-gray-400 hover:text-white transition-colors">
                            <Bell size={20} />
                            <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-indigo-500"></span>
                        </button>
                        <button className="text-gray-400 hover:text-white transition-colors">
                            <Settings size={20} />
                        </button>
                        <div className="flex items-center gap-3 pl-6 border-l border-white/10">
                            <div className="text-right">
                                <p className="text-sm font-semibold">{user.full_name}</p>
                                <p className="text-[10px] text-gray-500 uppercase tracking-wider">{user.role}</p>
                            </div>
                            <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-bold">
                                {user.full_name?.[0]}
                            </div>
                        </div>
                    </div>
                </header>

                {/* Content Area */}
                <div className="flex-1 overflow-y-auto px-4 custom-scrollbar">
                    {children}
                </div>
            </main>
        </div>
    );
}
