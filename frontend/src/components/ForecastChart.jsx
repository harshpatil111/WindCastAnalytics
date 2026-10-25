import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default function ForecastChart({ data }) {
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
    <section
      id="forecast"
      className="rounded-2xl border border-slate-800 bg-[#111b2d] p-5"
    >
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white">
          Forecast vs Actual
        </h3>

        <p className="mt-1 text-sm text-slate-400">
          Wind generation by delivery interval, measured in MW.
        </p>
      </div>

      {chartData.length === 0 ? (
        <div className="flex h-80 items-center justify-center text-sm text-slate-500">
          No matched data available for this period.
        </div>
      ) : (
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{ top: 10, right: 10, left: 0, bottom: 5 }}
            >
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
                width={60}
                label={{
                  value: "MW",
                  angle: -90,
                  position: "insideLeft",
                  fill: "#94a3b8",
                }}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#0b1220",
                  border: "1px solid #334155",
                  borderRadius: "12px",
                  color: "#fff",
                }}
                formatter={(value, name) => [
                  `${Number(value).toLocaleString()} MW`,
                  name,
                ]}
              />

              <Legend />

              <Line
                type="monotone"
                dataKey="forecast_mw"
                name="Forecast"
                stroke="#34d399"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />

              <Line
                type="monotone"
                dataKey="actual_mw"
                name="Actual"
                stroke="#60a5fa"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}