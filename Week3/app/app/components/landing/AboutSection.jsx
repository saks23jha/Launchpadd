
import Link from "next/link";

export default function AboutSection() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-5xl mx-auto px-6 text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">
          About This Project
        </h2>

        <p className="text-gray-600 max-w-2xl mx-auto mb-8">
          This dashboard demonstrates a real-world Next.js architecture
          with proper routing, layouts, and reusable UI components.
        </p>

        <Link
          href="/about"
          className="inline-block px-6 py-3 bg-slate-900 text-white rounded-lg hover:bg-slate-800 transition"
        >
          Read More About Project →
        </Link>
      </div>
    </section>
  );
}
