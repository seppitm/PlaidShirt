/**
 * Verify actual SVG output and failure behavior of the DOT renderer.
 * @module renderer-tests
 */

import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile, readFile, rm } from "node:fs/promises";
import { resolve, join } from "node:path";
import test from "node:test";
import { renderDot } from "../skills/plaidshirt/scripts/render_dot.mjs";

/**
 * Create an isolated workspace removed after the test.
 *
 * @param {import("node:test").TestContext} context - Running test context.
 * @returns {Promise<string>} Absolute path within the project's test area.
 */
async function temporaryProject(context) {
    const base = resolve("tmp/node-tests");
    await mkdir(base, { recursive: true });
    const directory = await mkdtemp(join(base, "renderer-"));
    assert.equal(resolve(directory).startsWith(base + "/")
        || resolve(directory).startsWith(base + "\\"), true);

    context.after(async () => {
        await rm(directory, { recursive: true, force: true });
    });
    return directory;
}

test("DOT produces SVG geometry and the expected labels", async context => {
    const directory = await temporaryProject(context);
    const source = join(directory, "flow.dot");
    const output = join(directory, "flow.svg");
    await writeFile(source, 'digraph { start [shape=oval]; start -> finish; }');
    await renderDot(source, output);
    const svg = await readFile(output, "utf8");
    assert.match(svg, /<svg\b/);
    assert.match(svg, /<ellipse\b/);
    assert.match(svg, /<path\b/);
    assert.match(svg, /finish/);
});

test("Invalid source does not overwrite an existing output", async context => {
    const directory = await temporaryProject(context);
    const source = join(directory, "broken.dot");
    const output = join(directory, "previous.svg");
    await writeFile(source, 'digraph { broken [');
    await writeFile(output, "previous output");
    await assert.rejects(renderDot(source, output));
    assert.equal(await readFile(output, "utf8"), "previous output");
});
