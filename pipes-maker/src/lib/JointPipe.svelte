<script>
  import { getContext } from 'svelte';

  /** @type {import("$lib/types").Pipe}*/
  export let pipe;

  export let x;
  export let y;

  $: index = pipe.joints.reduce(
    (acc, x, i) => acc + 2 ** (3 - i) * (x ? 1 : 0),
    0
  );

  function clickHandler() {
    const [top, right, bottom, left] = pipe.joints;
    pipe = { ...pipe, joints: [left, top, right, bottom] };
  }

  const colors = [
    'bg-white border-gray-200',
    'bg-white border-gray-300',
    'bg-blue-50 border-blue-500',
    'bg-green-50 border-green-500',
    'bg-red-50 border-red-500',
  ];

  $: fixed = pipe.colorIndex != 0;

  function rightHandler(e) {
    e.preventDefault();
    pipe = { ...pipe, colorIndex: (pipe.colorIndex + 1) % colors.length };
  }

  /** @type {import("svelte/store").Writable<import("$lib/types").Board>} */
  let board = getContext('board');
</script>

<td
  class="h-11 w-11 p-1 border-2 border-gray-200 overflow-hidden"
  class:border-t-rose-500={y == 0 || (fixed && !pipe.joints[0])}
  class:border-t-green-200={fixed && pipe.joints[0]}
  class:border-r-rose-500={x == $board.width - 1 || (fixed && !pipe.joints[1])}
  class:border-r-green-200={fixed && pipe.joints[1]}
  class:border-b-rose-500={y == $board.height - 1 || (fixed && !pipe.joints[2])}
  class:border-b-green-200={fixed && pipe.joints[2]}
  class:border-l-rose-500={x == 0 || (fixed && !pipe.joints[3])}
  class:border-l-green-200={fixed && pipe.joints[3]}
  on:click={clickHandler}
  on:contextmenu={rightHandler}
>
  <img class="opacity-10" src="pipe-{index}.png" alt="pipe {index}" />
</td>
