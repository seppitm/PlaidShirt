/**
 * Render DOT models locally using Graphviz as a WebAssembly library.
 * This optional renderer requires Node.js and the package `@viz-js/viz`.
 *
 * @module plaidshirt-dot
 */

import { readFile, mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { instance } from "@viz-js/viz";

/**
 * Generate an SVG file from an editable DOT model.
 *
 * Output is written only after rendering succeeds. A
 * source syntax error leaves an existing output file unchanged.
 *
 * @param {string} sourcePath - Path to the UTF-8 DOT source file.
 * @param {string} outputPath - Path of the SVG output file.
 * @returns {Promise<void>} Resolves after the output has been written.
 * @throws {Error} For invalid source or a file-access failure.
 */
export async function renderDot(sourcePath, outputPath) {
    const source = await readFile(sourcePath, "utf8");
    const renderer = await instance();
    const renderedDiagram = renderer.renderString(source, { format: "svg" });

    await mkdir(dirname(outputPath), { recursive: true });
    await writeFile(outputPath, renderedDiagram, "utf8");
}

if (process.argv[1] && fileURLToPath(import.meta.url) === resolve(process.argv[1])) {
    if (process.argv.length !== 4) {
        console.error("Usage: node render_dot.mjs SOURCE.dot OUTPUT.svg");
        process.exitCode = 2;
    } else {
        try {
            await renderDot(process.argv[2], process.argv[3]);
        } catch (error) {
            console.error(error.message);
            process.exitCode = 1;
        }
    }
}
