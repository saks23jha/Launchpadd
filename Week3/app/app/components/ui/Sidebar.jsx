'use client'; // Mark this component as client-side

import { useRouter } from 'next/navigation'; // Correct import for Client-side navigation
import {
  HomeIcon,
  TableCellsIcon,
  CreditCardIcon,
  WrenchScrewdriverIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  QuestionMarkCircleIcon,
  CogIcon,
  BellIcon,
} from '@heroicons/react/24/solid';

export default function Sidebar() {
  const router = useRouter();

  return (
    <aside className="w-72 bg-white min-h-screen px-6 py-8 shadow-md">
      {/* Logo */}
      <div className="flex items-center gap-3 mb-12">
        <img src="/logo.png" alt="Purity UI Dashboard Logo" className="w-9 h-9" />
        <span className="font-semibold text-sm tracking-wide text-gray-800">
          PURITY UI DASHBOARD
        </span>
      </div>

      {/* Main menu */}
      <nav className="space-y-1">
        <SidebarItem active={true} icon={<HomeIcon />} label="Dashboard" route="/dashboard" />
        <SidebarItem icon={<TableCellsIcon />} label="Tables" route="/tables" />
        <SidebarItem icon={<CreditCardIcon />} label="Billing" route="/billing" />
        <SidebarItem icon={<WrenchScrewdriverIcon />} label="RTL" route="/rtl" />
      </nav>

      {/* Account pages */}
      <p className="text-[11px] font-semibold text-gray-400 mt-10 mb-3 tracking-wider">
        ACCOUNT PAGES
      </p>
      <nav className="space-y-1">
        <SidebarItem icon={<UserIcon />} label="Profile" route="/profile" />
        <SidebarItem icon={<ArrowRightOnRectangleIcon />} label="Sign In" route="/sign-in" />
        <SidebarItem icon={<UserPlusIcon />} label="Sign Up" route="/sign-up" />
      </nav>

      {/* Help card */}
      <div className="mt-12 bg-gradient-to-br from-teal-400 to-teal-500 rounded-2xl p-5 text-white relative overflow-hidden">
        <div className="bg-white/20 w-10 h-10 rounded-lg flex items-center justify-center mb-3">
          <QuestionMarkCircleIcon className="w-6 h-6" />
        </div>
        <p className="font-semibold text-sm">Need help?</p>
        <p className="text-xs opacity-90 mb-4">
          Please check our docs
        </p>
        <button className="w-full bg-white text-gray-800 text-xs font-semibold py-2 rounded-lg hover:bg-gray-100 transition">
          DOCUMENTATION
        </button>
      </div>
    </aside>
  );
}

// SidebarItem Component
function SidebarItem({ icon, label, active, route }) {
  const router = useRouter(); // Client-side navigation

  const handleClick = () => {
    router.push(route); // Navigate to the selected route
  };

  return (
    <div
      className={`flex items-center gap-4 px-4 py-3 rounded-xl text-sm cursor-pointer transition
      ${active ? 'bg-gray-100 text-gray-900 font-semibold shadow-sm' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-800'}`}
      onClick={handleClick} // Handle click to navigate
    >
      <div
        className={`w-9 h-9 flex items-center justify-center rounded-lg
        ${active ? 'bg-teal-400 text-white' : 'bg-gray-100'}`}
      >
        <span className="w-5 h-5">{icon}</span>
      </div>
      {label}
    </div>
  );
}
