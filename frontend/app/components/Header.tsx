'use client';

import Link from 'next/link';
import { useState } from 'react';
import { Menu, X, Phone, User } from 'lucide-react';

export default function Header() {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const navigation = [
        { name: 'Home', href: '/' },
        { name: 'Services', href: '/services' },
        { name: 'Departments', href: '/departments' },
        { name: 'Find a Doctor', href: '/doctors' },
        { name: 'Book Appointment', href: '/appointments' },
        { name: 'Contact', href: '/contact' },
    ];

    return (
        <header className="bg-white shadow-md sticky top-0 z-50">
            <nav className="container-custom">
                <div className="flex items-center justify-between h-20">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-3">
                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                            <span className="text-white font-bold text-xl">H</span>
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">HMTP</h1>
                            <p className="text-xs text-gray-600">Healthcare Excellence</p>
                        </div>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden lg:flex items-center space-x-8">
                        {navigation.map((item) => (
                            <Link
                                key={item.name}
                                href={item.href}
                                className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200"
                            >
                                {item.name}
                            </Link>
                        ))}
                    </div>

                    {/* Right Side Actions */}
                    <div className="hidden lg:flex items-center space-x-4">
                        <a href="tel:+911234567890" className="flex items-center gap-2 text-red-600 font-semibold hover:text-red-700">
                            <Phone size={18} />
                            <span>Emergency</span>
                        </a>
                        <button className="btn-secondary hidden lg:flex items-center gap-2">
                            <a href="/login" className="flex items-center gap-2">
                                <User size={18} />
                                Patient Login
                            </a>
                        </button>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="lg:hidden p-2 rounded-lg hover:bg-gray-100"
                    >
                        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>
                </div>

                {/* Mobile Menu */}
                {mobileMenuOpen && (
                    <div className="lg:hidden py-4 border-t border-gray-200">
                        <div className="flex flex-col space-y-4">
                            {navigation.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200 py-2"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    {item.name}
                                </Link>
                            ))}
                            <div className="pt-4 border-t border-gray-200 space-y-3">
                                <a href="tel:+911234567890" className="flex items-center gap-2 text-red-600 font-semibold">
                                    <Phone size={18} />
                                    <span>Emergency</span>
                                </a>
                                <Link href="/login" className="btn-secondary flex items-center gap-2 justify-center">
                                    <User size={18} />
                                    <span>Patient Login</span>
                                </Link>
                            </div>
                        </div>
                    </div>
                )}
            </nav>
        </header>
    );
}
