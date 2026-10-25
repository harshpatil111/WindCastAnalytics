import { CalendarDays, RefreshCw } from "lucide-react";

export default function Header({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
  onRefresh,
  loading,
}) {
  return (
    <header className="flex flex-col justify-between gap-5 border-b border-slate-800 bg-[#0b1220]/90 px-6 py-5 xl:flex-row xl:items-center xl:px-9">
      <div>
        <div className="mb-2 flex items-center gap-2 text-xs text-slate-500">
          <span>Workspace</span>
          <span>/</span>
          <span className="text-emerald-400">Overview</span>
        </div>

        <h2 className="text-2xl font-bold tracking-tight text-white">
          Wind Generation Overview
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Compare day-ahead forecasts with actual UK wind generation.
        </p>
      </div>

      <div className="flex flex-wrap items-end gap-3">
        <label className="flex flex-col gap-2">
          <span className="text-xs text-slate-400">Start date</span>
          <input
            type="date"
            value={startDate}
            max={endDate}
            onChange={(event) => onStartDateChange(event.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-emerald-400"
          />
        </label>

        <label className="flex flex-col gap-2">
          <span className="text-xs text-slate-400">End date</span>
          <input
            type="date"
            value={endDate}
            min={startDate}
            onChange={(event) => onEndDateChange(event.target.value)}
            className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none focus:border-emerald-400"
          />
        </label>

        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <RefreshCw
            size={16}
            className={loading ? "animate-spin" : ""}
          />
          {loading ? "Loading..." : "Refresh"}
        </button>
      </div>
    </header>
  );
}