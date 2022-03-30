<script>
  export let width;

  $: numbers = [...Array(width).keys()];

  $: characters = numbers.map((x) =>
    String.fromCharCode('A'.charCodeAt(0) + x)
  );
</script>

<tr>
  <td />
  {#each characters as character}
    <td class="text-center">
      <span class="text-2xl text-gray-400">{character}</span>
    </td>
  {/each}
  <td />
</tr>
