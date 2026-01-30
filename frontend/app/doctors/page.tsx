'use client';

import { useState } from 'react';
import { Search, Filter } from 'lucide-react';

export default function DoctorsPage() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedSpecialty, setSelectedSpecialty] = useState('all');

    const doctors = [
        { id: 1, name: 'Dr. Rajesh Kumar', specialty: 'Cardiology', qualification: 'MD, DM (Cardiology)', experience: '15 years', available: true },
        { id: 2, name: 'Dr. Priya Sharma', specialty: 'Neurology', qualification: 'MD, DM (Neurology)', experience: '12 years', available: true },
        { id: 3, name: 'Dr. Amit Patel', specialty: 'Orthopedics', qualification: 'MS (Ortho)', experience: '18 years', available: false },
        { id: 4, name: 'Dr. Sunita Reddy', specialty: 'Pediatrics', qualification: 'MD (Pediatrics)', experience: '10 years', available: true },
        { id: 5, name: 'Dr. Vikram Singh', specialty: 'Oncology', qualification: 'MD, DM (Oncology)', experience: '14 years', available: true },
        { id: 6, name: 'Dr. Anjali Mehta', specialty: 'Cardiology', qualification: 'MD, DM (Cardiology)', experience: '11 years', available: true },
        { id: 7, name: 'Dr. Rahul Verma', specialty: 'Neurology', qualification: 'MD, DM (Neurology)', experience: '9 years', available: false },
        { id: 8, name: 'Dr. Kavita Joshi', specialty: 'Orthopedics', qualification: 'MS (Ortho)', experience: '16 years', available: true },
    ];

    const specialties = ['all', 'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology'];

    const filteredDoctors = doctors.filter(doctor => {
        const matchesSearch = doctor.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            doctor.specialty.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesSpecialty = selectedSpecialty === 'all' || doctor.specialty === selectedSpecialty;
        return matchesSearch && matchesSpecialty;
    });

    return (
        <div className="bg-white">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-blue-600 to-teal-600 text-white py-20">
                <div className="container-custom text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Find a Doctor</h1>
                    <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                        Search from our team of expert doctors and specialists
                    </p>
                </div>
            </section>

            {/* Search & Filter */}
            <section className="py-12 bg-gray-50">
                <div className="container-custom">
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1 relative">
                            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                            <input
                                type="text"
                                placeholder="Search by doctor name or specialty..."
                                className="input-medical pl-12"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                        <div className="md:w-64 relative">
                            <Filter className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                            <select
                                className="select-medical pl-12"
                                value={selectedSpecialty}
                                onChange={(e) => setSelectedSpecialty(e.target.value)}
                            >
                                {specialties.map(specialty => (
                                    <option key={specialty} value={specialty}>
                                        {specialty === 'all' ? 'All Specialties' : specialty}
                                    </option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>
            </section>

            {/* Doctors Grid */}
            <section className="py-12">
                <div className="container-custom">
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {filteredDoctors.map((doctor) => (
                            <div key={doctor.id} className="doctor-card">
                                <div className="h-48 bg-gradient-to-br from-blue-500 to-teal-500 flex items-center justify-center">
                                    <div className="w-24 h-24 rounded-full bg-white flex items-center justify-center text-4xl font-bold text-blue-600">
                                        {doctor.name.split(' ')[1].charAt(0)}
                                    </div>
                                </div>
                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-gray-900 mb-1">{doctor.name}</h3>
                                    <p className="text-blue-600 font-semibold mb-2">{doctor.specialty}</p>
                                    <p className="text-sm text-gray-600 mb-1">{doctor.qualification}</p>
                                    <p className="text-sm text-gray-600 mb-4">{doctor.experience} experience</p>
                                    <div className="flex items-center gap-2 mb-4">
                                        <div className={`w-2 h-2 rounded-full ${doctor.available ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                                        <span className={`text-sm font-medium ${doctor.available ? 'text-green-600' : 'text-gray-500'}`}>
                                            {doctor.available ? 'Available' : 'Not Available'}
                                        </span>
                                    </div>
                                    <a href="/appointments" className="btn-primary w-full text-center">
                                        Book Appointment
                                    </a>
                                </div>
                            </div>
                        ))}
                    </div>

                    {filteredDoctors.length === 0 && (
                        <div className="text-center py-12">
                            <p className="text-xl text-gray-600">No doctors found matching your criteria</p>
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
}
