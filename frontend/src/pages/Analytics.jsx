import { useState, useEffect } from 'react';
import axios from 'axios';
import Header from '../components/Header';
import {
  BarChart3,
  MessageSquare,
  TrendingUp,
  AlertTriangle,
  ThumbsUp,
  Loader2,
  HelpCircle,
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';

/** Color palette for pie chart segments. */
const PIE_COLORS = [
  '#3b82f6',
  '#22c55e',
  '#f59e0b',
  '#ef4444',
  '#8b5cf6',
  '#ec4899',
  '#06b6d4',
  '#f97316',
  '#14b8a6',
  '#6366f1',
];

/**
 * Analytics dashboard page.
 * Fetches /api/analytics and renders key metrics, charts, and tables.
 */
export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const { data: res } = await axios.get('/api/analytics');
        setData(res);
      } catch (err) {
        setError('Failed to load analytics data.');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  /**
   * Stat card component.
   * @param {Object} p
   * @param {import('lucide-react').LucideIcon} p.icon
   * @param {string} p.label
   * @param {string|number} p.value
   * @param {string} [p.sub]
   * @param {string} [p.color]
   */
  const StatCard = ({ icon: Icon, label, value, sub, color = 'text-accent' }) => (
    <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <Icon size={16} className={color} />
        <span className="text-xs font-medium text-navy-400 uppercase tracking-wide">
          {label}
        </span>
      </div>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-navy-500 mt-1">{sub}</p>}
    </div>
  );

  /** Placeholder values when data hasn't loaded. */
  const safeData = data ?? {
    total_queries: 0,
    today_queries: 0,
    week_queries: 0,
    category_distribution: [],
    avg_confidence: 0,
    escalation_rate: 0,
    satisfaction_rate: 0,
    top_questions: [],
    recent_escalations: [],
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <Header />

      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-6xl mx-auto">
          {/* ── Title ──────────────────────────────────── */}
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 rounded-xl bg-accent/10 flex items-center justify-center">
              <BarChart3 size={22} className="text-accent" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-white">Analytics</h1>
              <p className="text-sm text-navy-400">
                Helpdesk performance overview
              </p>
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 size={32} className="animate-spin text-accent" />
            </div>
          ) : error ? (
            <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-6 text-center">
              <p className="text-red-400">{error}</p>
            </div>
          ) : (
            <>
              {/* ── KPI cards ─────────────────────────── */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <StatCard
                  icon={MessageSquare}
                  label="Total Queries"
                  value={safeData.total_queries.toLocaleString()}
                  sub={`${safeData.today_queries} today / ${safeData.week_queries} this week`}
                />
                <StatCard
                  icon={TrendingUp}
                  label="Avg Confidence"
                  value={`${Math.round((safeData.avg_confidence ?? 0) * 100)}%`}
                  color="text-green-500"
                />
                <StatCard
                  icon={AlertTriangle}
                  label="Escalation Rate"
                  value={`${Math.round((safeData.escalation_rate ?? 0) * 100)}%`}
                  color="text-amber-500"
                />
                <StatCard
                  icon={ThumbsUp}
                  label="Satisfaction"
                  value={`${Math.round((safeData.satisfaction_rate ?? 0) * 100)}%`}
                  color="text-green-500"
                />
              </div>

              {/* ── Charts row ────────────────────────── */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {/* Category distribution pie chart */}
                <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5">
                  <h3 className="text-sm font-medium text-white mb-4">
                    Category Distribution
                  </h3>
                  {safeData.category_distribution?.length > 0 ? (
                    <ResponsiveContainer width="100%" height={260}>
                      <PieChart>
                        <Pie
                          data={safeData.category_distribution}
                          cx="50%"
                          cy="50%"
                          innerRadius={55}
                          outerRadius={95}
                          paddingAngle={3}
                          dataKey="count"
                          nameKey="category"
                          label={({ category, percent }) =>
                            `${category} ${(percent * 100).toFixed(0)}%`
                          }
                        >
                          {safeData.category_distribution.map((_, i) => (
                            <Cell
                              key={i}
                              fill={PIE_COLORS[i % PIE_COLORS.length]}
                            />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#1e293b',
                            border: '1px solid #334155',
                            borderRadius: '12px',
                            fontSize: '12px',
                          }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <p className="text-sm text-navy-500 text-center py-12">
                      No data available yet.
                    </p>
                  )}
                </div>

                {/* Top questions bar chart */}
                <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5">
                  <h3 className="text-sm font-medium text-white mb-4">
                    Most Asked Questions
                  </h3>
                  {safeData.top_questions?.length > 0 ? (
                    <ResponsiveContainer width="100%" height={260}>
                      <BarChart
                        data={safeData.top_questions.slice(0, 7)}
                        layout="vertical"
                        margin={{ left: 10, right: 20 }}
                      >
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke="#334155"
                          horizontal={false}
                        />
                        <XAxis type="number" stroke="#64748b" fontSize={11} />
                        <YAxis
                          type="category"
                          dataKey="question"
                          width={160}
                          stroke="#64748b"
                          fontSize={11}
                          tickFormatter={(v) =>
                            v.length > 28 ? v.slice(0, 28) + '...' : v
                          }
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#1e293b',
                            border: '1px solid #334155',
                            borderRadius: '12px',
                            fontSize: '12px',
                          }}
                        />
                        <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <p className="text-sm text-navy-500 text-center py-12">
                      No data available yet.
                    </p>
                  )}
                </div>
              </div>

              {/* ── Recent escalations table ──────────── */}
              <div className="bg-navy-800 border border-navy-700 rounded-2xl p-5">
                <div className="flex items-center gap-2 mb-4">
                  <AlertTriangle size={16} className="text-amber-500" />
                  <h3 className="text-sm font-medium text-white">
                    Recent Escalated Tickets
                  </h3>
                </div>
                {safeData.recent_escalations?.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                      <thead>
                        <tr className="border-b border-navy-700 text-navy-400 text-xs uppercase tracking-wider">
                          <th className="py-2 pr-4">Ticket</th>
                          <th className="py-2 pr-4">Issue</th>
                          <th className="py-2 pr-4">Category</th>
                          <th className="py-2 pr-4">Reason</th>
                          <th className="py-2">Time</th>
                        </tr>
                      </thead>
                      <tbody>
                        {safeData.recent_escalations.map((esc, i) => (
                          <tr
                            key={i}
                            className="border-b border-navy-700/50 last:border-0"
                          >
                            <td className="py-2.5 pr-4 text-accent font-mono text-xs">
                              #{esc.ticket_id}
                            </td>
                            <td className="py-2.5 pr-4 text-navy-300 max-w-xs truncate">
                              {esc.issue}
                            </td>
                            <td className="py-2.5 pr-4">
                              <span className="px-2 py-0.5 rounded-full bg-navy-700 text-navy-300 text-xs">
                                {esc.category}
                              </span>
                            </td>
                            <td className="py-2.5 pr-4 text-navy-400 text-xs">
                              {esc.reason}
                            </td>
                            <td className="py-2.5 text-navy-500 text-xs whitespace-nowrap">
                              {esc.timestamp}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="flex items-center justify-center py-8 text-navy-500">
                    <HelpCircle size={16} className="mr-2" />
                    <span className="text-sm">No escalations recorded yet.</span>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
