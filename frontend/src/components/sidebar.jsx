import {
  Activity,
  LayoutDashboard,
  Wind,
  ChartNoAxesCombined,
  Settings,
  Zap,
} from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="flex w-64 shrink-0 flex-col border-r border-slate-800 bg-[#0b1220] px-5 py-6">
      <div className="mb-10 flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-400/10 text-emerald-400">
          <Wind size={25} />
        </div>

        <div>
          <h1 className="text-lg font-bold tracking-tight text-white">
            WindCast
          </h1>
          <p className="text-xs text-slate-500">Analytics Platform</p>
        </div>
      </div>

      <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
        Workspace
      </p>

      <nav className="space-y-2">
        <a
          href="#dashboard"
          className="flex items-center gap-3 rounded-xl bg-emerald-400/10 px-3 py-3 text-sm font-medium text-emerald-400"
        >
          <LayoutDashboard size={19} />
          Dashboard
        </a>

        <a
          href="#forecast"
          className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-slate-800 hover:text-white"
        >
          <ChartNoAxesCombined size={19} />
          Forecast Analysis
        </a>

        <a
          href="#comparison"
          className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm text-slate-400 transition hover:bg-slate-800 hover:text-white"
        >
          <Activity size={19} />
          Data Comparison
        </a>
      </nav>

      <div className="mt-auto rounded-2xl border border-slate-800 bg-slate-900/70 p-4">
        <div className="mb-3 flex items-center gap-2 text-emerald-400">
          <Zap size={17} />
          <span className="text-sm font-semibold">Data Source</span>
        </div>

        <p className="text-sm text-white">Elexon BMRS</p>
        <p className="mt-1 text-xs leading-5 text-slate-500">
          UK wind generation forecasts and actual generation.
        </p>

        <div className="mt-4 flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400" />
          <span className="text-xs text-slate-400">
            Live API integration
          </span>
        </div>
      </div>

      <div className="mt-5 flex items-center gap-3 px-2 text-slate-500">
        <Settings size={17} />
        <span className="text-xs">WindCast Analytics v1.0</span>
      </div>
    </aside>
  );
}