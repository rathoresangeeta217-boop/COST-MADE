const fs = require('fs');

let content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

// Add a helper text in the full screen drawing view
content = content.replace(
  /\{isFullScreenDrawing \? <Minimize className="w-4 h-4" \/> : <Maximize className="w-4 h-4" \/>\}/,
  `{isFullScreenDrawing ? <Minimize className="w-4 h-4" /> : <Maximize className="w-4 h-4" />}
                </button>
              </div>
              {isFullScreenDrawing && (
                <div className="absolute top-6 left-1/2 -translate-x-1/2 bg-slate-800 text-slate-300 text-xs px-4 py-2 rounded-full shadow-lg z-[101] pointer-events-none">
                  Interactive Mode: Click on doors to open/close them. Click on internal shelf lines to remove/restore them.
                </div>
              )}
              <div className={isFullScreenDrawing ? "flex-1 overflow-auto flex items-center justify-center p-8" : "w-full h-full overflow-hidden"}>`
);

fs.writeFileSync('src/pages/CustomStorageCalculator.tsx', content);
console.log("Updated instructions!");
