'use client';

export default function PlatformSettings() {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 max-w-md">
      
      {/* Title */}
      <h2 className="text-lg font-semibold text-gray-800 mb-6">
        Platform Settings
      </h2>

      {/* ACCOUNT */}
      <div className="mb-6">
        <p className="text-xs font-semibold text-gray-400 uppercase mb-4">
          Account
        </p>

        <SettingItem label="Email me when someone follows me" enabled />
        <SettingItem label="Email me when someone answers on my post" />
        <SettingItem label="Email me when someone mentions me" enabled />
      </div>

      {/* APPLICATION */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase mb-4">
          Application
        </p>

        <SettingItem label="New launches and projects" />
        <SettingItem label="Monthly product updates" />
        <SettingItem label="Subscribe to newsletter" enabled />
      </div>
    </div>
  );
}

/* 🔘 Toggle Row Component */
function SettingItem({ label, enabled = false }) {
  return (
    <div className="flex items-center justify-between mb-4 last:mb-0">
      <span className="text-sm text-gray-500">
        {label}
      </span>

      <label className="relative inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          defaultChecked={enabled}
          className="sr-only peer"
        />
        <div className="w-11 h-6 bg-gray-200 rounded-full peer peer-checked:bg-teal-400
          after:content-[''] after:absolute after:top-0.5 after:left-0.5 
          after:bg-white after:h-5 after:w-5 after:rounded-full 
          after:transition-all peer-checked:after:translate-x-5">
        </div>
      </label>
    </div>
  );
}
