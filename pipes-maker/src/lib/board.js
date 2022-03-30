// @ts-check

/**
 * @param {string} str
 * @param {number} height
 * @param {number} width
 * @returns {import("$lib/types").Board}
 */
export function parse(str, height, width) {
  /** @type {import("$lib/types").Pipe[][]} */
  const pipes = [];
  for (let line of str.split('\n')) {
    /** @type {import("$lib/types").Pipe[]} */
    const row = [];
    line = line.trim();
    for (const code of line.split(' ')) {
      switch (code) {
        case '0':
          row.push({ joints: [false, false, false, false], colorIndex: 0});
          break;
        case '1':
          row.push({ joints: [true, false, false, false], colorIndex: 0});
          break;
        case '2a':
          row.push({ joints: [true, true, false, false], colorIndex: 0});
          break;
        case '2b':
          row.push({ joints: [true, false, true, false], colorIndex: 0});
          break;
        case '3':
          row.push({ joints: [true, true, true, false], colorIndex: 0});
          break;
        default:
          console.warn('unknown code');
      }
    }
    pipes.push(row);
  }
  return { pipes, height, width };
}
