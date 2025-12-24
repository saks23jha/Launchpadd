// import './globals.css';
// import Navbar from "./components/ui/Navbar.jsx";
// import Sidebar from "./components/ui/Sidebar.jsx";

// export default function RootLayout({ children }) {
//   return (
//     <html lang="en">
//       <body className="bg-gray-50">
//         <div className="flex min-h-screen">
          
//           {/* Sidebar */}
//           <Sidebar />

//           {/* Right side */}
//           <div className="flex flex-col flex-1">
//             <Navbar />
//             <main className="p-6">
//               {children}
//             </main>
//           </div>

//         </div>
//       </body>
//     </html>
//   );
// }
import "./globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        {children}
      </body>
    </html>
  );
}

