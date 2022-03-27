<script>
  import SmallCaps from '../lib/SmallCaps.svelte';

  import ColumnLabels from '$lib/ColumnLabels.svelte';

  import { parse } from '$lib/board';
  import Pipe from '$lib/Pipe.svelte';
  import RowLabels from '$lib/RowLabels.svelte';

  let raw = `1 2a 2a 1
2a 3 3 2a
2a 3 3 2a
0 0 1 1`;
  let height = 4;
  let width = 4;

  $: indices = new Array(height * width);

  $: numbers = [...Array(width).keys()];

  $: characters = numbers.map((x) =>
    String.fromCharCode('A'.charCodeAt(0) + x)
  );

  $: board = parse(raw, height, width);
</script>

<div>
  <h1 class="mt-2 font-bold text-xl">
    <SmallCaps text="PIPES" />
    <SmallCaps text="MAKER" />
  </h1>

  <p class="text-sm">it doesn't have to be this styled, honestly</p>

  <form class="mt-5 flex flex-col gap-2">
    <label for="height-input">
      Height:
      <input
        class="w-16 px-2 py-1 border rounded-md"
        id="height-input"
        type="number"
        bind:value={height}
      />
    </label>
    <label for="width-input">
      Width :
      <input
        class="w-16 px-2 py-1 border rounded-md"
        id="width-input"
        type="number"
        bind:value={width}
      />
    </label>
    <label for="raw-input"> Board : </label>
    <textarea
      id="raw-input"
      class="border rounded-md p-2 h-56"
      bind:value={raw}
    />
  </form>
</div>

<div
  class="mt-5 grid justify-center auto-rows-fr auto-cols-fr gap-1"
  style:grid-template-columns="repeat({width + 2}, min-content)"
>
  <div
    style:grid-column="1"
    style:grid-row="1"
    class="border-l-2 border-t-2 rounded-md border-gray-100"
  />
  <div
    style:grid-column={width + 2}
    style:grid-row={height + 2}
    class="border-r-2 border-b-2 rounded-md border-gray-100"
  />
  <ColumnLabels {width} row="1" />
  <ColumnLabels {width} row={height + 2} />
  <RowLabels {height} column="1" />
  <RowLabels {height} column={width + 2} />
  <div
    style:grid-template-rows="subgrid"
    style:grid-template-columns="subgrid"
    style:grid-column="2 / span {width}"
    style:grid-row="2 / span {height}"
    class="grid"
  >
    {#each board.pipes as pipe, i}
      <Pipe {pipe} index={indices[i]} />
    {/each}
  </div>
</div>
