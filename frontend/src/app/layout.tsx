import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TodoMovil Agente — Copiloto del Vendedor",
  description: "Asistente de ventas con RAG, semáforo y certeza para TodoMovil",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
