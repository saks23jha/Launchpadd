'use client';

import Sidebar from '../components/ui/Sidebar';
import Navbar from '../components/ui/Navbar';
import Footer from '../components/ui/Footer';

import ProfileCard from '../components/ui/ProfileCard';
import ProfileHero from '../components/ui/ProfileHero';

import PlatformSettings from '../components/ui/PlatformSettings';
import ProfileInfo from '../components/ui/ProfileInfo';
import Conversations from '../components/ui/Conversations';
import ProjectsGrid from '../components/ui/ProjectsGrid';

export default function ProfilePage() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* SIDEBAR */}
      <Sidebar />

      {/* MAIN CONTENT */}
      <div className="flex-1 relative">
        {/* TEAL HEADER WITH NAVBAR */}
        <div className="relative h-[300px] bg-gradient-to-r from-teal-400 to-teel-400 rounded-b-2xl">
          
          {/* NAVBAR INSIDE TEAL */}
          <div className="absolute top-0 left-0 w-full z-30">
            <Navbar />
          </div>

          {/* PAGE TITLE */}
          <div className="pt-24 px-6 text-white">
            <p className="text-sm opacity-80"></p>
            <h1 className="text-2xl font-semibold"></h1>
          </div>
        </div>

        {/* FLOATING PROFILE CARD */}
        <div className="-mt-24 px-6 relative z-20">
          <ProfileCard />
        </div>

        {/* MAIN GRID CONTENT */}
        <div className="px-6 mt-10 grid grid-cols-1 xl:grid-cols-3 gap-6">
          <PlatformSettings />
          <ProfileInfo />
          <Conversations />
        </div>

        {/* PROJECTS SECTION */}
        <div className="px-6 mt-8">
          <ProjectsGrid />
        </div>

        {/* FOOTER */}
        <div className="mt-10 px-6">
          <Footer />
        </div>
      </div>
    </div>
  );
}
