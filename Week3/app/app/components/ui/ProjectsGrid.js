'use client';

import Image from 'next/image';

const projects = [
  {
    id: 1,
    image: '/p1.svg',
    title: 'Modern',
    description:
      'As Uber works through a huge amount of internal management turmoil.',
  },
  {
    id: 2,
    image: '/p2.svg',
    title: 'Scandinavian',
    description:
      'Music is something that every person has his or her own specific opinion about.',
  },
  {
    id: 3,
    image: '/p3.svg',
    title: 'Minimalist',
    description:
      'Different people have different taste, and various types of music.',
  },
];

export default function Projects() {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      
      {/* Header */}
      <h2 className="text-lg font-semibold text-gray-800">
        Projects
      </h2>
      <p className="text-sm text-gray-400 mb-6">
        Architects design houses
      </p>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        {/* Project Cards */}
        {projects.map((project) => (
          <div
            key={project.id}
            className="bg-white rounded-xl"
          >
            {/* Image */}
            <Image
              src={project.image}
              alt={project.title}
              width={400}
              height={240}
              className="rounded-xl object-cover"
            />

            {/* Content */}
            <div className="mt-4">
              <p className="text-xs text-gray-400 mb-1">
                Project #{project.id}
              </p>

              <h3 className="font-semibold text-gray-800 mb-2">
                {project.title}
              </h3>

              <p className="text-sm text-gray-400 mb-4">
                {project.description}
              </p>

              {/* Footer row */}
              <div className="flex items-center justify-between">
                
                {/* View All Button */}
                <button className="text-xs font-semibold text-teal-500 border border-teal-400 rounded-full px-4 py-1 hover:bg-teal-50">
                  VIEW ALL
                </button>

                {/* Avatars */}
                <div className="flex -space-x-3">
                  <Image
                    src="/M2.png"
                    alt="Member"
                    width={32}
                    height={32}
                    className="rounded-full border-2 border-white shadow-sm"
                  />
                  <Image
                    src="/M3.png"
                    alt="Member"
                    width={32}
                    height={32}
                    className="rounded-full border-2 border-white shadow-sm"
                  />
                  <Image
                    src="/M4.png"
                    alt="Member"
                    width={32}
                    height={32}
                    className="rounded-full border-2 border-white shadow-sm"
                  />
                </div>

              </div>
            </div>
          </div>
        ))}

        {/* Create New Project */}
        <div className="flex flex-col items-center justify-center border border-dashed rounded-xl text-gray-400 hover:text-gray-600 cursor-pointer">
          <div className="text-3xl mb-2">+</div>
          <p className="font-medium">Create a New Project</p>
        </div>

      </div>
    </div>
  );
}
