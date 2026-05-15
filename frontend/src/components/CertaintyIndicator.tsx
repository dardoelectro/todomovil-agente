"use client";

interface Props {
  level: string; // Alta | Media | Baja
}

const LABELS: Record<string, string> = {
  Alta: "Certeza Alta",
  Media: "Certeza Media",
  Baja: "Certeza Baja",
};

export default function CertaintyIndicator({ level }: Props) {
  const colorClass =
    level === "Alta"
      ? "certeza-alta"
      : level === "Media"
      ? "certeza-media"
      : "certeza-baja";

  return (
    <span className={`text-xs font-semibold ${colorClass}`}>
      {LABELS[level] || level}
    </span>
  );
}
