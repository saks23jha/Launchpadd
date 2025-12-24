import StatsSection from "./components/StatsSection";
import SalesOverview from "./components/SalesOverview";
import OrdersOverview from "./components/OrdersOverview";

import { FiUsers, FiSend, FiShoppingCart, FiBox } from "react-icons/fi";


export default function DashboardPage() {
    return (
        <div className="space-y-6">
            {/* TOP STATS */}
            <StatsSection />

            {/* PROMO CARDS */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <OrdersOverview />

                {/* Work with the Rockets */}
                <div className="bg-white rounded-2xl p-3">
                    <div className="relative h-[260px] rounded-xl overflow-hidden">
                        <img
                            src="/Background.png"
                            alt="Work with the Rockets"
                            className="absolute inset-0 w-full h-full object-cover"
                        />

                        <div className="relative z-10 p-6 flex flex-col h-full">
                            <h3 className="text-white text-lg font-semibold">
                                Work with the Rockets
                            </h3>

                            <p className="text-white text-sm mt-2 max-w-sm">
                                Wealth creation is an evolutionarily recent positive-sum game.
                                It is all about who take the opportunity first.
                            </p>

                            <div className="mt-auto">
                                <button className="text-white text-sm font-medium hover:underline">
                                    Read more →
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* BOTTOM CHARTS */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* LEFT – Active Users */}
                <div className="xl:col-span-1">
                    <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
                        {/* Chart */}
                        <div className="h-[180px] bg-gradient-to-br from-slate-900 to-slate-700 rounded-t-2xl flex items-center justify-center" >
                            <img
                                src="/Graph.svg"
                                alt="Active Users Graph"
                                className="w-full h-full object-contain p-4"
                            />
                        </div>

                        <div className="p-5">
                            <h4 className="font-semibold text-gray-800">Active Users</h4>
                            <p className="text-sm text-green-500 mt-1">
                                (+23) than last week
                            </p>

                            {/* STATS */}
                            <div className="grid grid-cols-4 gap-4 mt-6 text-sm">
                                {/* Users */}
                                <div>
                                    <div className="flex items-center gap-2 text-gray-500">
                                        <div className="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center text-white">
                                            <FiUsers size={16} />
                                        </div>
                                        <span>Users</span>
                                    </div>

                                    <p className="font-semibold text-gray-800 mt-1">
                                        32,984
                                    </p>
                                    <div className="h-[2px] bg-teal-400 mt-2 rounded-full" />
                                </div>

                                {/* Clicks */}
                                <div>
                                    <div className="flex items-center gap-2 text-gray-500">
                                        <div className="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center text-white">
                                            <FiSend size={16} />
                                        </div>
                                        <span>Clicks</span>
                                    </div>

                                    <p className="font-semibold text-gray-800 mt-1">
                                        2.42m
                                    </p>
                                    <div className="h-[2px] bg-teal-400 mt-2 rounded-full" />
                                </div>

                                {/* Sales */}
                                <div>
                                    <div className="flex items-center gap-2 text-gray-500">
                                        <div className="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center text-white">
                                            <FiShoppingCart size={16} />
                                        </div>
                                        <span>Sales</span>
                                    </div>

                                    <p className="font-semibold text-gray-800 mt-1">
                                        2,400$
                                    </p>
                                    <div className="h-[2px] bg-teal-400 mt-2 rounded-full" />
                                </div>

                                {/* Items */}
                                <div>
                                    <div className="flex items-center gap-2 text-gray-500">
                                        <div className="w-8 h-8 rounded-lg bg-teal-400 flex items-center justify-center text-white">
                                            <FiBox size={16} />
                                        </div>
                                        <span>Items</span>
                                    </div>

                                    <p className="font-semibold text-gray-800 mt-1">
                                        320
                                    </p>
                                    <div className="h-[2px] bg-teal-400 mt-2 rounded-full" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* RIGHT – Sales Overview */}
                <div className="xl:col-span-2">
                    <div className="bg-white rounded-2xl shadow-sm p-5 h-full">
                        <div className="mb-4">
                            <h4 className="font-semibold text-black-800">
                                Sales overview
                            </h4>
                            <p className="text-sm text-green-500">
                                (+5) more in 2021
                            </p>
                        </div>

                        <div className="h-[260px] flex items-center justify-center">
                            <img
                                src="/Graph(1).png"
                                alt="   Sales Overview Graph"
                                className="w-full  h-full object-contain"
                            />
                        </div>
                    </div>
                </div>
            </div>
            {/* ================= PROJECTS + ORDERS ================= */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

                {/* ================= PROJECTS (LEFT) ================= */}
                <div className="bg-white rounded-2xl p-6 xl:col-span-2 shadow-sm">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-semibold text-gray-800">Projects</h3>
                            <p className="text-sm text-green-500">✔ 30 done this month</p>
                        </div>
                        <span className="text-gray-400 cursor-pointer">⋮</span>
                    </div>

                    {/* Table Head */}
                    <div className="grid grid-cols-12 text-xs text-gray-400 font-semibold pb-3 border-b border-gray-100">
                        <div className="col-span-5">COMPANIES</div>
                        <div className="col-span-3 text-center">MEMBERS</div>
                        <div className="col-span-2 text-center">BUDGET</div>
                        <div className="col-span-2">COMPLETION</div>
                    </div>

                    {/* Rows */}
                    {[
                        {
                            name: "Chakra Soft UI Version",
                            logo: "/xd.svg",
                            budget: "$14,000",
                            progress: 60,
                            members: ["/Members.png", "/M2.png"],
                        },
                        {
                            name: "Add Progress Track",
                            logo: "/atlassian.svg",
                            budget: "$3,000",
                            progress: 10,
                            members: ["/M5.png", "/M6.png"],
                        },
                        {
                            name: "Fix Platform Errors",
                            logo: "/slack.svg",
                            budget: "Not set",
                            progress: 100,
                            members: ["/M5.png", "/M6.png", "/M3.png"],
                        },
                        {
                            name: "Launch our Mobile App",
                            logo: "/spotify.svg",
                            budget: "$32,000",
                            progress: 100,
                            members: ["/Members.png", "/M2.png"],
                        },
                        {
                            name: "Add the New Pricing Page",
                            logo: "/diamond.svg",
                            budget: "$400",
                            progress: 25,
                            members: ["/M3.png", "/M4.png"],
                        },
                        {
                            name: "Redesign New Online Shop",
                            logo: "/linkedin.svg",
                            budget: "$7,600",
                            progress: 40,
                            members: ["/M6.png"],
                        },
                    ].map((project, idx) => (
                        <div
                            key={idx}
                            className="grid grid-cols-12 items-center py-4 border-b last:border-none"
                        >
                            {/* Company */}
                            <div className="col-span-5 flex items-center gap-3">
                                <img src={project.logo} className="w-8 h-8 rounded-lg" />
                                <span className="font-medium text-gray-800">{project.name}</span>
                            </div>

                            {/* Members */}
                            <div className="col-span-3 flex justify-center">
                                <div className="flex -space-x-3">
                                    {project.members.map((m, i) => (
                                        <img
                                            key={i}
                                            src={m}
                                            className="w-8 h-8 rounded-full border-2 border-white object-cover"
                                        />
                                    ))}

                                </div>
                            </div>

                            {/* Budget */}
                            <div className="col-span-2 text-center text-sm font-semibold text-gray-700">
                                {project.budget}
                            </div>

                            {/* Completion */}
                            <div className="col-span-2 flex items-center gap-2">
                                <span className="text-xs text-gray-600">{project.progress}%</span>
                                <div className="w-full h-1.5 bg-gray-200 rounded-full">
                                    <div
                                        className="h-1.5 bg-teal-400 rounded-full"
                                        style={{ width: `${project.progress}%` }}
                                    />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
                {/* ================= ORDERS OVERVIEW (RIGHT) ================= */}
                <div className="bg-white rounded-2xl p-6 shadow-sm">

                    {/* Header */}
                    <div className="mb-6">
                        <h3 className="text-lg font-semibold text-gray-800">
                            Orders overview
                        </h3>
                        <p className="text-sm text-green-500">+30% this month</p>
                    </div>

                    {/* Timeline */}
                    <div className="space-y-5">
                        {[
                            {
                                title: "$2400, Design changes",
                                time: "22 DEC 7:20 PM",
                                Icon: "/Icon1.png",
                            },
                            {
                                title: "New order #4219423",
                                time: "21 DEC 11:21 PM",
                                Icon: "/Icon2.png",
                            },
                            {
                                title: "Server Payments for April",
                                time: "21 DEC 9:28 PM",
                                Icon: "/Icon3.png",
                            },
                            {
                                title: "New card added for order #3210145",
                                time: "20 DEC 3:52 PM",
                                Icon: "/Icon4.png",
                            },
                            {
                                title: "Unlock packages for Development",
                                time: "19 DEC 11:35 PM",
                                Icon: "/Icon5.png",
                            },
                            {
                                title: "New order #9851258",
                                time: "18 DEC 4:41 PM",
                                Icon: "/Icon6.png",
                            },
                        ].map((item, idx) => (
                            <div key={idx} className="flex items-start gap-4">

                                <img
                                    src={item.Icon}
                                    alt="icon"
                                    className="w-6 h-6 mt-1"
                                />

                                {/* Content */}
                                <div>
                                    <p className="text-sm font-medium text-gray-800">
                                        {item.title}
                                    </p>
                                    <p className="text-xs text-gray-400">
                                        {item.time}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

