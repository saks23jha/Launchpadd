'use client';

import Image from 'next/image';

export default function AuthorsTable() {
  const authors = [
    {
      name: 'Esthera Jackson',
      email: 'esthera@simmple.com',
      image: '/ImageA1.svg',
      role: 'Manager',
      dept: 'Organization',
      status: 'Online',
      date: '14/06/21',
    },
    {
      name: 'Alexa Liras',
      email: 'alexa@simmple.com',
      image: '/ImageA2.svg',
      role: 'Programmer',
      dept: 'Developer',
      status: 'Offline',
      date: '14/06/21',
    },
    {
        
      name: 'Laurent Michael',
      email: 'laurent@simmple.com',
      image: '/ImageA3.svg',
      role: 'Executive',
      dept: 'Projects',
      status: 'Online',
      date: '14/06/21',
    },
    {
      name: 'Freduardo Hill',
      email: 'freduardo@simmple.com',
      image: '/ImageA4.svg',
      role: 'Manager',
      dept: 'Organization',
      status: 'Online',
      date: '14/06/21',
    },
    {
      name: 'Daniel Thomas',
      email: 'daniel@simmple.com',
      image: '/ImageA5.svg',
      role: 'Programmer',
      dept: 'Developer',
      status: 'Offline',
      date: '14/06/21',
    },
    {
      name: 'Mark Wilson',
      email: 'mark@simmple.com',
      image: '/ImageA6.svg',
      role: 'Designer',
      dept: 'UI/UX Design',
      status: 'Offline',
      date: '14/06/21',
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h2 className="font-bold text-black-800 mb-4">
        Authors Table
      </h2>

      <table className="w-full">
        <thead>
          <tr className="text-left text-xs text-gray-400 uppercase border-b">
            <th className="pb-3">Author</th>
            <th className="pb-3">Function</th>
            <th className="pb-3">Status</th>
            <th className="pb-3">Employed</th>
            <th className="pb-3"></th>
          </tr>
        </thead>

        <tbody>
          {authors.map((a, index) => (
            <tr key={index} className="border-b last:border-none">
              {/* Author */}
              <td className="py-4">
                <div className="flex items-center gap-3">
                  <Image
                    src={a.image}
                    alt={a.name}
                    width={40}
                    height={40}
                    className="rounded-full object-cover"
                  />
                  <div>
                    <p className="font-medium text-gray-800">
                      {a.name}
                    </p>
                    <p className="text-sm text-gray-400">
                      {a.email}
                    </p>
                  </div>
                </div>
              </td>

              {/* Function */}
              <td className="py-4">
                <p className="font-bold text-black-800">{a.role}</p>
                <p className="text-sm text-gray-400">{a.dept}</p>
              </td>

              {/* Status */}
              <td className="py-4">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-big ${
                    a.status === 'Online'
                      ? 'bg-green-100 text-green-600'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {a.status}
                </span>
              </td>

              {/* Employed */}
              <td className="py-4 text-sm text-black-600 font-black">
                {a.date}
              </td>

              {/* Edit */}
              <td className="py-4 text-sm text-black cursor-pointer">
                Edit
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
