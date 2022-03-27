<script>
  import '../app.css';
</script>

<div class="w-full mx-auto flex items-center justify-center space-x-10">
  <slot />
</div>

<style global lang="postcss">
  :root {
    @apply font-mono;
  }
</style>
