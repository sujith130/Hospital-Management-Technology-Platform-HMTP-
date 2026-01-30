import { Heart, Brain, Bone, Baby, Eye, Ear, Lungs, Kidney, Users, ArrowRight } from 'lucide-react';

export default function DepartmentsPage() {
    const departments = [
        {
            icon: Heart,
            name: 'Cardiology',
            description: 'Comprehensive cardiac care with advanced diagnostic and treatment facilities for all heart conditions.',
            specialists: 25,
            services: ['ECG/Echo', 'Angiography', 'Cardiac Surgery', 'Pacemaker'],
            color: 'from-red-500 to-pink-500',
        },
        {
            icon: Brain,
            name: 'Neurology',
            description: 'Expert neurological care for brain, spine, and nervous system disorders with state-of-the-art technology.',
            specialists: 18,
            services: ['Neuro Diagnostics', 'Brain Surgery', 'Stroke Care', 'Epilepsy Treatment'],
            color: 'from-purple-500 to-indigo-500',
        },
        {
            icon: Bone,
            name: 'Orthopedics',
            description: 'Complete bone and joint care including trauma management, joint replacement, and sports medicine.',
            specialists: 22,
            services: ['Joint Replacement', 'Arthroscopy', 'Fracture Care', 'Physiotherapy'],
            color: 'from-blue-500 to-cyan-500',
        },
        {
            icon: Baby,
            name: 'Pediatrics',
            description: 'Specialized care for infants, children, and adolescents with experienced pediatricians and NICU facilities.',
            specialists: 20,
            services: ['Newborn Care', 'NICU', 'Vaccination', 'Child Development'],
            color: 'from-green-500 to-teal-500',
        },
        {
            icon: Users,
            name: 'Oncology',
            description: 'Comprehensive cancer care with advanced treatment options including chemotherapy and radiation therapy.',
            specialists: 15,
            services: ['Chemotherapy', 'Radiation', 'Surgical Oncology', 'Palliative Care'],
            color: 'from-orange-500 to-red-500',
        },
        {
            icon: Eye,
            name: 'Ophthalmology',
            description: 'Complete eye care services including cataract surgery, LASIK, and treatment for all eye conditions.',
            specialists: 12,
            services: ['Cataract Surgery', 'LASIK', 'Retina Care', 'Glaucoma Treatment'],
            color: 'from-teal-500 to-green-500',
        },
        {
            icon: Ear,
            name: 'ENT',
            description: 'Expert care for ear, nose, and throat conditions with advanced diagnostic and surgical facilities.',
            specialists: 10,
            services: ['Hearing Tests', 'Sinus Surgery', 'Tonsillectomy', 'Voice Disorders'],
            color: 'from-yellow-500 to-orange-500',
        },
        {
            icon: Lungs,
            name: 'Pulmonology',
            description: 'Specialized respiratory care for lung diseases, asthma, and breathing disorders.',
            specialists: 14,
            services: ['Pulmonary Function Tests', 'Bronchoscopy', 'Sleep Studies', 'Asthma Care'],
            color: 'from-cyan-500 to-blue-500',
        },
        {
            icon: Kidney,
            name: 'Nephrology',
            description: 'Comprehensive kidney care including dialysis, kidney transplant, and management of renal diseases.',
            specialists: 16,
            services: ['Dialysis', 'Kidney Transplant', 'Renal Care', 'Hypertension Management'],
            color: 'from-indigo-500 to-purple-500',
        },
    ];

    return (
        <div className="bg-white">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-blue-600 to-teal-600 text-white py-20">
                <div className="container-custom text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Our Departments</h1>
                    <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                        Specialized medical departments with expert doctors and advanced technology to serve all your healthcare needs
                    </p>
                </div>
            </section>

            {/* Departments Grid */}
            <section className="py-20">
                <div className="container-custom">
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {departments.map((dept, index) => (
                            <div key={index} className="department-card">
                                <div className={`h-48 bg-gradient-to-br ${dept.color} flex items-center justify-center relative overflow-hidden`}>
                                    <div className="absolute inset-0 bg-black/20"></div>
                                    <div className="relative z-10">
                                        <dept.icon className="text-white mx-auto mb-4" size={48} />
                                        <h3 className="text-3xl font-bold text-white text-center">{dept.name}</h3>
                                    </div>
                                </div>
                                <div className="p-6 bg-white">
                                    <div className="flex items-center gap-2 mb-4">
                                        <Users size={18} className="text-blue-600" />
                                        <span className="text-sm font-semibold text-gray-700">{dept.specialists} Specialists</span>
                                    </div>
                                    <p className="text-gray-600 mb-4 leading-relaxed">{dept.description}</p>
                                    <div className="border-t border-gray-200 pt-4 mt-4">
                                        <h4 className="font-semibold text-gray-900 mb-2">Services Offered:</h4>
                                        <ul className="space-y-2 mb-4">
                                            {dept.services.map((service, idx) => (
                                                <li key={idx} className="flex items-center gap-2 text-gray-700 text-sm">
                                                    <div className="w-1.5 h-1.5 rounded-full bg-blue-600"></div>
                                                    {service}
                                                </li>
                                            ))}
                                        </ul>
                                        <a href="/doctors" className="btn-outline w-full flex items-center justify-center gap-2">
                                            View Doctors
                                            <ArrowRight size={16} />
                                        </a>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-16 bg-gradient-to-br from-blue-50 to-teal-50">
                <div className="container-custom text-center">
                    <h2 className="text-4xl font-bold text-gray-900 mb-6">Find the Right Specialist</h2>
                    <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                        Our team of expert specialists is here to provide you with the best possible care
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="/doctors" className="btn-primary">
                            Find a Doctor
                        </a>
                        <a href="/appointments" className="btn-secondary">
                            Book Appointment
                        </a>
                    </div>
                </div>
            </section>
        </div>
    );
}
