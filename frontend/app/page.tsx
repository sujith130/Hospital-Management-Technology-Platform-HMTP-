'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from '@/lib/auth_context';
import { ArrowRight, Heart, Users, Award, Clock, Stethoscope, Activity, Microscope, Pill, Ambulance, Star } from 'lucide-react';
import Image from 'next/image';

export default function Home() {
    const router = useRouter();
    const { user, isLoading } = useAuth();

    useEffect(() => {
        if (!isLoading && user) {
            router.push(`/dashboard/${user.role}`);
        }
    }, [user, isLoading, router]);

    const stats = [
        { number: '50K+', label: 'Patients Served', icon: Users },
        { number: '200+', label: 'Expert Doctors', icon: Stethoscope },
        { number: '15+', label: 'Departments', icon: Activity },
        { number: '25+', label: 'Years of Excellence', icon: Award },
    ];

    const services = [
        {
            icon: Ambulance,
            title: 'Emergency Care',
            description: '24/7 emergency services with state-of-the-art facilities and expert medical teams.',
        },
        {
            icon: Stethoscope,
            title: 'Outpatient Services',
            description: 'Comprehensive outpatient care across multiple specialties with minimal wait times.',
        },
        {
            icon: Activity,
            title: 'Advanced Surgery',
            description: 'Cutting-edge surgical procedures with experienced surgeons and modern technology.',
        },
        {
            icon: Microscope,
            title: 'Diagnostic Services',
            description: 'Complete diagnostic facilities including lab tests, imaging, and pathology services.',
        },
        {
            icon: Heart,
            title: 'Cardiology',
            description: 'Specialized cardiac care with advanced treatment options and preventive programs.',
        },
        {
            icon: Pill,
            title: 'Pharmacy',
            description: 'In-house pharmacy with all medications available at competitive prices.',
        },
    ];

    const departments = [
        { name: 'Cardiology', specialists: 25, color: 'from-red-500 to-pink-500' },
        { name: 'Neurology', specialists: 18, color: 'from-purple-500 to-indigo-500' },
        { name: 'Orthopedics', specialists: 22, color: 'from-blue-500 to-cyan-500' },
        { name: 'Pediatrics', specialists: 20, color: 'from-green-500 to-teal-500' },
        { name: 'Oncology', specialists: 15, color: 'from-orange-500 to-red-500' },
        { name: 'General Medicine', specialists: 30, color: 'from-teal-500 to-green-500' },
    ];

    const testimonials = [
        {
            name: 'Rajesh Kumar',
            text: 'Excellent care and professional staff. The doctors took time to explain everything clearly. Highly recommend!',
            rating: 5,
        },
        {
            name: 'Priya Sharma',
            text: 'The emergency department saved my father\'s life. Quick response and expert treatment. Forever grateful!',
            rating: 5,
        },
        {
            name: 'Amit Patel',
            text: 'Modern facilities and caring staff. The entire experience from booking to treatment was seamless.',
            rating: 5,
        },
    ];

    return (
        <div className="bg-white">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="container-custom">
                    <div className="grid lg:grid-cols-2 gap-12 items-center">
                        <div className="space-y-8 animate-fade-in-up">
                            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full border border-blue-200">
                                <Award className="text-blue-600" size={20} />
                                <span className="text-sm font-semibold text-gray-700">Trusted Healthcare Partner Since 1999</span>
                            </div>
                            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight">
                                Your Health, <span className="text-gradient-blue">Our Priority</span>
                            </h1>
                            <p className="text-xl text-gray-600 leading-relaxed">
                                Experience world-class healthcare with compassionate care, expert doctors, and state-of-the-art facilities.
                                Your well-being is our commitment.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-4">
                                <button
                                    onClick={() => router.push('/appointments')}
                                    className="btn-primary flex items-center justify-center gap-2 text-lg"
                                >
                                    Book Appointment
                                    <ArrowRight size={20} />
                                </button>
                                <button
                                    onClick={() => router.push('/doctors')}
                                    className="btn-secondary flex items-center justify-center gap-2 text-lg"
                                >
                                    Find a Doctor
                                </button>
                            </div>
                            <div className="flex items-center gap-6 pt-4">
                                <div className="trust-badge">
                                    <Award size={20} />
                                    <span>JCI Accredited</span>
                                </div>
                                <div className="trust-badge">
                                    <Award size={20} />
                                    <span>ISO Certified</span>
                                </div>
                            </div>
                        </div>
                        <div className="relative h-[500px] lg:h-[600px] animate-fade-in-up">
                            <div className="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-teal-400/20 rounded-3xl transform rotate-3"></div>
                            <div className="relative h-full bg-white rounded-3xl overflow-hidden shadow-2xl">
                                <Image
                                    src="/api/placeholder/600/700"
                                    alt="Modern Hospital Building"
                                    fill
                                    className="object-cover"
                                    priority
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="py-16 bg-white">
                <div className="container-custom">
                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
                        {stats.map((stat, index) => (
                            <div key={index} className="stat-card animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                                <div className="flex justify-center mb-4">
                                    <div className="icon-container">
                                        <stat.icon className="text-white" size={28} />
                                    </div>
                                </div>
                                <div className="stat-number">{stat.number}</div>
                                <div className="stat-label">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Services Section */}
            <section className="py-20 bg-gray-50">
                <div className="container-custom">
                    <div className="text-center mb-16">
                        <h2 className="section-title">Our Services</h2>
                        <p className="section-subtitle">
                            Comprehensive healthcare services designed to meet all your medical needs under one roof
                        </p>
                    </div>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {services.map((service, index) => (
                            <div key={index} className="service-card animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                                <div className="icon-container mb-6">
                                    <service.icon className="text-white" size={28} />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 mb-3">{service.title}</h3>
                                <p className="text-gray-600 leading-relaxed">{service.description}</p>
                            </div>
                        ))}
                    </div>
                    <div className="text-center mt-12">
                        <button onClick={() => router.push('/services')} className="btn-primary">
                            View All Services
                        </button>
                    </div>
                </div>
            </section>

            {/* Departments Section */}
            <section className="py-20 bg-white">
                <div className="container-custom">
                    <div className="text-center mb-16">
                        <h2 className="section-title">Our Departments</h2>
                        <p className="section-subtitle">
                            Specialized departments with expert doctors and advanced medical technology
                        </p>
                    </div>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {departments.map((dept, index) => (
                            <div
                                key={index}
                                className="department-card animate-fade-in-up"
                                style={{ animationDelay: `${index * 0.1}s` }}
                            >
                                <div className={`h-48 bg-gradient-to-br ${dept.color} flex items-center justify-center relative overflow-hidden`}>
                                    <div className="absolute inset-0 bg-black/20"></div>
                                    <div className="relative text-center text-white z-10">
                                        <h3 className="text-3xl font-bold mb-2">{dept.name}</h3>
                                        <p className="text-lg">{dept.specialists} Specialists</p>
                                    </div>
                                </div>
                                <div className="p-6 bg-white">
                                    <button
                                        onClick={() => router.push('/departments')}
                                        className="btn-outline w-full"
                                    >
                                        Learn More
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="py-20 bg-gradient-to-br from-blue-50 to-teal-50">
                <div className="container-custom">
                    <div className="text-center mb-16">
                        <h2 className="section-title">What Our Patients Say</h2>
                        <p className="section-subtitle">
                            Real experiences from real patients who trust us with their health
                        </p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-8">
                        {testimonials.map((testimonial, index) => (
                            <div key={index} className="testimonial-card animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                                <div className="flex gap-1 mb-4">
                                    {[...Array(testimonial.rating)].map((_, i) => (
                                        <Star key={i} className="text-yellow-400 fill-yellow-400" size={20} />
                                    ))}
                                </div>
                                <p className="text-gray-700 mb-6 italic leading-relaxed">"{testimonial.text}"</p>
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-teal-500 flex items-center justify-center text-white font-bold">
                                        {testimonial.name.charAt(0)}
                                    </div>
                                    <div>
                                        <p className="font-semibold text-gray-900">{testimonial.name}</p>
                                        <p className="text-sm text-gray-600">Verified Patient</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Emergency CTA Section */}
            <section className="py-16 bg-red-600">
                <div className="container-custom">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-8 text-white">
                        <div className="flex items-center gap-4">
                            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center animate-pulse-slow">
                                <Ambulance size={32} />
                            </div>
                            <div>
                                <h3 className="text-3xl font-bold mb-2">24/7 Emergency Services</h3>
                                <p className="text-red-100">We're here for you, anytime, anywhere</p>
                            </div>
                        </div>
                        <a href="tel:+911234567899" className="btn-emergency text-xl px-12 py-4 bg-white text-red-600 hover:bg-gray-100">
                            Call Emergency: +91 123 456 7899
                        </a>
                    </div>
                </div>
            </section>

            {/* Final CTA Section */}
            <section className="py-20 bg-gradient-to-br from-blue-600 to-teal-600 text-white">
                <div className="container-custom text-center">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Experience Better Healthcare?</h2>
                    <p className="text-xl mb-10 text-blue-100 max-w-2xl mx-auto">
                        Book your appointment today and take the first step towards a healthier tomorrow
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button
                            onClick={() => router.push('/appointments')}
                            className="px-12 py-4 bg-white text-blue-600 rounded-full font-bold text-lg hover:bg-gray-100 transition-all duration-300 active:scale-95 shadow-lg"
                        >
                            Book Appointment Now
                        </button>
                        <button
                            onClick={() => router.push('/contact')}
                            className="px-12 py-4 border-2 border-white text-white rounded-full font-bold text-lg hover:bg-white hover:text-blue-600 transition-all duration-300 active:scale-95"
                        >
                            Contact Us
                        </button>
                    </div>
                </div>
            </section>
        </div>
    );
}
