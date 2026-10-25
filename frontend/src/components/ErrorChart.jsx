import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from "recharts";

export default function ErrorChart({ data }) {
  const chartData = data.map((item) => ({
    ...item,
    timeLabel: new Date(item.delivery_time).toLocaleString("en-GB", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "UTC",
    }),
  }));

  return (
    <section className="rounded-2xl border border-slate-800 bg-[#111b2d] p-5">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white">
          Forecast Error Analysis
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          Forecast minus actual generation. Positive values indicate overforecasting.
        </p>
      </div>

      {chartData.length === 0 ? (
        <div className="flex h-72 items-center justify-center text-sm text-slate-500">
          No matched data available for this period.
        </div>
      ) : (
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid
                stroke="#253248"
                strokeDasharray="4 4"
                vertical={false}
              />

              <XAxis
                dataKey="timeLabel"
                stroke="#64748b"
                tick={{ fill: "#94a3b8", fontSize: 10 }}
                tickLine={false}
                axisLine={false}
                minTickGap={35}
              />

              <YAxis
                stroke="#64748b"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                tickLine={false}
                axisLine={false}
              />

              <ReferenceLine y={0} stroke="#94a3b8" />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#0b1220",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                  color: "#fff",
                }}
                formatter={(value) => [
                  `${Number(value).toLocaleString()} MW`,
                  "Forecast Error",
                ]}
              />

              <Bar
                dataKey="error_mw"
                name="Forecast Error"
                fill="#a78bfa"
                radius={[3, 3, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}