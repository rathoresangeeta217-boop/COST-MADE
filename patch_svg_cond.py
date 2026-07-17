import re

with open('src/pages/CustomStorageCalculator.tsx', 'r') as f:
    content = f.read()

target = """                               {!isRemoved && (
                                 <>
                                   {/* Louvers / Vents */}
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                   <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
    
                                   {/* Lock / Handle */}
                                   <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                                   <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2" fill="#475569" />
                                 </>
                               )}"""

replace = """                               {!isRemoved && (
                                 <>
                                   {/* Louvers / CNC Design */}
                                   {lockerCncDesign ? (
                                     <g>
                                       {/* Simulate CNC perforations */}
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 25} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 35} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 - 10} cy={tierY + 45} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2} cy={tierY + 45} r="2" fill="#64748b" />
                                       <circle cx={colX + colWidth/2 + 10} cy={tierY + 45} r="2" fill="#64748b" />
                                     </g>
                                   ) : (
                                     <g>
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 20} x2={colX + colWidth/2 + 15} y2={tierY + 20} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 26} x2={colX + colWidth/2 + 15} y2={tierY + 26} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                       <line x1={colX + colWidth/2 - 15} y1={tierY + 32} x2={colX + colWidth/2 + 15} y2={tierY + 32} stroke="#64748b" strokeWidth="2" strokeLinecap="round" />
                                     </g>
                                   )}
    
                                   {/* Lock / Handle */}
                                   <rect x={colX + colWidth - 25} y={tierY + tierHeight/2 - 20} width="10" height="40" fill="#94a3b8" rx="2" />
                                   
                                   {lockerLockType === "cam" && (
                                     <circle cx={colX + colWidth - 20} cy={tierY + tierHeight/2 - 5} r="2.5" fill="#1e293b" />
                                   )}
                                   {lockerLockType === "padlock" && (
                                     <path d={`M ${colX + colWidth - 23} ${tierY + tierHeight/2 - 5} Q ${colX + colWidth - 20} ${tierY + tierHeight/2 - 10} ${colX + colWidth - 17} ${tierY + tierHeight/2 - 5} L ${colX + colWidth - 17} ${tierY + tierHeight/2} L ${colX + colWidth - 23} ${tierY + tierHeight/2} Z`} fill="none" stroke="#1e293b" strokeWidth="1.5" />
                                   )}
                                   {lockerLockType === "digital" && (
                                     <rect x={colX + colWidth - 23} y={tierY + tierHeight/2 - 12} width="6" height="14" fill="#0f172a" rx="1" />
                                   )}
                                 </>
                               )}"""

content = content.replace(target, replace, 1)

with open('src/pages/CustomStorageCalculator.tsx', 'w') as f:
    f.write(content)

