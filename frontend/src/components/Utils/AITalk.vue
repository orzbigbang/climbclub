<script setup>
import { ref } from "vue";
import { postMessage } from "@/api/AIService";

const prompt = ref("")
const response = ref("")
const showDialog = ref(false)

const controlDialog = () => {
  showDialog.value = !showDialog.value
}

const callAI = () => {
  postMessage(prompt.value).then(res => {
    response.value = res
  }).catch(err => {
    response.value = "出错了^^; -> " + err.message
  })
  prompt.value = ""
}
</script>

<template>
<div class="ai-wrapper pos-fix z-100">
  <div class="coversation-wrapper flex-col-between pos-abs z-1000" v-show="showDialog">
    <div class="resposne">{{ response }}</div>
    <input type="text" v-model="prompt" @keydown.enter="callAI">
  </div>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <!-- Warning Triangle - now just a shape without fill or stroke -->
    <path d="M50 10 L90 80 L10 80 Z" 
          fill="none"/>
    
    <!-- Question Mark - rotated 30 degrees -->
    <text @click="controlDialog" class="ai-bear" x="60" y="45" 
          font-size="22" 
          font-weight="900" 
          fill="#2F4F4F"
          style="font-family: Arial Black, Arial, sans-serif"
          transform="rotate(30, 60, 45)">?</text>
    
    <!-- Bear Face -->
    <g @click="controlDialog" class="ai-bear" transform="translate(50,65) scale(0.8)">
      <!-- Bear Head -->
      <circle cx="0" cy="0" r="16" fill="#A0522D"/>
      
      <!-- Inner face patch -->
      <circle cx="0" cy="2" r="12" fill="#DEB887"/>
      
      <!-- Ears -->
      <circle cx="-12" cy="-12" r="6" fill="#A0522D"/>
      <circle cx="12" cy="-12" r="6" fill="#A0522D"/>
      <circle cx="-12" cy="-12" r="3" fill="#DEB887"/>
      <circle cx="12" cy="-12" r="3" fill="#DEB887"/>
      
      <!-- Eyes -->
      <circle cx="-6" cy="-2" r="2.5" fill="#2F4F4F"/>
      <circle cx="6" cy="-2" r="2.5" fill="#2F4F4F"/>
      <circle cx="-6.5" cy="-3" r="1" fill="white"/>
      <circle cx="5.5" cy="-3" r="1" fill="white"/>
      
      <!-- Nose -->
      <circle cx="0" cy="3" r="2.5" fill="#2F4F4F"/>
      
      <!-- Mouth -->
      <path d="M-4 7 Q0 9 4 7" 
            fill="none" 
            stroke="#2F4F4F" 
            stroke-width="1.5"
            stroke-linecap="round"/>
    </g>
  </svg>
</div>
</template>

<style lang='less' scoped>
.ai-wrapper {
  width: 12rem;
  height: 12rem;
  right: 3%;
  bottom: 3%;

  .coversation-wrapper {
    width: 240px;
    height: 300px;
    background-color: pink;
    left: -100%;
    top: -65%;
  }

  .ai-bear {
    
    &:hover {
      cursor: pointer;
    }
  }
}
</style>