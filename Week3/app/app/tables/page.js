'use client';

import Sidebar from "../components/ui/Sidebar";
import Navbar from "../components/ui/Navbar";
import AuthorsTable from "../components/ui/AuthorsTable";
import ProjectsTable from "../components/ui/ProjectsTable";
import Footer from "../components/ui/Footer";


export default function TablesPage() {
  return (
    <div className="flex min-h-screen bg-[#f8f9fa]">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        <Navbar />

        <main className="p-6 space-y-8">
          <AuthorsTable />
          <ProjectsTable />
        </main>
        <Footer />
      </div>
    </div>
  );
}
