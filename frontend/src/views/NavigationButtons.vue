<template>
  <div class="d-flex justify-content-between mt-4">
    <button class="btn btn-outline-secondary" @click="goBack">⬅ Back</button>
    <button class="btn btn-outline-primary" @click="goNext">Next ➡</button>
  </div>
</template>

<script>
export default {
  name: "NavigationButtons",
  props: {
    nextRoute: {
      type: Object,
      required: false,
    },
  },
  methods: {
    goBack() {
      this.$router.go(-1); // Go one step back in browser history
    },
    goNext() {
      if (this.nextRoute) {
        this.$router.push(this.nextRoute); // Navigate to next page
      } else {
        alert("No next page configured yet!");
      }
    },
  },
};
</script>
