'use client';

import Image from 'next/image';

export default function ProfileInformation() {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6 max-w-md">
      
      {/* Title */}
      <h2 className="text-lg font-semibold text-gray-800 mb-3">
        Profile Information
      </h2>

      {/* Description */}
      <p className="text-sm text-gray-400 leading-relaxed mb-5">
        Hi, I'm Alec Thompson, Decisions: If you can't decide, the answer is no.
        If two equally difficult paths, choose the one more painful in the short
        term (pain avoidance is creating an illusion of equality).
      </p>

      <hr className="mb-5" />

      {/* Info Rows */}
      <InfoRow label="Full Name" value="Alec M. Thompson" />
      <InfoRow label="Mobile" value="(44) 123 1234 123" />
      <InfoRow label="Email" value="alecthompson@mail.com" />
      <InfoRow label="Location" value="United States" />

      {/* Social Media */}
      <div className="flex items-center gap-4 mt-4">
        <span className="text-sm font-medium text-gray-500 w-28">
          Social Media
        </span>

        <div className="flex gap-3">
          <Image src="/facebook.svg" alt="Facebook" width={16} height={16} />
          <Image src="/twitter.svg" alt="Twitter" width={16} height={16} />
          <Image src="/instagram.svg" alt="Instagram" width={16} height={16} />
        </div>
      </div>

    </div>
  );
}

/* 🔹 Reusable Row */
function InfoRow({ label, value }) {
  return (
    <div className="flex items-center gap-4 mb-4">
      <span className="text-sm font-medium text-gray-500 w-28">
        {label}
      </span>
      <span className="text-sm text-gray-700">
        {value}
      </span>
    </div>
  );
}
