const fs = require('fs');
const content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
let dq = 0, sq = 0, bq = 0;
for (const c of content) {
    if (c === '"') dq++;
    if (c === "'") sq++;
    if (c === '`') bq++;
}
console.log(`Double: ${dq}, Single: ${sq}, Backtick: ${bq}`);
