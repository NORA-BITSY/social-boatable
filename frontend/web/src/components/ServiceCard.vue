<template>
  <div class="service-card">
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
    <p>Price: ${{ price }}</p>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    description: String,
    price: String
  }
}
</script>

<style scoped>
.service-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px;
  width: 300px;
  text-align: center;
}
</style>
