
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
    const pathname = usePathname();

    const navItems = [
        { label: "Dashboard", href: "/dashboard", icon: "/dashboard.svg" },
        { label: "Profile", href: "/profile", icon: "/profile.svg" },
        { label: "Sign Up", href: "/signup", icon: "/signup.svg" },
        { label: "Sign In", href: "/signin", icon: "/signin.svg" },
    ];

    return (
        <div className="w-full flex justify-center pt-6">
            <div
                className="w-[90%] max-w-6xl flex items-center justify-between px-6 py-3
        rounded-xl shadow-sm border
        bg-gradient-to-r from-white via-white-100"
            >
                {/* LEFT: Logo */}
                <div className="flex items-center gap-2">
                    <img
                        src="/logo.png"
                        alt="Purity UI Logo"
                        className="w-7 h-7 object-contain"
                    />
                    <span className="font-semibold text-sm text-gray-800">
                        PURITY UI DASHBOARD
                    </span>
                </div>

                {/* CENTER: Navigation */}
                <div className="flex items-center gap-8 relative">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;

                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={`relative flex items-center gap-2 text-xs font-semibold
                ${isActive
                                        ? "text-gray-900"
                                        : "text-gray-500 hover:text-gray-700"
                                    }`}
                            >
                                {/* ICON */}
                                <img
                                    src={item.icon}
                                    alt={item.label}
                                    className="w-4 h-4"
                                />

                                {/* TEXT */}
                                <span>{item.label}</span>

                                {/* Active underline */}
                                {isActive && (
                                    <span
                                        className={`absolute -bottom-4 left-0 w-full h-[3px] rounded-full transition-opacity
                                            ${isActive ? "bg-blue-500 opacity-100" : "opacity-0"}`}
                                    />

                                )}
                            </Link>
                        );
                    })}
                </div>

                {/* RIGHT: Button */}
                <button
                    className="bg-gray-800 text-white text-xs font-semibold
          px-4 py-2 rounded-full hover:bg-gray-700 transition"
                >
                    Free Download
                </button>
            </div>
        </div>
    );
}
