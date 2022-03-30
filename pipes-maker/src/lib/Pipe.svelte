<script>
  /** @type {import("$lib/types").Pipe}*/
  export let pipe;

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
    'bg-gray-300 border-gray-300',
    'bg-blue-50 border-blue-500',
    'bg-green-50 border-green-500',
    'bg-red-50 border-red-500',
  ];

  function rightHandler(e) {
    e.preventDefault();
    pipe = { ...pipe, colorIndex: (pipe.colorIndex + 1) % colors.length };
  }
</script>

<div
  class="{colors[
    pipe.colorIndex
  ]} h-10 border-[1.5px] border-gray-200 rounded-md bg-contain aspect-square"
  style:background-image="url('pipe-{index}.png')"
  on:click={clickHandler}
  on:contextmenu={rightHandler}
/>
