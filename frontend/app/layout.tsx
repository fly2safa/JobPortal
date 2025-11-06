import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TalentNest - Find Your Dream Job",
  description: "Connect job seekers with top employers. Powered by AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

