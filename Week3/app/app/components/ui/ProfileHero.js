'use client';

export default function ProfileHero() {
  return (
    <div className="relative h-[260px] rounded-b-2xl bg-gradient-to-r from-teal-400 to-cyan-400 overflow-hidden">
      
      {/* Waves */}
      <div className="absolute inset-0 opacity-30 bg-[url('/waves.svg')] bg-cover bg-center" />

      {/* Breadcrumb */}
      <div className="relative z-10 px-6 pt-6 text-white">
        <p className="text-white font-bold black ">Pages / Profile</p>
        <h1 className="text-xl font-bold">Profile</h1>
      </div>
    </div>
  );
}
