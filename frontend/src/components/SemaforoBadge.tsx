"use client";

interface Props {
  color: string; // verde | amarillo | rojo | no_aplica
}

const LABELS: Record<string, string> = {
  verde: "VERDE — Ofrecer",
  amarillo: "AMARILLO — Ofrecer con advertencia",
  rojo: "ROJO — No ofrecer",
  no_aplica: "NO APLICA — Fuera de cobertura",
};

const ICONS: Record<string, string> = {
  verde: "🟢",
  amarillo: "🟡",
  rojo: "🔴",
  no_aplica: "⚪",
};

export default function SemaforoBadge({ color }: Props) {
  const colorClass =
    color === "verde"
      ? "semaforo-verde"
      : color === "amarillo"
      ? "semaforo-amarillo"
      : color === "rojo"
      ? "semaforo-rojo"
      : "semaforo-no-aplica";

  return (
    <span className={`semaforo-badge ${colorClass}`}>
      <span>{ICONS[color] || "⚪"}</span>
      {LABELS[color] || color}
    </span>
  );
}
