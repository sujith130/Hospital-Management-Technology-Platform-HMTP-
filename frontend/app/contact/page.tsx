'use client';

import { useState } from 'react';
import { Search, MapPin, Phone, Mail, Clock, Send } from 'lucide-react';

export default function ContactPage() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: '',
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        alert('Thank you for contacting us! We will get back to you soon.');
        setFormData({ name: '', email: '', phone: '', subject: '', message: '' });
    };

    return (
        <div className="bg-white">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-blue-600 to-teal-600 text-white py-20">
                <div className="container-custom text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Contact Us</h1>
                    <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                        We're here to help. Reach out to us for any queries, appointments, or emergency assistance
                    </p>
                </div>
            </section>

            {/* Contact Info & Form */}
            <section className="py-20">
                <div className="container-custom">
                    <div className="grid lg:grid-cols-2 gap-12">
                        {/* Contact Information */}
                        <div>
                            <h2 className="text-3xl font-bold text-gray-900 mb-8">Get in Touch</h2>
                            <div className="space-y-6">
                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                        <MapPin className="text-blue-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-900 mb-1">Address</h3>
                                        <p className="text-gray-600">123 Healthcare Avenue<br />Medical District, City - 500001</p>
                                    </div>
                                </div>

                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                        <Phone className="text-blue-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-900 mb-1">Phone</h3>
                                        <p className="text-gray-600">
                                            General: <a href="tel:+911234567890" className="text-blue-600 hover:underline">+91 123 456 7890</a><br />
                                            Emergency: <a href="tel:+911234567899" className="text-red-600 hover:underline font-semibold">+91 123 456 7899</a>
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                        <Mail className="text-blue-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-900 mb-1">Email</h3>
                                        <p className="text-gray-600">
                                            General: <a href="mailto:info@hmtp.com" className="text-blue-600 hover:underline">info@hmtp.com</a><br />
                                            Appointments: <a href="mailto:appointments@hmtp.com" className="text-blue-600 hover:underline">appointments@hmtp.com</a>
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-start gap-4">
                                    <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                                        <Clock className="text-blue-600" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-gray-900 mb-1">Working Hours</h3>
                                        <p className="text-gray-600">
                                            Mon - Sat: 8:00 AM - 8:00 PM<br />
                                            Sunday: 9:00 AM - 5:00 PM<br />
                                            <span className="text-green-600 font-semibold">Emergency: 24/7</span>
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Map Placeholder */}
                            <div className="mt-8 bg-gray-200 rounded-xl h-64 flex items-center justify-center">
                                <p className="text-gray-600">Map Integration Placeholder</p>
                            </div>
                        </div>

                        {/* Contact Form */}
                        <div className="medical-card">
                            <h2 className="text-3xl font-bold text-gray-900 mb-6">Send us a Message</h2>
                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div>
                                    <label className="label-medical">Full Name</label>
                                    <input
                                        type="text"
                                        required
                                        className="input-medical"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        placeholder="Enter your full name"
                                    />
                                </div>

                                <div>
                                    <label className="label-medical">Email Address</label>
                                    <input
                                        type="email"
                                        required
                                        className="input-medical"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                        placeholder="your.email@example.com"
                                    />
                                </div>

                                <div>
                                    <label className="label-medical">Phone Number</label>
                                    <input
                                        type="tel"
                                        required
                                        className="input-medical"
                                        value={formData.phone}
                                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                        placeholder="+91 1234567890"
                                    />
                                </div>

                                <div>
                                    <label className="label-medical">Subject</label>
                                    <input
                                        type="text"
                                        required
                                        className="input-medical"
                                        value={formData.subject}
                                        onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                                        placeholder="How can we help you?"
                                    />
                                </div>

                                <div>
                                    <label className="label-medical">Message</label>
                                    <textarea
                                        required
                                        rows={5}
                                        className="textarea-medical"
                                        value={formData.message}
                                        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                                        placeholder="Tell us more about your inquiry..."
                                    />
                                </div>

                                <button type="submit" className="btn-primary w-full flex items-center justify-center gap-2">
                                    <Send size={20} />
                                    Send Message
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </section>

            {/* Emergency Banner */}
            <section className="py-12 bg-red-600 text-white">
                <div className="container-custom text-center">
                    <h3 className="text-3xl font-bold mb-4">Medical Emergency?</h3>
                    <p className="text-xl mb-6">Call our 24/7 emergency hotline immediately</p>
                    <a href="tel:+911234567899" className="btn-emergency text-xl px-12 py-4 bg-white text-red-600 hover:bg-gray-100">
                        Emergency: +91 123 456 7899
                    </a>
                </div>
            </section>
        </div>
    );
}
