'use client';

import { useState } from 'react';
import { Calendar, User, Stethoscope, FileText, CheckCircle } from 'lucide-react';

export default function AppointmentsPage() {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        patientName: '',
        phone: '',
        email: '',
        department: '',
        doctor: '',
        date: '',
        time: '',
        reason: '',
    });

    const departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology'];
    const timeSlots = ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM'];

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (step < 3) {
            setStep(step + 1);
        } else {
            alert('Appointment booked successfully!');
            setStep(4);
        }
    };

    return (
        <div className="bg-white min-h-screen">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-blue-600 to-teal-600 text-white py-20">
                <div className="container-custom text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Book an Appointment</h1>
                    <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                        Schedule your consultation with our expert doctors in just a few simple steps
                    </p>
                </div>
            </section>

            {/* Appointment Form */}
            <section className="py-20">
                <div className="container-custom max-w-3xl">
                    {/* Progress Steps */}
                    <div className="flex justify-between mb-12">
                        {[1, 2, 3].map((s) => (
                            <div key={s} className="flex items-center flex-1">
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step >= s ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-600'
                                    }`}>
                                    {s}
                                </div>
                                {s < 3 && <div className={`flex-1 h-1 mx-2 ${step > s ? 'bg-blue-600' : 'bg-gray-200'}`}></div>}
                            </div>
                        ))}
                    </div>

                    {step < 4 ? (
                        <div className="medical-card">
                            <h2 className="text-3xl font-bold text-gray-900 mb-6">
                                {step === 1 && 'Personal Information'}
                                {step === 2 && 'Select Doctor & Date'}
                                {step === 3 && 'Appointment Details'}
                            </h2>

                            <form onSubmit={handleSubmit} className="space-y-6">
                                {step === 1 && (
                                    <>
                                        <div>
                                            <label className="label-medical">Full Name</label>
                                            <input
                                                type="text"
                                                required
                                                className="input-medical"
                                                value={formData.patientName}
                                                onChange={(e) => setFormData({ ...formData, patientName: e.target.value })}
                                                placeholder="Enter your full name"
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
                                    </>
                                )}

                                {step === 2 && (
                                    <>
                                        <div>
                                            <label className="label-medical">Department</label>
                                            <select
                                                required
                                                className="select-medical"
                                                value={formData.department}
                                                onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                                            >
                                                <option value="">Select Department</option>
                                                {departments.map(dept => (
                                                    <option key={dept} value={dept}>{dept}</option>
                                                ))}
                                            </select>
                                        </div>
                                        <div>
                                            <label className="label-medical">Preferred Date</label>
                                            <input
                                                type="date"
                                                required
                                                className="input-medical"
                                                value={formData.date}
                                                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                                                min={new Date().toISOString().split('T')[0]}
                                            />
                                        </div>
                                        <div>
                                            <label className="label-medical">Preferred Time</label>
                                            <select
                                                required
                                                className="select-medical"
                                                value={formData.time}
                                                onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                                            >
                                                <option value="">Select Time Slot</option>
                                                {timeSlots.map(time => (
                                                    <option key={time} value={time}>{time}</option>
                                                ))}
                                            </select>
                                        </div>
                                    </>
                                )}

                                {step === 3 && (
                                    <>
                                        <div>
                                            <label className="label-medical">Reason for Visit</label>
                                            <textarea
                                                required
                                                rows={5}
                                                className="textarea-medical"
                                                value={formData.reason}
                                                onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                                                placeholder="Please describe your symptoms or reason for consultation..."
                                            />
                                        </div>
                                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                                            <h3 className="font-semibold text-gray-900 mb-4">Appointment Summary</h3>
                                            <div className="space-y-2 text-sm">
                                                <p><span className="font-semibold">Name:</span> {formData.patientName}</p>
                                                <p><span className="font-semibold">Phone:</span> {formData.phone}</p>
                                                <p><span className="font-semibold">Email:</span> {formData.email}</p>
                                                <p><span className="font-semibold">Department:</span> {formData.department}</p>
                                                <p><span className="font-semibold">Date:</span> {formData.date}</p>
                                                <p><span className="font-semibold">Time:</span> {formData.time}</p>
                                            </div>
                                        </div>
                                    </>
                                )}

                                <div className="flex gap-4">
                                    {step > 1 && (
                                        <button
                                            type="button"
                                            onClick={() => setStep(step - 1)}
                                            className="btn-secondary flex-1"
                                        >
                                            Previous
                                        </button>
                                    )}
                                    <button type="submit" className="btn-primary flex-1">
                                        {step === 3 ? 'Confirm Appointment' : 'Next'}
                                    </button>
                                </div>
                            </form>
                        </div>
                    ) : (
                        <div className="medical-card text-center">
                            <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
                                <CheckCircle className="text-green-600" size={48} />
                            </div>
                            <h2 className="text-3xl font-bold text-gray-900 mb-4">Appointment Confirmed!</h2>
                            <p className="text-xl text-gray-600 mb-8">
                                Your appointment has been successfully booked. We've sent a confirmation email to {formData.email}
                            </p>
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
                                <h3 className="font-semibold text-gray-900 mb-4">Appointment Details</h3>
                                <div className="space-y-2">
                                    <p><span className="font-semibold">Department:</span> {formData.department}</p>
                                    <p><span className="font-semibold">Date:</span> {formData.date}</p>
                                    <p><span className="font-semibold">Time:</span> {formData.time}</p>
                                </div>
                            </div>
                            <a href="/" className="btn-primary">
                                Back to Home
                            </a>
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
}
