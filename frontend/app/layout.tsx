import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "./components/Header";
import Footer from "./components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "HMTP - Hospital Management Technology Platform",
    description: "World-class healthcare services with compassion, expertise, and cutting-edge technology. Book appointments, find doctors, and access comprehensive medical care.",
    keywords: "hospital, healthcare, medical services, doctors, appointments, emergency care",
};

import { AuthProvider } from "@/lib/auth_context";

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <AuthProvider>
                    <Header />
                    <main className="min-h-screen">
                        {children}
                    </main>
                    <Footer />
                </AuthProvider>
            </body>
        </html>
    );
}
