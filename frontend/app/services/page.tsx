import { Ambulance, Stethoscope, Activity, Microscope, Heart, Pill, Syringe, Baby, Brain, Bone } from 'lucide-react';

export default function ServicesPage() {
    const services = [
        {
            icon: Ambulance,
            title: '24/7 Emergency Care',
            description: 'Round-the-clock emergency services with state-of-the-art trauma care, advanced life support, and rapid response teams ready to handle any medical emergency.',
            features: ['Trauma Center', 'ICU/CCU', 'Ambulance Service', 'Emergency Surgery'],
        },
        {
            icon: Stethoscope,
            title: 'Outpatient Department (OPD)',
            description: 'Comprehensive outpatient consultations across all specialties with minimal wait times and expert medical professionals.',
            features: ['General Medicine', 'Specialist Consultations', 'Health Checkups', 'Follow-up Care'],
        },
        {
            icon: Activity,
            title: 'Advanced Surgery',
            description: 'State-of-the-art surgical facilities with experienced surgeons performing minimally invasive and complex procedures.',
            features: ['Laparoscopic Surgery', 'Robotic Surgery', 'Day Care Surgery', 'Post-op Care'],
        },
        {
            icon: Microscope,
            title: 'Diagnostic Services',
            description: 'Complete diagnostic facilities with latest technology for accurate and timely test results.',
            features: ['Pathology Lab', 'Radiology', 'CT/MRI Scans', 'Ultrasound'],
        },
        {
            icon: Heart,
            title: 'Cardiology',
            description: 'Comprehensive cardiac care including preventive cardiology, interventional procedures, and cardiac rehabilitation.',
            features: ['ECG/Echo', 'Angiography', 'Cardiac Surgery', 'Pacemaker Implantation'],
        },
        {
            icon: Pill,
            title: 'In-House Pharmacy',
            description: 'Fully stocked pharmacy with all medications available at competitive prices, open 24/7 for your convenience.',
            features: ['Prescription Medicines', 'OTC Products', 'Home Delivery', '24/7 Availability'],
        },
        {
            icon: Syringe,
            title: 'Vaccination Services',
            description: 'Complete immunization services for all age groups including routine vaccinations and travel vaccines.',
            features: ['Child Immunization', 'Adult Vaccines', 'Travel Vaccines', 'Corporate Packages'],
        },
        {
            icon: Baby,
            title: 'Maternity & Childcare',
            description: 'Comprehensive maternity services and pediatric care with experienced obstetricians and pediatricians.',
            features: ['Prenatal Care', 'Normal & C-Section Delivery', 'NICU', 'Pediatric Care'],
        },
        {
            icon: Brain,
            title: 'Neurology & Neurosurgery',
            description: 'Advanced neurological care and neurosurgical procedures for brain and spine conditions.',
            features: ['Neuro Diagnostics', 'Brain Surgery', 'Spine Surgery', 'Stroke Care'],
        },
        {
            icon: Bone,
            title: 'Orthopedics',
            description: 'Complete orthopedic care including joint replacement, sports medicine, and trauma management.',
            features: ['Joint Replacement', 'Arthroscopy', 'Fracture Management', 'Physiotherapy'],
        },
    ];

    return (
        <div className="bg-white">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-blue-600 to-teal-600 text-white py-20">
                <div className="container-custom text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">Our Services</h1>
                    <p className="text-xl text-blue-100 max-w-3xl mx-auto">
                        Comprehensive healthcare services delivered with excellence, compassion, and cutting-edge technology
                    </p>
                </div>
            </section>

            {/* Services Grid */}
            <section className="py-20">
                <div className="container-custom">
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {services.map((service, index) => (
                            <div key={index} className="medical-card-hover">
                                <div className="icon-container mb-6">
                                    <service.icon className="text-white" size={28} />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 mb-3">{service.title}</h3>
                                <p className="text-gray-600 mb-4 leading-relaxed">{service.description}</p>
                                <div className="border-t border-gray-200 pt-4 mt-4">
                                    <h4 className="font-semibold text-gray-900 mb-2">Key Features:</h4>
                                    <ul className="space-y-2">
                                        {service.features.map((feature, idx) => (
                                            <li key={idx} className="flex items-center gap-2 text-gray-700">
                                                <div className="w-1.5 h-1.5 rounded-full bg-blue-600"></div>
                                                {feature}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-16 bg-gray-50">
                <div className="container-custom text-center">
                    <h2 className="text-4xl font-bold text-gray-900 mb-6">Need Medical Assistance?</h2>
                    <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                        Our team of expert doctors and medical professionals is ready to serve you
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="/appointments" className="btn-primary">
                            Book Appointment
                        </a>
                        <a href="/contact" className="btn-secondary">
                            Contact Us
                        </a>
                    </div>
                </div>
            </section>
        </div>
    );
}
