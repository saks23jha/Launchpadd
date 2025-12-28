'use client';

import Image from 'next/image';

export default function Conversations() {
  const chats = [
    {
      name: 'Esthera Jackson',
      message: 'Hi! I need more informations...',
      image: '/ImageA1.svg',
    },
    {
      name: 'Esthera Jackson',
      message: 'Awesome work, can you change...',
      image: '/ImageA2.svg',
    },
    {
      name: 'Esthera Jackson',
      message: 'Have a great afternoon...',
      image: '/ImageA3.svg',
    },
    {
      name: 'Esthera Jackson',
      message: 'About files I can...',
      image: '/ImageA4.svg',
    },
  ];

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <h3 className="font-semibold text-gray-800 mb-4">
        Conversations
      </h3>

      <div className="space-y-4">
        {chats.map((chat, i) => (
          <div key={i} className="flex items-center gap-3">
            <Image
              src={chat.image}
              alt={chat.name}
              width={40}
              height={40}
              className="rounded-full"
            />
            <div className="flex-1">
              <p className="font-medium text-sm text-gray-800">
                {chat.name}
              </p>
              <p className="text-xs text-gray-400">
                {chat.message}
              </p>
            </div>
            <span className="text-xs text-teal-400 cursor-pointer">
              REPLY
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
