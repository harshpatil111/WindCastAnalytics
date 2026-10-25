import { ArrowDownWideNarrow } from "lucide-react";

function formatNumber(value) {
  return Number(value).toLocaleString("en-GB", {
    maximumFractionDigits: 2,
  });
}

export default function ComparisonTable({ data }) {
  return (
    <section
      id="comparison"
      className="overflow-hidden rounded-2xl border border-slate-800 bg-[#111b2d]"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 p-5">
        <div>
          <h3 className="text-lg font-semibold text-white">
            Delivery Interval Comparison
          </h3>

          <p className="mt-1 text-sm text-slate-400">
            Forecast, actual generation, and signed forecast error.
          </p>
        </div>

        <span className="rounded-lg bg-slate-800 px-3 py-2 text-xs text-slate-300">
          {data.length.toLocaleString()} intervals
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[850px] text-left text-sm">
          <thead className="bg-slate-900/70 text-xs uppercase tracking-wider text-slate-500">
            <tr>
              <th className="px-5 py-4 font-medium">Delivery time (UTC)</th>
              <th className="px-5 py-4 text-right font-medium">Forecast</th>
              <th className="px-5 py-4 text-right font-medium">Actual</th>
              <th className="px-5 py-4 text-right font-medium">Error</th>
              <th className="px-5 py-4 text-right font-medium">Abs. Error</th>
              <th className="px-5 py-4 text-right font-medium">Lead Time</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-800/80">
            {data.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-5 py-12 text-center text-slate-500">
                  No comparison records available.
                </td>
              </tr>
            ) : (
              data.map((item) => (
                <tr
                  key={`${item.delivery_time}-${item.forecast_publish_time}`}
                  className="transition hover:bg-slate-800/30"
                >
                  <td className="whitespace-nowrap px-5 py-4 text-slate-300">
                    {new Date(item.delivery_time).toLocaleString("en-GB", {
                      year: "numeric",
                      month: "short",
                      day: "2-digit",
                      hour: "2-digit",
                      minute: "2-digit",
                      timeZone: "UTC",
                    })}
                  </td>

                  <td className="px-5 py-4 text-right text-slate-300">
                    {formatNumber(item.forecast_mw)} MW
                  </td>

                  <td className="px-5 py-4 text-right text-slate-300">
                    {formatNumber(item.actual_mw)} MW
                  </td>

                  <td
                    className={`px-5 py-4 text-right font-medium ${
                      item.error_mw > 0
                        ? "text-amber-400"
                        : item.error_mw < 0
                          ? "text-blue-400"
                          : "text-emerald-400"
                    }`}
                  >
                    {item.error_mw > 0 ? "+" : ""}
                    {formatNumber(item.error_mw)} MW
                  </td>

                  <td className="px-5 py-4 text-right text-slate-300">
                    {formatNumber(item.absolute_error_mw)} MW
                  </td>

                  <td className="px-5 py-4 text-right text-slate-300">
                    {formatNumber(item.lead_hours)} h
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}