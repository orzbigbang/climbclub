<script setup>
import {getRandomSentences, getRandomColors} from '@/compositions/randomThing.js'
const randomSentences = getRandomSentences()
const randomColors = getRandomColors()

const scene1Gsap = () => {
  const splitTypes = document.querySelectorAll(".reveal-type")
  splitTypes.forEach((sentenceDOM, i) => {
  const text = new SplitType(sentenceDOM, {types: 'words,chars', whitespace: 'preserve'})
  
  gsap.from(text.chars, {
      scrollTrigger: {
        trigger: sentenceDOM,
        start: 'top 80%',
        end: 'top 30%',
        scrub: true,
      },
      opacity: 0.2,
      stagger: 0.2
    })
  })
}

defineExpose({
  scene1Gsap
})
</script>

<template>
  <section class="section-wrapper scene-1">
    <div class="type-wrapper flex-center pos-rel" v-for="sentence, index in randomSentences" :style="{ backgroundImage: randomColors[index] }">
      <div class="reveal-type">{{ sentence }}</div>
    </div>
  </section>
</template>

<style scoped  lang='less'>
@text-size: 32px;

.scene-1 {
  .type-wrapper {
    height: 70vh;
    width: 100vw;
    padding: 0 15%;
    margin: 0 auto;

    &::after {
      display: block;
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      background-image: url("noise-bg.png");
    }

    .reveal-type {
      width: 100%;
      font-size: @text-size;
      font-weight: bold;
      text-align: center;
    }
  }
}
</style>