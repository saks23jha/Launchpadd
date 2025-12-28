'use client';

import Image from 'next/image';

export default function ProjectsTable() {
  const projects = [
    {
      name: 'Chakra Soft UI Version',
      logo: '/xd.svg',
      budget: '$14,000',
      status: 'Working',
      progress: 60,
    },
    {
      name: 'Add Progress Track',
      logo: '/atlassian.svg',
      budget: '$3,000',
      status: 'Canceled',
      progress: 10,
    },
    {
      name: 'Fix Platform Errors',
      logo: '/slack.svg',
      budget: 'Not set',
      status: 'Done',
      progress: 100,
    },
    {
      name: 'Launch our Mobile App',
      logo: '/spotify.svg',
      budget: '$32,000',
      status: 'Done',
      progress: 100,
    },
    {
      name: 'Add the New Pricing Page',
      logo: '/jira.svg',
      budget: '$400',
      status: 'Working',
      progress: 25,
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      {/* Header */}
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Projects</h2>
        <p className="text-sm text-gray-400">✅ 30 done this month</p>
      </div>

      {/* Table */}
      <table className="w-full border-collapse">
        <thead>
          <tr className="text-left text-xs text-gray-400 uppercase border-b">
            <th className="pb-3">Companies</th>
            <th className="pb-3">Budget</th>
            <th className="pb-3">Status</th>
            <th className="pb-3">Completion</th>
            <th className="pb-3"></th>
          </tr>
        </thead>

        <tbody>
          {projects.map((p, index) => (
            <tr
              key={index}
              className="border-b last:border-none"
            >
              {/* Company */}
              <td className="py-4">
                <div className="flex items-center gap-3">
                  <Image
                    src={p.logo}
                    alt={p.name}
                    width={32}
                    height={32}
                    className="rounded-md"
                  />
                  <span className="font-medium text-gray-800">
                    {p.name}
                  </span>
                </div>
              </td>

              {/* Budget */}
              <td className="py-4 text-sm font-bold text-gray-600">
                {p.budget}
              </td>

              {/* Status */}
              <td className="py-4">
                <span
                  className={`text-sm font-bold ${
                    p.status === 'Done'
                      ? 'text-black-500'
                      : p.status === 'Working'
                      ? 'text-black-500'
                      : 'text-black-400'
                  }`}
                >
                  {p.status}
                </span>
              </td>

              {/* Completion */}
              <td className="py-4 w-48">
                <div className="flex flex-col gap-1">
                  <span className="text-xs font-medium text-gray-600">
                    {p.progress}%
                  </span>
                  <div className="w-full h-2 bg-gray-200 rounded-full">
                    <div
                      className="h-2 bg-teal-400 rounded-full transition-all"
                      style={{ width: `${p.progress}%` }}
                    />
                  </div>
                </div>
              </td>

              {/* Options */}
              <td className="py-4 text-gray-400 text-lg cursor-pointer">
                ⋮
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
