// TypeScript/JavaScript
const jsClientProcess = Deno.run({
  cmd: [
    "deno",
    "bundle",
    "-c",
    "deno.json",
    "index.ts",
    "index.js",
    "--unstable",
    "--watch",
  ],
});

await jsClientProcess.status();
jsClientProcess.close();