import {
  Plus,
  MessageSquare,
  KeyRound,
  Globe,
  Wifi,
  Mail,
  AppWindow,
  Printer,
  ShieldCheck,
  HardDrive,
  UserPlus,
  Cloud,
} from 'lucide-react';

/**
 * @typedef {Object} Conversation
 * @property {string} id
 * @property {string} title
 * @property {Date} timestamp
 */

/**
 * Quick-access category definitions.
 * @type {Array<{label: string, value: string, icon: import('lucide-react').LucideIcon}>}
 */
const CATEGORIES = [
  { label: 'Password', value: 'password', icon: KeyRound },
  { label: 'VPN', value: 'vpn', icon: Globe },
  { label: 'WiFi', value: 'wifi', icon: Wifi },
  { label: 'Email', value: 'email', icon: Mail },
  { label: 'Software', value: 'software', icon: AppWindow },
  { label: 'Printer', value: 'printer', icon: Printer },
  { label: 'Security', value: 'security', icon: ShieldCheck },
  { label: 'Hardware', value: 'hardware', icon: HardDrive },
  { label: 'Onboarding', value: 'onboarding', icon: UserPlus },
  { label: 'Cloud', value: 'cloud', icon: Cloud },
];

/**
 * Left sidebar with new-chat button, conversation history, and category filters.
 *
 * @param {Object} props
 * @param {() => void} props.onNewChat
 * @param {Conversation[]} props.conversations
 * @param {string} props.activeId - Current conversation id
 * @param {(id: string) => void} props.onSelect
 * @param {string|null} props.categoryFilter
 * @param {(cat: string|null) => void} props.onCategoryChange
 */
export default function SideBar({
  onNewChat,
  conversations,
  activeId,
  onSelect,
  categoryFilter,
  onCategoryChange,
}) {
  return (
    <aside className="w-64 shrink-0 bg-navy-800/60 border-r border-navy-700 flex flex-col h-full overflow-hidden">
      {/* ── New Chat ──────────────────────────────────── */}
      <div className="p-3">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg border border-navy-600 text-sm font-medium text-navy-300 hover:text-white hover:border-accent hover:bg-accent/10 transition-default"
        >
          <Plus size={16} />
          New Chat
        </button>
      </div>

      {/* ── Conversation history ──────────────────────── */}
      <div className="flex-1 overflow-y-auto px-2">
        {conversations.length > 0 && (
          <div className="mb-4">
            <p className="text-xs font-semibold uppercase text-navy-500 px-2 mb-2">
              Recent
            </p>
            <ul className="space-y-0.5">
              {conversations.map((conv) => (
                <li key={conv.id}>
                  <button
                    onClick={() => onSelect(conv.id)}
                    className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm truncate transition-default ${
                      conv.id === activeId
                        ? 'bg-accent/15 text-accent'
                        : 'text-navy-400 hover:bg-navy-700 hover:text-white'
                    }`}
                  >
                    <MessageSquare size={14} className="shrink-0" />
                    <span className="truncate">{conv.title}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* ── Category quick filters ────────────────────── */}
      <div className="border-t border-navy-700 p-3">
        <p className="text-xs font-semibold uppercase text-navy-500 mb-2">
          Categories
        </p>
        <div className="grid grid-cols-2 gap-1.5">
          {CATEGORIES.map(({ label, value, icon: Icon }) => {
            const active = categoryFilter === value;
            return (
              <button
                key={value}
                onClick={() => onCategoryChange(active ? null : value)}
                className={`flex items-center gap-1.5 px-2 py-1.5 rounded-md text-xs font-medium transition-default ${
                  active
                    ? 'bg-accent/20 text-accent'
                    : 'text-navy-400 hover:bg-navy-700 hover:text-white'
                }`}
              >
                <Icon size={12} />
                {label}
              </button>
            );
          })}
        </div>
      </div>
    </aside>
  );
}
