<script setup>
import { defineProps, ref, watch,  } from 'vue';

const props = defineProps({
  schema: Object,
  show_grid: Boolean,
  show_anchor: Boolean,
});

let prevWaitingSchema = [];
const prevSchema = ref([]);
const currentSchema = ref([]);
const display_mimic = ref(false);

const animation_type = ref('');
const transformation_type = ref('');

const anchorIn = ref([1, 1]);
const anchorOut = ref([1, 5]);

const scale_factor = ref(1);

const delta_translate_x = ref(0);
const delta_translate_y = ref(0);

let timeOut1 = null;
let timeOut2 = null;

watch(() => props.schema, (value) => {
  scale_factor.value = 1 / (value.iteration * value.iteration / 8 + 1);

  if (value.iteration === 0) {
    prevWaitingSchema = value.schema;
    currentSchema.value = value.schema;
    prevSchema.value = value.schema;
    return;
  }

  if (value.iteration % 2 === 1) {
    transformation_type.value = 'rotate';

    delta_translate_x.value = (anchorOut.value[0] - anchorIn.value[0] - 3) * 100 * 0.9 / 4;
    delta_translate_y.value = (anchorOut.value[1] - anchorIn.value[1] - 1) * 100 * 0.9 / 6;
  } else if (value.iteration % 4 === 0) {
    transformation_type.value = 'flip-vertical';

    delta_translate_x.value = 0;
    delta_translate_y.value = (value.anchorOut[1] - value.anchorIn[1] - (6 / 2 - value.anchorIn[1]) * 2) * 100 * 0.9 / 6;
  } else {
    transformation_type.value = 'flip-horizontal';

    delta_translate_x.value = (value.anchorOut[0] - value.anchorIn[0] - (4 / 2 - value.anchorIn[0]) * 2) * 100 * 0.9 / 4;
    delta_translate_y.value = 0;
  }

  anchorIn.value = value.anchorIn || [1, 1];
  anchorOut.value = value.anchorOut || [1, 5];

  if (timeOut1) {
    clearTimeout(timeOut1);
  }
  if (timeOut2) {
    clearTimeout(timeOut2);
    currentSchema.value = prevWaitingSchema;
    prevSchema.value = prevWaitingSchema;
  }
  prevWaitingSchema = value.schema;

  display_mimic.value = false;
  animation_type.value = 'fade-in';
  display_mimic.value = true;

  timeOut2 = setTimeout(() => {
    display_mimic.value = false;
    prevSchema.value = currentSchema.value;
  }, 3000);

  timeOut1 = setTimeout(() => {
    animation_type.value = 'fade-away';
    currentSchema.value = value.schema;
  }, 2000);
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
      <circle
          v-if="!show_anchor"
          :cx="fromGridToCanvas(anchorIn[0], 4)"
          :cy="fromGridToCanvas(anchorIn[1], 6)"
          r="5"
          fill="red"
      />
      <circle
          v-if="!show_anchor"
          :cx="fromGridToCanvas(anchorOut[0], 4)"
          :cy="fromGridToCanvas(anchorOut[1], 6)"
          r="5"
          fill="green"
      />
    </svg>
    <svg
        class="letter mimic"
        v-if="display_mimic"
        ref="mimic"
        :style="{translate:`${delta_translate_x}% ${delta_translate_y}%`}"

        :animation-type="animation_type"
        :transformation-type="transformation_type"
    >
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
  height: 300px;

  transition: transform 1s ease-out;
}

.letter svg {
  width: 100%;
  height: 100%;
  overflow: visible;
}

.mimic {
  position: absolute;
  left: 0;
  top: 0;
  aspect-ratio: 4/6;
  width: 100%;

  animation: transform-unflip 2s ease-in-out infinite;
  animation-iteration-count: 1;
  opacity: 1;
  scale: 1;
}

.mimic[transformation-type="rotate"] {
  rotate: 90deg;
}
.mimic[transformation-type="flip-vertical"] {
  rotate: 180deg x;
}
.mimic[transformation-type="flip-horizontal"] {
  rotate: 180deg y;
}
.mimic[animation-type="fade-away"] {
  animation: fade-away 1s linear;
}

@keyframes fade-away {
  0% {
  }
  100% {
    opacity: 0;
    scale: 1.2;
  }
}

@keyframes transform-unflip {
  0% {
    rotate: 0deg;
    translate: 0 0;
  }
  100% {
  }
}
</style>