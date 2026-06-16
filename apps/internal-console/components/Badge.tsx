const COLORS: Record<string, string> = {
  pending: "bg-earth-gold/20 text-earth-goldmuted",
  in_review: "bg-blue-100 text-blue-700",
  decided: "bg-earth-green/15 text-earth-green",
  accepted: "bg-green-100 text-green-700",
  needs_retake: "bg-amber-100 text-amber-700",
  documentation_only: "bg-stone-200 text-stone-700",
  rejected: "bg-red-100 text-red-700",
  RESTRICTED: "bg-red-100 text-red-700",
  INTERNAL: "bg-stone-200 text-stone-700",
  PARTNER: "bg-earth-gold/20 text-earth-goldmuted",
  PUBLIC: "bg-green-100 text-green-700",
};

export function Badge({ value }: { value: string | null | undefined }) {
  const v = value ?? "—";
  const cls = COLORS[v] ?? "bg-stone-200 text-stone-700";
  return <span className={`badge ${cls}`}>{v}</span>;
}
