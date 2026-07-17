import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                         {/* Doors (Tiers) */}
                         {Array.from({ length: lockerTiers }).map((_, tIdx) => {
                           const tierHeight = computedLockerHeight / lockerTiers;
                           const tierY = tIdx * tierHeight;
                           const pad = 4;
                           return (
                             <g key={`door-${cIdx}-${tIdx}`}>
                               <rect 
                                 x={colX + pad} 
                                 y={tierY + pad} 
                                 width={colWidth - pad*2} 
                                 height={tierHeight - pad*2} 
                                 fill="#cbd5e1" 
                                 stroke="#94a3b8" 
                                 strokeWidth="2" 
                                 rx="2"
                               />
                               {/* Louvers / Vents */}
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                               <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />

                               {/* Lock / Handle */}
                               <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                               <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2" fill="#475569" />
                             </g>
                           )
                         })}"""

replacement = """                         {/* Doors (Tiers) */}
                         {Array.from({ length: lockerTiers }).map((_, tIdx) => {
                           const tierHeight = computedLockerHeight / lockerTiers;
                           const tierY = tIdx * tierHeight;
                           const pad = 4;
                           const doorId = `${cIdx}-${tIdx}`;
                           const isRemoved = removedLockerDoors.includes(doorId);
                           
                           return (
                             <g 
                               key={`door-${cIdx}-${tIdx}`} 
                               onClick={() => {
                                 setRemovedLockerDoors(prev => 
                                   prev.includes(doorId) ? prev.filter(id => id !== doorId) : [...prev, doorId]
                                 );
                               }}
                               className="cursor-pointer hover:opacity-80 transition-opacity"
                             >
                               {/* Always draw horizontal shelf line if it's not the top/bottom tier */}
                               {tIdx > 0 && <line x1={colX} y1={tierY} x2={colX + colWidth} y2={tierY} stroke="#94a3b8" strokeWidth="2" />}
                               
                               <rect 
                                 x={colX + pad} 
                                 y={tierY + pad} 
                                 width={colWidth - pad*2} 
                                 height={tierHeight - pad*2} 
                                 fill={isRemoved ? "#e2e8f0" : "#cbd5e1"}
                                 fillOpacity={isRemoved ? 0.3 : 1}
                                 stroke={isRemoved ? "#94a3b8" : "#94a3b8"} 
                                 strokeWidth="2" 
                                 strokeDasharray={isRemoved ? "4 4" : "none"}
                                 rx="2"
                               />
                               
                               {!isRemoved && (
                                 <>
                                   {/* Louvers / Vents */}
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
    
                                   {/* Lock / Handle */}
                                   <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                                   <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2" fill="#475569" />
                                 </>
                               )}
                               
                               {/* Hover / hint overlay */}
                               <title>{isRemoved ? "Click to add door" : "Click to remove door"}</title>
                             </g>
                           )
                         })}"""

content = content.replace(target, replacement, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

