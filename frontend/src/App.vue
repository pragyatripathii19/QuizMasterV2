<template>
  <router-view :key="$route.fullPath"></router-view>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Optional simple styling */
.container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
}
input,
button {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
}
</style>
