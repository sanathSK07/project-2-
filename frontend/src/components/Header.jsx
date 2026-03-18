import { Link, useLocation } from 'react-router-dom';
import { Monitor, Shield, BarChart3 } from 'lucide-react';

/**
 * Top navigation header.
 * Displays the app title, subtitle, and navigation links to Chat, Admin, and Analytics.
 */
export default function Header() {
  const { pathname } = useLocation();

  const navItems = [
    { to: '/', label: 'Chat', icon: Monitor },
    { to: '/admin', label: 'Admin', icon: Shield },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  ];

  return (
    <header className="bg-navy-800 border-b border-navy-700 px-6 py-3 flex items-center justify-between shrink-0">
      {/* ── Branding ──────────────────────────────────── */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-accent flex items-center justify-center">
          <Monitor size={20} className="text-white" />
        </div>
        <div>
          <h1 className="text-lg font-semibold leading-tight text-white">
            IT HelpDesk AI
          </h1>
          <p className="text-xs text-navy-400 leading-tight">
            Powered by RAG + AI Agents
          </p>
        </div>
      </div>

      {/* ── Navigation ────────────────────────────────── */}
      <nav className="flex items-center gap-1">
        {navItems.map(({ to, label, icon: Icon }) => {
          const active = pathname === to;
          return (
            <Link
              key={to}
              to={to}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-default ${
                active
                  ? 'bg-accent/15 text-accent'
                  : 'text-navy-400 hover:text-white hover:bg-navy-700'
              }`}
            >
              <Icon size={16} />
              <span className="hidden sm:inline">{label}</span>
            </Link>
          );
        })}
      </nav>
    </header>
  );
}
