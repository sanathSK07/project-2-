import {
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
 * Category filter definitions.
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
 * Grid of category filter buttons used to narrow chat scope.
 *
 * @param {Object} props
 * @param {string|null} props.active - Currently selected category value
 * @param {(cat: string|null) => void} props.onChange - Called when a category is toggled
 */
export default function CategoryPanel({ active, onChange }) {
  return (
    <div className="grid grid-cols-5 gap-2">
      {CATEGORIES.map(({ label, value, icon: Icon }) => {
        const selected = active === value;
        return (
          <button
            key={value}
            onClick={() => onChange(selected ? null : value)}
            className={`flex flex-col items-center gap-1.5 p-3 rounded-xl text-xs font-medium transition-default ${
              selected
                ? 'bg-accent/15 text-accent border border-accent/30'
                : 'bg-navy-800 text-navy-400 border border-navy-700 hover:border-navy-600 hover:text-white'
            }`}
          >
            <Icon size={18} />
            {label}
          </button>
        );
      })}
    </div>
  );
}
