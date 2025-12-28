'use client';

import PurityNav from '../components/ui/PurityNav';
import Footer from '../components/ui/Footer';
import Link from 'next/link';

export default function SignUp() {
  return (
    <div className="min-h-screen flex flex-col bg-teel">

     
      <section className="relative h-[420px] bg-[#4FD1C5] text-white">

        
        <div className="absolute top-0 left-0 w-full z-20" >
          <PurityNav />
        </div>

        
        <div className="h-full flex flex-col items-center justify-center text-center px-4">
          <h1 className="text-3xl font-bold mb-2">Welcome!</h1>
          <p className="text-sm max-w-md font-bold opacity-90">
            Use these awesome forms to login or create new account in your project for free.
          </p>
        </div>

      </section>
      <section className="relative flex justify-center">
        <div
          className="
            absolute
            top-[-140px]
            w-full
            flex
            justify-center
            z-10
          "
        >
          <div className="bg-white w-[380px] rounded-2xl shadow-xl px-8 py-8">
            <h2 className="text-center font-semibold text-gray-700 mb-6">
              Register with
            </h2>

         
            <div className="flex justify-center gap-4 mb-4">
              {['/Facebook.svg', '/Apple.svg', '/Google.svg'].map((icon, i) => (
                <div
                  key={i}
                  className="w-14 h-14 border rounded-xl flex items-center justify-center hover:shadow-md transition"
                >
                  <img src={icon} alt="social" className="w-15 h-15" />
                </div>
              ))}
            </div>

            <p className="text-center text-xs text-gray-400 mb-4">or</p>

           
            <div className="space-y-4">
              <div>
                <label className="text-xs text-gray-600 font-medium">
                  Name
                </label>
                <input
                  type="text"
                  placeholder="Your full name"
                  className="w-full mt-1 px-4 py-3 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-300"
                />
              </div>

              <div>
                <label className="text-xs text-gray-600 font-medium">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="Your email address"
                  className="w-full mt-1 px-4 py-3 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-300"
                />
              </div>

              <div>
                <label className="text-xs text-gray-600 font-medium">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Your password"
                  className="w-full mt-1 px-4 py-3 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-300"
                />
              </div>

              <div className="flex items-center gap-2 text-xs text-gray-600">
                <input type="checkbox" />
                <span>Remember me</span>
              </div>

              <button className="w-full bg-[#4FD1C5] text-white py-3 rounded-lg font-semibold text-sm hover:opacity-90 transition">
                SIGN UP
              </button>

              <p className="text-center text-xs text-gray-500">
                Already have an account?{' '}
                <Link href="/signin" className="text-teal-500 font-semibold">
                  Sign in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </section>

     
      <div className="h-[420px]" />

      <Footer />
    </div>
  );
}
