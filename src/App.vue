<script setup>
import { ref } from "vue";

import SideBar from "./components/SideBar.vue";
import LineLetter from "./components/LineLetter.vue";

const schemeModel = ref({ schema: [], iteration: 0, anchorIn: [1, 1], anchorOut: [1, 5] });
</script>

<template>
  <div class="horizontal-container">
    <div  class="canvas-container">
      <LineLetter :schema="schemeModel" />
    </div>
    <SideBar v-model="schemeModel" />
  </div>
</template>

<style scoped>
.horizontal-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
}

.canvas-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
