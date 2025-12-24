export default function AboutPage() {
  return (
    <main className="min-h-screen bg-gray-50 py-20 px-6">
      <div className="max-w-4xl mx-auto bg-white p-10 rounded-2xl shadow-sm">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          About This Dashboard
        </h1>

        <p className="text-gray-600 mb-4">
          This application is built using Next.js App Router,
          Tailwind CSS, and component-driven architecture.
        </p>

        <p className="text-gray-600 mb-4">
          The landing page introduces the app, while the dashboard
          is separated using layouts to maintain clean UI boundaries.
        </p>

        <p className="text-gray-600">
          This structure mirrors how real SaaS products are built.
        </p>
      </div>
    </main>
  );
}
