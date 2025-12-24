
export default function Hero() {
  return (
    <section className="bg-gradient-to-b from-white to-gray-100 min-h-[90vh] flex items-center">

      <div className="max-w-4xl mx-auto px-6 text-center">

        {/* Heading */}
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
          Manage Your Business <br />
          With Smart Dashboard
        </h1>

        {/* Subtitle */}
        <p className="text-gray-600 text-lg mb-10">
          Track projects, sales, and performance using a fast,
          modern dashboard built with Next.js and Tailwind CSS.
        </p>

        {/* Buttons */}
        <div className="flex justify-center gap-4">
          <a
            href="/dashboard"
            className="px-6 py-3 bg-teal-500 text-white rounded-lg font-semibold hover:bg-teal-600 transition"
          >
            Go to Dashboard
          </a>

          <a
            href="/about"
            className="px-6 py-3 border border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-100 transition"
          >
            Learn More
          </a>
        </div>
      </div>
    </section>
  );
}
