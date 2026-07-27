with open('src/components/Layout.tsx', 'r') as f:
    content = f.read()

old_auth = """            <div className="w-px h-6 bg-gray-200"></div>
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
            )}"""

new_auth = """            <div className="w-px h-6 bg-gray-200"></div>
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Cloud className="w-4 h-4 text-emerald-500" />
              <span className="hidden sm:inline">Live Sync</span>
            </div>"""

content = content.replace(old_auth, new_auth)
with open('src/components/Layout.tsx', 'w') as f:
    f.write(content)
