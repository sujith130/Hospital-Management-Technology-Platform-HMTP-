import Link from 'next/link';
import { Phone, Mail, MapPin, Clock, Facebook, Twitter, Linkedin, Instagram } from 'lucide-react';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    const departments = [
        'Cardiology',
        'Neurology',
        'Orthopedics',
        'Pediatrics',
        'Oncology',
        'Emergency Care',
    ];

    const quickLinks = [
        { name: 'About Us', href: '/about' },
        { name: 'Services', href: '/services' },
        { name: 'Find a Doctor', href: '/doctors' },
        { name: 'Book Appointment', href: '/appointments' },
        { name: 'Contact Us', href: '/contact' },
        { name: 'Careers', href: '/careers' },
    ];

    return (
        <footer className="bg-gray-900 text-gray-300">
            {/* Main Footer */}
            <div className="container-custom py-16">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
                    {/* About Section */}
                    <div>
                        <div className="flex items-center space-x-3 mb-6">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                                <span className="text-white font-bold text-xl">H</span>
                            </div>
                            <div>
                                <h3 className="text-xl font-bold text-white">HMTP</h3>
                                <p className="text-xs text-gray-400">Healthcare Excellence</p>
                            </div>
                        </div>
                        <p className="text-gray-400 mb-6">
                            Providing world-class healthcare services with compassion, expertise, and cutting-edge technology.
                        </p>
                        <div className="flex space-x-4">
                            <a href="#" className="w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 flex items-center justify-center transition-colors">
                                <Facebook size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 flex items-center justify-center transition-colors">
                                <Twitter size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 flex items-center justify-center transition-colors">
                                <Linkedin size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-gray-800 hover:bg-blue-600 flex items-center justify-center transition-colors">
                                <Instagram size={18} />
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="text-lg font-bold text-white mb-6">Quick Links</h4>
                        <ul className="space-y-3">
                            {quickLinks.map((link) => (
                                <li key={link.name}>
                                    <Link href={link.href} className="hover:text-blue-400 transition-colors">
                                        {link.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Departments */}
                    <div>
                        <h4 className="text-lg font-bold text-white mb-6">Departments</h4>
                        <ul className="space-y-3">
                            {departments.map((dept) => (
                                <li key={dept}>
                                    <Link href="/departments" className="hover:text-blue-400 transition-colors">
                                        {dept}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Contact Info */}
                    <div>
                        <h4 className="text-lg font-bold text-white mb-6">Contact Us</h4>
                        <ul className="space-y-4">
                            <li className="flex items-start gap-3">
                                <MapPin size={20} className="text-blue-400 mt-1 flex-shrink-0" />
                                <span>123 Healthcare Avenue, Medical District, City - 500001</span>
                            </li>
                            <li className="flex items-center gap-3">
                                <Phone size={20} className="text-blue-400 flex-shrink-0" />
                                <div>
                                    <a href="tel:+911234567890" className="hover:text-blue-400">+91 123 456 7890</a>
                                    <p className="text-sm text-gray-500">General Inquiries</p>
                                </div>
                            </li>
                            <li className="flex items-center gap-3">
                                <Phone size={20} className="text-red-400 flex-shrink-0" />
                                <div>
                                    <a href="tel:+911234567899" className="hover:text-red-400 font-semibold">+91 123 456 7899</a>
                                    <p className="text-sm text-red-500">Emergency 24/7</p>
                                </div>
                            </li>
                            <li className="flex items-center gap-3">
                                <Mail size={20} className="text-blue-400 flex-shrink-0" />
                                <a href="mailto:info@hmtp.com" className="hover:text-blue-400">info@hmtp.com</a>
                            </li>
                            <li className="flex items-start gap-3">
                                <Clock size={20} className="text-blue-400 mt-1 flex-shrink-0" />
                                <div>
                                    <p>Mon - Sat: 8:00 AM - 8:00 PM</p>
                                    <p>Sunday: 9:00 AM - 5:00 PM</p>
                                    <p className="text-green-400 font-semibold">Emergency: 24/7</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            {/* Bottom Bar */}
            <div className="border-t border-gray-800">
                <div className="container-custom py-6">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <p className="text-sm text-gray-500">
                            © {currentYear} HMTP. All rights reserved.
                        </p>
                        <div className="flex gap-6 text-sm">
                            <Link href="/privacy" className="hover:text-blue-400 transition-colors">
                                Privacy Policy
                            </Link>
                            <Link href="/terms" className="hover:text-blue-400 transition-colors">
                                Terms of Service
                            </Link>
                            <Link href="/disclaimer" className="hover:text-blue-400 transition-colors">
                                Medical Disclaimer
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
}
