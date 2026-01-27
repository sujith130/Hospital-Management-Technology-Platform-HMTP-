const API_URL = 'http://127.0.0.1:8000/api/v1';

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    const headers = new Headers(options.headers);
    if (token) {
        headers.set('Authorization', `Bearer ${token}`);
    }
    if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
        headers.set('Content-Type', 'application/json');
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(errorData.detail || response.statusText);
    }

    return response.json();
}

export const authApi = {
    login: (formData: FormData) =>
        apiRequest('/auth/login', {
            method: 'POST',
            body: formData, // OAuth2PasswordRequestForm expects form data
        }),
    register: (userData: any) =>
        apiRequest('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData),
        }),
};
