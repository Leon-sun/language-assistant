import type { Metadata } from "next";
import "./globals.css";
import { LanguageProvider } from "@/contexts/language-context";
import { Navbar } from "@/components/layout/navbar";
import { Sidebar } from "@/components/layout/sidebar";
import { Footer } from "@/components/layout/footer";

export const metadata: Metadata = {
  title: "Dictionary Project",
  description: "French-English dictionary powered by Django and Google Gemini AI.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-zinc-900 font-sans text-zinc-100 antialiased">
        <LanguageProvider>
          <Navbar />
          <main className="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-[280px_1fr] lg:gap-8">
              <div className="hidden lg:block">
                <Sidebar />
              </div>
              <section className="min-w-0">
                {children}
              </section>
            </div>
          </main>
          <Footer />
        </LanguageProvider>
      </body>
    </html>
  );
}
