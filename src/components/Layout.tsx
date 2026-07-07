import { Link, Outlet } from 'react-router-dom';
import { Pickaxe, Home, LogIn, LogOut, Cloud, FileDown } from 'lucide-react';
import { downloadHardwarePdf } from '../lib/downloadHardwarePdf';
import { useFirestoreSync } from '../lib/useFirestoreSync';
import { useAuth } from '../lib/AuthContext';

export default function Layout() {
  useFirestoreSync();
  const { user, signInWithGoogle, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-gray-900 group">
            <div className="bg-indigo-600 text-white p-2 rounded-lg group-hover:bg-indigo-700 transition-colors">
              <Pickaxe className="w-5 h-5" />
            </div>
            <span className="font-semibold text-lg tracking-tight">Cost Calculator</span>
          </Link>
          <nav className="flex items-center gap-6">
            <Link
              to="/"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Home className="w-4 h-4" />
              Products
            </Link>
            <Link
              to="/rules"
              className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              <Pickaxe className="w-4 h-4" />
              Pricing Rules
            </Link>
            
            <button
              onClick={downloadHardwarePdf}
              className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors bg-indigo-50 px-3 py-1.5 rounded-md"
            >
              <FileDown className="w-4 h-4" />
              Hardware Rates
            </button>

            <div className="w-px h-6 bg-gray-200"></div>

            {user ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Cloud className="w-4 h-4 text-emerald-500" />
                  <span className="hidden sm:inline">Synced</span>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={signInWithGoogle}
                className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors"
              >
                <LogIn className="w-4 h-4" />
                Sign in to Sync
              </button>
            )}
          </nav>
        </div>
      </header>
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        <Outlet />
      </main>

      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} Cost Calculator. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
