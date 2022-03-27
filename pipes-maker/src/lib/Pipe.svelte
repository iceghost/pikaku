<script>
  /** @type {import("$lib/types").Pipe}*/
  export let pipe;

  export let index = 0;
  $: {
    const [top, right, bottom, left] = pipe.joints;
    index = (top ? 8 : 0) + (right ? 4 : 0) + (bottom ? 2 : 0) + (left ? 1 : 0);
  }

  function clickHandler() {
    const [top, right, bottom, left] = pipe.joints;
    pipe.joints = [left, top, right, bottom];
    pipe = pipe;
  }

  const colors = [
    'bg-white border-gray-200',
    'bg-gray-300 border-gray-300',
    'bg-blue-50 border-blue-500',
    'bg-green-50 border-green-500',
    'bg-red-50 border-red-500',
  ];
  let colorIndex = 0;

  function rightHandler(e) {
    e.preventDefault();
    colorIndex = (colorIndex + 1) % colors.length;
  }
</script>

<div
  class="{colors[
    colorIndex
  ]} h-10 border-[1.5px] border-gray-200 rounded-md bg-contain aspect-square"
  style:background-image="url('pipe-{index}.png')"
  on:click={clickHandler}
  on:contextmenu={rightHandler}
/>
