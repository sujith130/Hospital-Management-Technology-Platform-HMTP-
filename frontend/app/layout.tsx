import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "HMTP - Hospital Management",
    description: "Enterprise Hospital Management Platform",
};

import { AuthProvider } from "@/lib/auth_context";

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className="bg-animate">
                <AuthProvider>
                    {children}
                </AuthProvider>
            </body>
        </html>
    );
}
