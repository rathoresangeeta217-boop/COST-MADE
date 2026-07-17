const fs = require('fs');
const ts = require('typescript');

const content = fs.readFileSync('src/pages/CustomStorageCalculator.tsx', 'utf-8');

const sourceFile = ts.createSourceFile(
    'src/pages/CustomStorageCalculator.tsx',
    content,
    ts.ScriptTarget.Latest,
    true,
    ts.ScriptKind.TSX
);

const program = ts.createProgram(['src/pages/CustomStorageCalculator.tsx'], {
    noEmit: true,
    jsx: ts.JsxEmit.ReactJSX
});

const diagnostics = ts.getPreEmitDiagnostics(program);
diagnostics.forEach(diagnostic => {
    if (diagnostic.file) {
        const { line, character } = diagnostic.file.getLineAndCharacterOfPosition(diagnostic.start);
        const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
        console.log(`${line + 1}:${character + 1} - ${message}`);
    } else {
        console.log(ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n'));
    }
});
