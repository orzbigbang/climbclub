<script setup>
import { useShowStore } from '@/stores/show'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const { notification } = storeToRefs(useShowStore())
const progressDuration = computed(() => notification.value.duration)
</script>

<template>
  <Transition name="notification-fade">
    <div v-if="notification.show" 
         class="notification-container"
         :class="notification.type">
      <div class="notification-content pos-rel z-1">{{ notification.message }}</div>
      <div class="notification-progress"></div>
    </div>
  </Transition>
</template>

<style lang="less" scoped>
.notification-container {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 10px;
  z-index: 9999;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;

  .notification-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: v-bind('notification.type === "success" ? "#67c23a" : "#f56c6c"');
    border-radius: inherit;
    animation: progress linear forwards;
    animation-duration: v-bind('progressDuration + "ms"');
    transform-origin: left;
  }

  .success {
    background-color: #fef0f0;
    color: #67c23a;
  }

  .error {
    background-color: #fef0f0;
    color: #f56c6c;
  }
}

@keyframes progress {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

.notification-fade-enter-active,
.notification-fade-leave-active {
  transition: all 0.3s ease;
}

.notification-fade-enter-from,
.notification-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-20px);
}
</style> 