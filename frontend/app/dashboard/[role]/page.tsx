'use client';

import React from 'react';
import { useAuth } from '@/lib/auth_context';
import {
    Users,
    Calendar,
    Activity,
    TrendingUp,
    AlertCircle,
    Plus,
    FileText,
    Clock
} from 'lucide-react';

export default function RoleDashboard() {
    const { user } = useAuth();

    if (!user) return null;

    const renderStats = () => {
        switch (user.role) {
            case 'doctor':
                return (
                    <>
                        <StatCard title="Total Patients" value="1,284" icon={Users} trend="+12% from last month" />
                        <StatCard title="Today's Appointments" value="14" icon={Calendar} trend="Next: 10:30 AM" />
                        <StatCard title="Active Treatments" value="48" icon={Activity} trend="8 pending review" />
                        <StatCard title="Satisfaction" value="98%" icon={TrendingUp} trend="Top 5% in hospital" />
                    </>
                );
            case 'admin':
                return (
                    <>
                        <StatCard title="Monthly Revenue" value="$84,200" icon={TrendingUp} trend="+5.4% this week" />
                        <StatCard title="New Admissions" value="124" icon={Users} trend="Active: 89" />
                        <StatCard title="Inventory Alerts" value="3" icon={AlertCircle} trend="Critical: 0" color="text-red-400" />
                        <StatCard title="Staff Active" value="56" icon={Activity} trend="8 on night shift" />
                    </>
                );
            case 'patient':
                return (
                    <>
                        <StatCard title="Upcoming Visit" value="Oct 24" icon={Calendar} trend="Dr. Sarah Johnson" />
                        <StatCard title="Total Records" value="28" icon={FileText} trend="Last added: Oct 12" />
                        <StatCard title="Health Score" value="A+" icon={Activity} trend="Stable for 6 months" />
                        <StatCard title="Outstanding Bills" value="$0.00" icon={TrendingUp} trend="No pending payments" color="text-green-400" />
                    </>
                );
            default:
                return null;
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            <div>
                <h1 className="text-3xl font-bold text-white">Welcome back, {user.full_name}</h1>
                <p className="text-gray-400 mt-2">Here's what's happening in your hospital today.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {renderStats()}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Activity / Schedule */}
                <div className="lg:col-span-2 glass-card h-96 overflow-hidden flex flex-col">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold">Recent Activity</h3>
                        <button className="text-sm text-indigo-400 hover:underline">View all</button>
                    </div>
                    <div className="flex-1 space-y-4 overflow-y-auto pr-2 custom-scrollbar">
                        {[1, 2, 3, 4, 5].map((i) => (
                            <div key={i} className="flex items-center gap-4 p-4 rounded-xl hover:bg-white/5 transition-colors border border-white/5">
                                <div className="h-10 w-10 rounded-full bg-white/5 flex items-center justify-center">
                                    <Clock size={18} className="text-gray-400" />
                                </div>
                                <div className="flex-1">
                                    <p className="text-sm font-medium">Updated patient records for Sarah Miller</p>
                                    <p className="text-xs text-gray-500">2 hours ago</p>
                                </div>
                                <div className="px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-[10px] font-bold uppercase tracking-wider">
                                    Updates
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="glass-card flex flex-col">
                    <h3 className="text-xl font-bold mb-6">Quick Actions</h3>
                    <div className="space-y-3">
                        <QuickAction icon={Plus} label="New Admission" color="bg-blue-500" />
                        <QuickAction icon={Calendar} label="Book Appointment" color="bg-purple-500" />
                        <QuickAction icon={FileText} label="Create Report" color="bg-pink-500" />
                        <ActionToggle label="Email Notifications" active={true} />
                        <ActionToggle label="SMS Alerts" active={false} />
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ title, value, icon: Icon, trend, color = "text-indigo-400" }: any) {
    return (
        <div className="glass-card">
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-sm text-gray-500 font-medium mb-1 uppercase tracking-wider">{title}</p>
                    <h4 className="text-3xl font-bold">{value}</h4>
                </div>
                <div className={`p-3 rounded-xl bg-white/5 ${color}`}>
                    <Icon size={24} />
                </div>
            </div>
            <p className="text-xs text-gray-400 mt-4 flex items-center gap-1">
                <TrendingUp size={12} className="text-indigo-500" />
                {trend}
            </p>
        </div>
    );
}

function QuickAction({ icon: Icon, label, color }: any) {
    return (
        <button className="w-full flex items-center gap-3 p-4 rounded-xl border border-white/5 hover:bg-white/5 transition-all group">
            <div className={`p-2 rounded-lg ${color} bg-opacity-20 group-hover:scale-110 transition-transform`}>
                <Icon size={18} className={color.replace('bg-', 'text-')} />
            </div>
            <span className="font-medium text-gray-300">{label}</span>
        </button>
    );
}

function ActionToggle({ label, active }: any) {
    return (
        <div className="flex items-center justify-between p-4 rounded-xl border border-white/5">
            <span className="text-gray-400 text-sm font-medium">{label}</span>
            <div className={`w-10 h-6 rounded-full p-1 transition-colors ${active ? 'bg-indigo-500' : 'bg-gray-700'}`}>
                <div className={`w-4 h-4 rounded-full bg-white transition-transform ${active ? 'translate-x-4' : 'translate-x-0'}`}></div>
            </div>
        </div>
    );
}
