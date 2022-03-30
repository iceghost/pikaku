<script context="module">
  export const prerender = false;
</script>

<script>
  import SmallCaps from '../lib/SmallCaps.svelte';

  import ColumnLabels from '$lib/ColumnLabels.svelte';

  import { parse } from '$lib/board';
  import Pipe from '$lib/Pipe.svelte';
  import RowLabels from '$lib/RowLabels.svelte';
  import JointColumnLabels from '$lib/JointColumnLabels.svelte';
  import JointPipe from '$lib/JointPipe.svelte';
  import { writable } from 'svelte/store';
  import { setContext } from 'svelte';

  let raw = `1 1 1 2a 1
2b 2a 3 3 3
3 2b 3 1 2b
2b 2a 3 3 1
1 2a 1 2a 1`;
  let height = 5;
  let width = 5;

  const board = writable(undefined);
  setContext('board', board);

  $: $board = parse(raw, height, width);
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

<div>
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
      {#each $board.pipes as row, y}
        {#each row as pipe, x}
          <Pipe bind:pipe />
        {/each}
      {/each}
    </div>
  </div>
  <table class="border-collapse rounded-md mb-5">
    <JointColumnLabels {width} />
    {#each $board.pipes as row, y}
      <tr>
        <td>
          <span class="px-4 text-2xl text-gray-400">{y + 1}</span>
        </td>
        {#each row as pipe, x}
          <JointPipe bind:pipe {x} {y} />
        {/each}
        <td>
          <span class="px-4 text-2xl text-gray-400">{y + 1}</span>
        </td>
      </tr>
    {/each}
    <JointColumnLabels {width} />
  </table>
</div>
