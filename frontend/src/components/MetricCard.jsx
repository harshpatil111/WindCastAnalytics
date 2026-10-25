export default function MetricCard({
  title,
  value,
  unit,
  description,
  icon: Icon,
  accent = "emerald",
}) {
  const accents = {
    emerald: "bg-emerald-400/10 text-emerald-400",
    blue: "bg-blue-400/10 text-blue-400",
    amber: "bg-amber-400/10 text-amber-400",
    violet: "bg-violet-400/10 text-violet-400",
  };

  return (
    <article className="rounded-2xl border border-slate-800 bg-[#111b2d] p-5 transition hover:border-slate-700">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>

          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold tracking-tight text-white">
              {value}
            </span>

            {unit && (
              <span className="text-xs font-medium text-slate-500">
                {unit}
              </span>
            )}
          </div>
        </div>

        {Icon && (
          <div className={`rounded-xl p-3 ${accents[accent] || accents.emerald}`}>
            <Icon size={21} />
          </div>
        )}
      </div>

      <p className="mt-4 border-t border-slate-800 pt-3 text-xs leading-5 text-slate-500">
        {description}
      </p>
    </article>
  );
}