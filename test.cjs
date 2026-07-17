const fs = require('fs');
const content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');
const ts = require('typescript');
const sourceFile = ts.createSourceFile('test.tsx', content, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);

function getLineAndChar(pos) {
    const { line, character } = sourceFile.getLineAndCharacterOfPosition(pos);
    return `${line + 1}:${character + 1}`;
}

// Just print parse errors from sourceFile
sourceFile.parseDiagnostics.forEach(diagnostic => {
    const { line, character } = sourceFile.getLineAndCharacterOfPosition(diagnostic.start);
    console.log(`Parse Error at ${line + 1}:${character + 1}: ${diagnostic.messageText}`);
});
