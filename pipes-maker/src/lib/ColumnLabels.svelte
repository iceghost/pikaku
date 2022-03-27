<script>
  export let width;
  export let row;

  $: numbers = [...Array(width).keys()];

  $: characters = numbers.map((x) =>
    String.fromCharCode('A'.charCodeAt(0) + x)
  );
</script>

<div
  class="grid place-items-center"
  style:grid-template-rows="subgrid"
  style:grid-template-columns="subgrid"
  style:grid-column="2 / span {width}"
  style:grid-row={row}
>
  {#each characters as character}
    <span class="text-2xl text-gray-400">{character}</span>
  {/each}
</div>
