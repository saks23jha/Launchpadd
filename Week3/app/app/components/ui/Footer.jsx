export default function Footer() {
  return (
    <footer className="w-full  py-4 text-xs text-gray-400">
      <div className="max-w-6xl mx-auto flex items-center justify-between px-6">
        <p>
          © 2021, Made with ❤️ by{" "}
          <span className="text-teal-400 font-medium">Creative Tim</span>{" "}
          &amp;{" "}
          <span className="text-teal-400 font-medium">Simmmple</span>{" "}
          for a better web
        </p>

        <div className="flex gap-6">
          <span>Creative Tim</span>
          <span>Simmmple</span>
          <span>Blog</span>
          <span>License</span>
        </div>
      </div>
    </footer>
  );
}
