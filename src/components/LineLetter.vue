<script setup>
import { defineProps, ref, watch,  } from 'vue';

const props = defineProps({
  schema: Object,
  show_grid: Boolean,
  show_anchor: Boolean,
});

const prevSchema = ref([]);
const currentSchema = ref([]);
const display_mimic_1 = ref(false);
const display_mimic_2 = ref(false);
const display_mimic_3 = ref(false);

const anchorIn = ref([1, 1]);
const anchorOut = ref([1, 5]);

const scale_factor = ref(1);

const delta_translate_x = ref(0);
const delta_translate_y = ref(0);

watch(() => props.schema, (value) => {
  scale_factor.value = 1 / (value.iteration * value.iteration / 8 + 1);

  // anchorIn.value = value.anchorIn || [1, 1];
  // anchorOut.value = value.anchorOut || [1, 5];

  if (true || value.iteration === 0) {
    currentSchema.value = value.schema;
    prevSchema.value = value.schema;
    return;
  }

  let display_mimic = value.iteration % 2 === 1 ? display_mimic_1 :
      (value.iteration % 4 === 0 ? display_mimic_2 : display_mimic_3);

  delta_translate_x.value = (value.anchorOut[0] - value.anchorIn[0]) * 100 / 6;
  delta_translate_y.value = (value.anchorOut[1] - value.anchorIn[1]) * 60 / 6;

  display_mimic.value = true;

  setTimeout(() => {
    display_mimic.value = false;
    prevSchema.value = currentSchema.value;
  }, 3000);

  setTimeout(() => {
    currentSchema.value = value.schema;
  }, 2250);
});

function fromGridToCanvas(pos, direction_cells = 0) {
  return pos * 90 / direction_cells + 5 + '%';
}
</script>

<template>
  <div class="letter" :style="{ transform: `scale(${scale_factor})` }" ref="letter_box">
    <svg>
      <line
          v-if="show_grid"
          v-for="y in 7"
          :x1="fromGridToCanvas(0, 4)"
          :y1="fromGridToCanvas(y-1, 6)"
          :x2="fromGridToCanvas(4, 4)"
          :y2="fromGridToCanvas(y-1, 6)"
          stroke="#313131"
          stroke-width="2"
      />
      <line
          v-if="show_grid"
          v-for="x in 5"
          :x1="fromGridToCanvas(x-1, 4)"
          :y1="fromGridToCanvas(0, 6)"
          :x2="fromGridToCanvas(x-1, 4)"
          :y2="fromGridToCanvas(6, 6)"
          stroke="#313131"
          stroke-width="2"
      />
      <line
          v-for="line in currentSchema"
          :x1="fromGridToCanvas(line[0], 4)"
          :y1="fromGridToCanvas(line[1], 6)"
          :x2="fromGridToCanvas(line[2], 4)"
          :y2="fromGridToCanvas(line[3], 6)"
          stroke="white"
          stroke-width="4"
          stroke-linecap="round"
      />
<!--      <circle-->
<!--          v-if="!show_anchor"-->
<!--          :cx="fromGridToCanvas(anchorIn[0], 4)"-->
<!--          :cy="fromGridToCanvas(anchorIn[1], 6)"-->
<!--          r="5"-->
<!--          fill="red"-->
<!--      />-->
<!--      <circle-->
<!--          v-if="!show_anchor"-->
<!--          :cx="fromGridToCanvas(anchorOut[0], 4)"-->
<!--          :cy="fromGridToCanvas(anchorOut[1], 6)"-->
<!--          r="5"-->
<!--          fill="green"-->
<!--      />-->
    </svg>
    <svg class="letter mimic-1" v-if="display_mimic_1" ref="mimic_1" :style="{translate:`${delta_translate_x}% ${delta_translate_y}%`}">
      <line
          v-for="line in prevSchema"
          :x1="fromGridToCanvas(line[0], 4)"
          :y1="fromGridToCanvas(line[1], 6)"
          :x2="fromGridToCanvas(line[2], 4)"
          :y2="fromGridToCanvas(line[3], 6)"
          stroke="white"
          stroke-width="4"
          stroke-linecap="round"
      />
    </svg>
    <svg class="letter mimic-2" v-if="display_mimic_2" ref="mimic_2" :style="{translate:`${delta_translate_x}% ${delta_translate_y}%`}">
      <line
          v-for="line in prevSchema"
          :x1="fromGridToCanvas(line[0], 4)"
          :y1="fromGridToCanvas(line[1], 6)"
          :x2="fromGridToCanvas(line[2], 4)"
          :y2="fromGridToCanvas(line[3], 6)"
          stroke="white"
          stroke-width="4"
          stroke-linecap="round"
      />
    </svg>
    <svg class="letter mimic-3" v-if="display_mimic_3" ref="mimic_3" :style="{translate:`${delta_translate_x}% ${delta_translate_y}%`}">
      <line
          v-for="line in prevSchema"
          :x1="fromGridToCanvas(line[0], 4)"
          :y1="fromGridToCanvas(line[1], 6)"
          :x2="fromGridToCanvas(line[2], 4)"
          :y2="fromGridToCanvas(line[3], 6)"
          stroke="white"
          stroke-width="4"
          stroke-linecap="round"
      />
    </svg>
  </div>
</template>

<style scoped>
.letter {
  aspect-ratio: 4/6;
  width: 200px;

  transition: transform 1s ease-out;
}

.letter svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.mimic-1 {
  position: absolute;
  left: 0;
  top: 0;
  animation: transform-rotate 3s linear alternate;
}

.mimic-2 {
  position: absolute;
  left: 0;
  top: 0;
  animation: transform-flip-vertical 3s linear alternate;
}

.mimic-3 {
  position: absolute;
  left: 0;
  top: 0;
  animation: transform-flip-horisontaly 3s linear alternate;
}

@keyframes transform-rotate {
  0% {
    opacity: 1;
    rotate: 0deg;
    scale: 1;
    //translate: 0 0;
  }
  75% {
    opacity: 1;
    rotate: 90deg;
    scale: 1;
  }
  100% {
    opacity: 0;
    rotate: 90deg;
    //scale: 1.2;
  }
}

@keyframes transform-flip-vertical {
  0% {
    opacity: 1;
    rotate: 0deg x;
    scale: 1;
    //translate: 0 0;
  }
  75% {
    opacity: 1;
    rotate: 180deg x;
    scale: 1;
  }
  80% {
    opacity: 1;
    rotate: 180deg x;
    scale: 1;
  }
  100% {
    opacity: 0;
    rotate: 180deg x;
    scale: 1.2;
  }
}

@keyframes transform-flip-horisontaly {
  0% {
    opacity: 1;
    rotate: 0deg y;
    scale: 1;
    //translate: 0 0;
  }
  75% {
    opacity: 1;
    rotate: 180deg y;
    scale: 1;
  }
  80% {
    opacity: 1;
    rotate: 180deg y;
    scale: 1;
  }
  100% {
    opacity: 0;
    rotate: 180deg y;
    scale: 1.2;
  }
}
</style>