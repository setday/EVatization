<script setup>
import {defineModel, ref, watch} from 'vue'

import LetterSchemes from '../data/letter-schemes.json'
import LineLetter from "./LineLetter.vue";

import { changeShape } from '../utils/transformation.js'
import { generateSVG } from '../utils/svg_generator.js'

const currentSchema = defineModel();

const letter = ref('');
const svgs = ref([]);

function getProps(letter) {
  if (!(letter in LetterSchemes))
    return { perimeter: 0, elements: 0, complexity: 0, symmetry: '' };

  const scheme = LetterSchemes[letter] || [];
  let perimeter = 0;
  let elements = 0;
  let complexity = 0;
  let symmetry = '';

  for (const line of scheme) {
    const x1 = line[0];
    const y1 = line[1];
    const x2 = line[2];
    const y2 = line[3];

    perimeter += x2 - x1 + y2 - y1;
    elements += 1;
  }

  complexity = Math.round(perimeter / elements);

  return { perimeter, elements, complexity, symmetry };
}

function factorizeSchema() {
  const res = changeShape(
      currentSchema.value.schema,
      currentSchema.value.iteration,
      currentSchema.value.anchorIn,
      currentSchema.value.anchorOut
  );
  const new_schema = res.new_shape;

  currentSchema.value = {
    schema: new_schema,
    iteration: currentSchema.value.iteration + 1,
    anchorIn: currentSchema.value.anchorIn,
    anchorOut: res.new_anchor_out,
  };

  svgs.value.push(generateSVG(new_schema));
}

const perimeter = ref(0);
const elements = ref(0);
const complexity = ref(0);
const symmetry = ref('');

watch(letter, (value) => {
  const new_vals = getProps(value);
  perimeter.value = new_vals.perimeter
  elements.value = new_vals.elements
  complexity.value = new_vals.complexity
  symmetry.value = new_vals.symmetry

  currentSchema.value = {
    schema: LetterSchemes[value] || [],
    iteration: 0,
    anchorIn: currentSchema.value.anchorIn,
    anchorOut: [1, 5],
  };

  svgs.value = [generateSVG(LetterSchemes[value] || [])];
});
</script>

<template>
  <div class="sidebar">
    <div class="section">
      <span>[0]</span>
      <h1>Генерация фрактального начертания</h1>
    </div>
    <div class="section">
      <span>[1]</span>
      <div class="section-list">
        <h2>Поле ввода:</h2>
        <input type="text" placeholder="Введите букву..." maxlength="1" v-model="letter" />
      </div>
    </div>
    <div class="section">
      <span>[2]</span>
      <div class="section-list">
        <h2>Схема буквы:</h2>
        <div class="scheme-section">
          <LineLetter :schema="{
            schema: LetterSchemes[letter],
            iteration: 0,
          }" show_grid />
          <div class="scheme-list">
            <span>Значение: {{ letter }}</span>
            <span>Периметр: {{ perimeter }}</span>
            <span>Кол-во элементов: {{ elements }}</span>
            <span>Сложность: {{ complexity }}</span>
<!--            <span>Симметрия: {{ symmetry }}</span>-->
          </div>
        </div>
      </div>
    </div>
    <div class="section">
      <span>[3]</span>
      <button @click="factorizeSchema" :disabled="!(letter in LetterSchemes)">
        Фрактализовать
      </button>
    </div>
    <div class="section last-section">
      <span>[4]</span>
      <div class="section-list">
        <h2>Экспорт итераций:</h2>
        <div class="scheme-list">
          <a v-for="(svg, index) in svgs" :key="index" :href="'data:attachment/text,' + encodeURI(svg)" :download="letter + '_fractal_' + index + '.svg'">
            {{ letter + '_fractal_' + index + '.svg' }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.sidebar {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  height: 100%;
  width: 400px;
  z-index: 1;
  background-color: #161616;
  overflow-x: hidden;
}

.section {
  display: flex;
  align-items: start;
  padding: 26px 16px;
  gap: 25px;
  color: white;
  border-top: 1px solid #343434;
  border-bottom: 1px solid #343434;
  font-family: 'Inter', sans-serif;
}

.section-list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.section span {
  font-size: 16px;
  font-weight: 600;
}

.sidebar h1, h2 {
  margin: 0;
  padding: 0;
  text-align: start;
}

.sidebar input[type="text"] {
  width: 100%;
}

.scheme-section {
  display: flex;
  gap: 25px;
  margin-top: 12px;
}

.scheme-section .letter {
  width: 160px;
  height: auto;
  overflow: clip;
}

.scheme-list {
  margin-top: 12px;
  gap: 6px;
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: end;
  width: 100%;
}

.scheme-list span {
  font-size: 12px;
  font-weight: 400;
}

.sidebar button {
  width: 100%;
  padding: 12px 20px;
  box-sizing: border-box;
  cursor: pointer;
}

.scheme-list a {
  font-size: 12px;
}

.last-section {
  flex-grow: 1;
}
</style>