<template>
  <div class="feed">
    <ServiceCard title="Boat Tour" description="Explore the coast!" price="150" />
    <ServiceCard title="Fishing Trip" description="Catch some fish!" price="200" />
  </div>
</template>

<script>
import ServiceCard from './ServiceCard.vue';

export default {
  components: {
    ServiceCard
  }
}
</script>

<style scoped>
.feed {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
