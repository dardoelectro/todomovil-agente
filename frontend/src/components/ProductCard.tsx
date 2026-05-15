"use client";

import SemaforoBadge from "./SemaforoBadge";

interface Props {
  id: string;
  nombre: string;
  marca: string;
  tipo: string;
  gamma: string;
  precio?: number;
  sistemas: string[];
  funciones: string[];
  semaforo_default: string;
  notas?: string;
}

export default function ProductCard({
  nombre,
  marca,
  tipo,
  gamma,
  precio,
  sistemas,
  funciones,
  semaforo_default,
  notas,
}: Props) {
  const gammaColors: Record<string, string> = {
    entrada: "bg-tm-accent/20 text-tm-accent",
    media: "bg-tm-accent2/20 text-tm-accent2",
    alta: "bg-tm-rojo/20 text-tm-rojo",
  };

  return (
    <div className="product-card">
      <div className="flex items-center justify-between mb-3">
        <div>
          <h3 className="font-bold text-tm-text">{nombre}</h3>
          <p className="text-xs text-tm-muted">{marca} · {tipo}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-xs px-2 py-0.5 rounded-full ${gammaColors[gamma] || "bg-tm-muted/20 text-tm-muted"}`}>
            {gamma}
          </span>
          <SemaforoBadge color={semaforo_default} />
        </div>
      </div>

      {precio && (
        <p className="text-lg font-bold text-tm-accent mb-2">
          ${precio.toLocaleString("es-AR")}
        </p>
      )}

      <div className="mb-2">
        <p className="text-[10px] text-tm-muted uppercase tracking-wider mb-1">
          Sistemas
        </p>
        <div className="flex flex-wrap gap-1">
          {sistemas.map((s) => (
            <span key={s} className="text-[11px] bg-tm-bg px-2 py-0.5 rounded text-tm-text">
              {s}
            </span>
          ))}
        </div>
      </div>

      {funciones.length > 0 && (
        <div className="mb-2">
          <p className="text-[10px] text-tm-muted uppercase tracking-wider mb-1">
            Funciones especiales
          </p>
          <div className="flex flex-wrap gap-1">
            {funciones.map((f) => (
              <span key={f} className="text-[11px] bg-tm-accent/10 px-2 py-0.5 rounded text-tm-accent">
                {f}
              </span>
            ))}
          </div>
        </div>
      )}

      {notas && (
        <p className="text-xs text-tm-muted mt-2 border-t border-tm-border/30 pt-2">
          {notas}
        </p>
      )}
    </div>
  );
}
