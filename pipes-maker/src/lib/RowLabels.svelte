<script>
  export let height;
  export let column;

  $: numbers = [...Array(height).keys()];
</script>

<div
  class="grid place-items-center"
  style:grid-template-rows="subgrid"
  style:grid-template-columns="subgrid"
  style:grid-row="2 / span {height}"
  style:grid-column={column}
>
  {#each numbers as number}
    <span class="px-4 text-2xl text-gray-400">{number + 1}</span>
  {/each}
</div>
