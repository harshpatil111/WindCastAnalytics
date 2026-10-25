import { useCallback, useEffect, useState } from "react";
import {
  Activity,
  Gauge,
  TrendingUp,
  Database,
  AlertCircle,
  Clock3,
} from "lucide-react";

import Sidebar from "./components/sidebar.jsx";
import Header from "./components/Header";
import MetricCard from "./components/MetricCard";
import ForecastChart from "./components/ForecastChart";
import ErrorChart from "./components/ErrorChart";
import ComparisonTable from "./components/comparisonTable.jsx";

import { fetchSummary, fetchComparison } from "./services/api";

const INITIAL_START_DATE = "2026-01-01";
const INITIAL_END_DATE = "2026-01-31";

function formatMetric(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) {
    return "—";
  }

  return Number(value).toLocaleString("en-GB", {
    maximumFractionDigits: 2,
  });
}

export default function App() {
  const [startDate, setStartDate] = useState(INITIAL_START_DATE);
  const [endDate, setEndDate] = useState(INITIAL_END_DATE);

  const [summary, setSummary] = useState(null);
  const [comparison, setComparison] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    if (!startDate || !endDate || startDate > endDate) {
      setError("Choose a valid delivery date range.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const [summaryResult, comparisonResult] = await Promise.all([
        fetchSummary(startDate, endDate),
        fetchComparison(startDate, endDate),
      ]);

      if (summaryResult.status !== "success") {
        throw new Error("The summary API returned an unsuccessful response.");
      }

      if (comparisonResult.status !== "success") {
        throw new Error("The comparison API returned an unsuccessful response.");
      }

      setSummary(summaryResult);
      setComparison(comparisonResult.results ?? []);
    } catch (err) {
      console.error("Dashboard API error:", err);

      setSummary(null);
      setComparison([]);

      const apiMessage = err.response?.data?.error;

      setError(
        apiMessage ||
          (err.code === "ECONNABORTED"
            ? "The request timed out. Please try again."
            : "Unable to load dashboard data. Check that the Django backend is running.")
      );
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const metrics = summary?.metrics;

  return (
    <div className="min-h-screen bg-[#0b1220] text-slate-200">
      <div className="flex min-h-screen">
        <div className="hidden lg:flex">
          <Sidebar />
        </div>

        <main className="min-w-0 flex-1">
          <Header
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
            onRefresh={loadDashboard}
            loading={loading}
          />

          <div className="mx-auto max-w-[1700px] space-y-6 p-5 md:p-7 xl:p-9">
            <section className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
              <div>
                <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1.5 text-xs font-medium text-emerald-400">
                  <Activity size={14} />
                  Forecast Performance
                </div>

                <h1 className="text-2xl font-bold tracking-tight text-white md:text-3xl">
                  Wind Power Analytics
                </h1>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
                  Evaluate day-ahead UK wind generation forecasts against
                  actual generation to support electricity purchasing decisions.
                </p>
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-500">
                <Clock3 size={15} />
                <span>Delivery timestamps shown in UTC</span>
              </div>
            </section>

            {error && (
              <div
                role="alert"
                className="flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200"
              >
                <AlertCircle className="mt-0.5 shrink-0 text-red-400" size={19} />

                <div>
                  <p className="font-semibold">Unable to load analytics</p>
                  <p className="mt-1 leading-6">{error}</p>

                  <button
                    onClick={loadDashboard}
                    className="mt-3 rounded-lg border border-red-400/30 px-3 py-1.5 text-xs font-semibold transition hover:bg-red-400/10"
                  >
                    Try again
                  </button>
                </div>
              </div>
            )}

            {loading && !summary && (
              <div className="rounded-xl border border-slate-800 bg-[#111b2d] p-4 text-sm text-slate-400">
                Retrieving forecast and actual generation data from Elexon...
              </div>
            )}

            <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 2xl:grid-cols-4">
              <MetricCard
                title="Mean Absolute Error"
                value={formatMetric(metrics?.mae_mw)}
                unit="MW"
                description="Average absolute difference between forecast and actual generation."
                icon={Gauge}
                accent="emerald"
              />

              <MetricCard
                title="Root Mean Squared Error"
                value={formatMetric(metrics?.rmse_mw)}
                unit="MW"
                description="Penalizes larger forecast errors more heavily."
                icon={TrendingUp}
                accent="blue"
              />

              <MetricCard
                title="Forecast Bias"
                value={formatMetric(metrics?.bias_mw)}
                unit="MW"
                description="Positive means overforecasting; negative means underforecasting."
                icon={Activity}
                accent="amber"
              />

              <MetricCard
                title="Matched Intervals"
                value={formatMetric(metrics?.sample_count)}
                description="Hourly delivery intervals with eligible forecasts and actual data."
                icon={Database}
                accent="violet"
              />
            </section>

            {summary && (
              <div className="flex flex-wrap items-center gap-x-5 gap-y-2 rounded-xl border border-slate-800 bg-slate-900/50 px-4 py-3 text-xs text-slate-400">
                <span>
                  Delivery period:{" "}
                  <strong className="text-slate-200">
                    {summary.delivery_period.start_date}
                  </strong>{" "}
                  to{" "}
                  <strong className="text-slate-200">
                    {summary.delivery_period.end_date}
                  </strong>
                </span>

                <span className="hidden text-slate-700 sm:inline">|</span>

                <span>
                  Rule: {summary.forecast_rule}
                </span>
              </div>
            )}

            <ForecastChart data={comparison} />

            <ErrorChart data={comparison} />

            <ComparisonTable data={comparison} />

            <footer className="flex flex-col justify-between gap-2 border-t border-slate-800 py-5 text-xs text-slate-500 sm:flex-row">
              <p>WindCast Analytics · UK Wind Generation Forecast Evaluation</p>
              <p>Data source: Elexon BMRS FUELHH and WINDFOR</p>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}