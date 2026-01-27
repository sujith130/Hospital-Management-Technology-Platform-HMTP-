export const navItems = {
  admin: [
    { label: 'Overview', path: '/dashboard', icon: '📊' },
    { label: 'Manage Users', path: '/dashboard/users', icon: '👥' },
    { label: 'System Settings', path: '/dashboard/settings', icon: '⚙️' },
    { label: 'Pharmacy', path: '/dashboard/inventory', icon: '📦' },
  ],
  doctor: [
    { label: 'My Schedule', path: '/dashboard/schedule', icon: '📅' },
    { label: 'Patients', path: '/dashboard/patients', icon: '🩺' },
    { label: 'Appointments', path: '/dashboard/appointments', icon: '📋' },
  ],
  patient: [
    { label: 'My Health', path: '/dashboard/overview', icon: '❤️' },
    { label: 'Prescriptions', path: '/dashboard/prescriptions', icon: '💊' },
    { label: 'Billing', path: '/dashboard/billing', icon: '💳' },
  ]
};