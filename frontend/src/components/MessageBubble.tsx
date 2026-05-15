"use client";

import SemaforoBadge from "./SemaforoBadge";
import CertaintyIndicator from "./CertaintyIndicator";

interface Fuente {
  tipo_fuente: string;
  producto: string;
  sistema?: string;
  marca?: string;
  modelo?: string;
  url?: string;
  certezza: string;
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  semaforo?: {
    color: string;
    motivo: string;
    detalle?: string;
  };
  certeza?: string;
  fuentes?: Fuente[];
  productos?: string[];
  capa?: string;
  timestamp: Date;
}

interface Props {
  message: Message;
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`msg-bubble ${isUser ? "msg-user" : "msg-assistant"}`}>
        {/* ── Contenido principal ──────────────── */}
        <p className="whitespace-pre-wrap">{message.content}</p>

        {/* ── Metadatos (solo assistant) ────────── */}
        {!isUser && message.semaforo && (
          <div className="mt-3 pt-3 border-t border-tm-border/50 space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <SemaforoBadge color={message.semaforo.color} />
              {message.certeza && (
                <CertaintyIndicator level={message.certeza} />
              )}
              {message.capa && (
                <span className="text-[10px] text-tm-muted bg-tm-bg px-2 py-0.5 rounded">
                  Capa: {message.capa}
                </span>
              )}
            </div>

            {message.semaforo.motivo && (
              <p className="text-xs text-tm-muted">
                {message.semaforo.motivo}
              </p>
            )}

            {message.semaforo.detalle && (
              <p className="text-xs text-tm-muted/70">
                {message.semaforo.detalle}
              </p>
            )}
          </div>
        )}

        {/* ── Fuentes ──────────────────────────── */}
        {!isUser && message.fuentes && message.fuentes.length > 0 && (
          <div className="mt-2 pt-2 border-t border-tm-border/30">
            <p className="text-[10px] text-tm-muted uppercase tracking-wider mb-1">
              Fuentes
            </p>
            <div className="space-y-1">
              {message.fuentes.map((fuente, i) => (
                <div key={i} className="text-[11px] text-tm-muted flex items-center gap-1">
                  <span className="text-tm-accent">
                    {fuente.tipo_fuente === "oficial_fabricante" ? "📋" :
                     fuente.tipo_fuente === "verificacion_manual" ? "✋" :
                     fuente.tipo_fuente === "web_search" ? "🌐" : "💬"}
                  </span>
                  <span>
                    {fuente.producto && `${fuente.producto} · `}
                    {fuente.marca && `${fuente.marca} `}
                    {fuente.modelo && `${fuente.modelo} · `}
                    {fuente.sistema && `${fuente.sistema}`}
                  </span>
                  {fuente.url && (
                    <a
                      href={fuente.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-tm-accent2 hover:underline truncate max-w-[150px]"
                    >
                      [link]
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Productos mencionados ─────────────── */}
        {!isUser && message.productos && message.productos.length > 0 && (
          <div className="mt-2 flex gap-1 flex-wrap">
            {message.productos.map((prod) => (
              <span
                key={prod}
                className="text-[10px] bg-tm-accent/10 text-tm-accent px-2 py-0.5 rounded-full"
              >
                {prod}
              </span>
            ))}
          </div>
        )}

        {/* ── Timestamp ────────────────────────── */}
        <div className="mt-1 text-[10px] text-tm-muted/50 text-right">
          {message.timestamp.toLocaleTimeString("es-AR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  );
}
