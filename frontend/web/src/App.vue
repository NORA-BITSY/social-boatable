<template>
  <div>
    <h1>Boatable</h1>
    <Navbar />
    <Feed />
    <router-view /> <!-- Add routing for profiles, groups, etc. -->
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';
import Feed from './components/Feed.vue';

export default {
  components: {
    Navbar,
    Feed
  }
}
</script>

<style scoped>
/* Add some styling */
</style>
