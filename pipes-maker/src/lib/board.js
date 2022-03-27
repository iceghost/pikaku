// @ts-check

/**
 * @param {string} str
 * @param {number} height
 * @param {number} width
 * @returns {import("$lib/types").Board}
 */
export function parse(str, height, width) {
  /** @type {import("$lib/types").Pipe[]} */
  const pipes = [];
  for (let line of str.split('\n')) {
    line = line.trim();
    for (const code of line.split(' ')) {
      switch (code) {
        case '0':
          pipes.push({ joints: [false, false, false, false] });
          break;
        case '1':
          pipes.push({ joints: [true, false, false, false] });
          break;
        case '2a':
          pipes.push({ joints: [true, true, false, false] });
          break;
        case '2b':
          pipes.push({ joints: [true, false, true, false] });
          break;
        case '3':
          pipes.push({ joints: [true, true, true, false] });
          break;
        default:
          console.warn('unknown code');
      }
    }
  }
  return { pipes, height, width };
}
