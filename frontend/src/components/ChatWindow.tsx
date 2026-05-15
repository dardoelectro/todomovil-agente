"use client";

import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import SemaforoBadge from "./SemaforoBadge";
import CertaintyIndicator from "./CertaintyIndicator";

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
  fuentes?: Array<{
    tipo_fuente: string;
    producto: string;
    sistema?: string;
    marca?: string;
    modelo?: string;
    url?: string;
    certezza: string;
  }>;
  productos?: string[];
  capa?: string;
  timestamp: Date;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

      const response = await fetch(`${API_URL}/api/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_history: messages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: `msg_${Date.now()}_resp`,
        role: "assistant",
        content: data.reply,
        semaforo: data.semaforo,
        certeza: data.certeza_global,
        fuentes: data.fuentes,
        productos: data.productos_mencionados,
        capa: data.capa_utilizada,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: `msg_${Date.now()}_err`,
        role: "assistant",
        content: "Error al conectar con el servidor. Verificá que el backend esté corriendo en el puerto 8000.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      {/* ── Header ──────────────────────────────── */}
      <div className="chat-header">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-tm-accent rounded-full flex items-center justify-center text-tm-bg font-bold text-lg">
            TM
          </div>
          <div>
            <h1 className="text-lg font-bold text-tm-text">
              TodoMovil Agente
            </h1>
            <p className="text-xs text-tm-muted">
              Copiloto del vendedor — RAG + Semáforo + Certeza
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs text-tm-muted">
          <span className="w-2 h-2 bg-tm-verde rounded-full animate-pulse" />
          En línea
        </div>
      </div>

      {/* ── Messages ────────────────────────────── */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-tm-muted space-y-4">
            <div className="w-20 h-20 bg-tm-accent/20 rounded-full flex items-center justify-center">
              <span className="text-4xl">🔧</span>
            </div>
            <div className="text-center space-y-2">
              <h2 className="text-xl font-bold text-tm-text">
                Copiloto del Vendedor
              </h2>
              <p className="text-sm max-w-md">
                Preguntame sobre compatibilidad de escáneres, funciones,
                objeciones de clientes, o qué producto recomendar.
              </p>
            </div>
            <div className="flex flex-wrap gap-2 mt-4">
              {[
                "¿Qué escáner me recomendás para un mecánico general?",
                "¿El CRP239 cubre BSI en Peugeot 208?",
                "¿Cómo respondo si dicen que es muy caro?",
                "¿El MX900 hace IMMO?",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="btn-secondary text-xs py-2 px-3"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-tm-muted text-sm">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-tm-accent rounded-full animate-bounce [animation-delay:0ms]" />
              <span className="w-2 h-2 bg-tm-accent rounded-full animate-bounce [animation-delay:150ms]" />
              <span className="w-2 h-2 bg-tm-accent rounded-full animate-bounce [animation-delay:300ms]" />
            </div>
            Pensando...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ── Input ───────────────────────────────── */}
      <div className="chat-input-area">
        <div className="flex gap-3 items-center">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Preguntá sobre escáneres, compatibilidad, objeciones..."
            className="input-chat"
            disabled={loading}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>
  );
}
