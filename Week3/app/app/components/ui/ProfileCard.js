'use client';

import Image from 'next/image';

export default function ProfileCard() {
    return (
        <div className="bg-white rounded-xl shadow-md p-7 flex flex-col md:flex-row md:items-center justify-between gap-4 overflow-visible">

            {/* Left */}
            <div className="flex items-center gap-4">

                {/* Avatar Wrapper */}
                <div className="relative overflow-visible">
                    <Image
                        src="/ImageA1.svg"
                        alt="Esthera Jackson"
                        width={60}
                        height={60}
                        className="rounded-xl"
                    />

                    {/* Pen Icon */}
                    <div className="absolute -bottom-2 -right-2 z-10 w-9 h-9 bg-white rounded-full flex items-center justify-center shadow-md cursor-pointer">
                        <Image
                            src="/pen.svg"
                            alt="Edit profile"
                            width={20}
                            height={20}
                        />
                    </div>

                </div>

                {/* Text */}
                <div>
                    <h2 className="font-semibold text-gray-800">
                        Esthera Jackson
                    </h2>
                    <p className="text-sm text-gray-400">
                        esthera@simmple.com
                    </p>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-2">

                {/* Overview (active) */}
                <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-100 text-sm font-medium text-gray-900">
                    <Image src="/overview.svg" alt="Overview" width={16} height={16} />
                    <span>Overview</span>
                </button>

                {/* Teams */}
                <button className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900">
                    <Image src="/teams.svg" alt="Teams" width={16} height={16} />
                    <span>Teams</span>
                </button>

                {/* Projects */}
                <button className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900">
                    <Image src="/projects.svg" alt="Projects" width={16} height={16} />
                    <span>Projects</span>
                </button>
            </div>
        </div>
    );
}
