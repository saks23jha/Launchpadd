
'use client';

import PurityNav from '../components/ui/PurityNav';
import Footer from '../components/ui/Footer';

export default function SignIn() {
  return (
    <div className="min-h-screen flex flex-col bg-white">

      {/* TOP NAV */}
      <PurityNav />

      {/* MAIN CONTENT */}
      <main className="flex-grow">
        <div className="flex pt-28">

          {/* LEFT */}
          <div className="w-[55%] flex items-center justify-center">
            <div className="w-[380px]">
              <h1 className="text-3xl font-bold text-teal-400 mb-2">
                Welcome Back
              </h1>

              <p className="text-sm text-gray-400 font-semibold mb-8">
                Enter your email and password to sign in
              </p>

              <div className="space-y-5">
                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder="Email"
                    className="w-full px-4 py-3 placeholder-gray-400 focus:outline-none
                               border border-gray-200 focus:ring-2 focus:ring-teal-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-600">
                    Password
                  </label>
                  <input
                    type="password"
                    placeholder="Password"
                    className="w-full px-4 py-3 placeholder-gray-400 focus:outline-none
                               border border-gray-200 focus:ring-2 focus:ring-teal-300 rounded-lg"
                  />
                </div>

                <button className="w-full bg-teal-400 text-white py-3 rounded-lg font-semibold">
                  SIGN IN
                </button>
                {/* Sign up text */}
                <p className="mt-4 text-sm text-gray-400 text-center">
                  Don&apos;t have an account?{" "}
                  <a
                    href="/signup"
                    className="text-teal-400 font-semibold hover:underline"
                  >
                    Sign up
                  </a>
                </p>

              </div>
            </div>
          </div>

          {/* RIGHT */}
          <div className="w-[45%] flex items-center justify-center">
            <img
              src="/chakra.svg"
              alt="chakra"
              className="w-[80%]"
            />
          </div>

        </div>
      </main>

      {/* FOOTER */}
      <Footer />

    </div>
  );
}
