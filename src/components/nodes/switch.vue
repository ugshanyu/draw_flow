<template>
    <div ref="el">
        <nodeHeader title="Switch"/>
    </div>
  </template>
  
  <script>
  import { defineComponent, onMounted, getCurrentInstance, ref, nextTick, watch } from 'vue'
  import nodeHeader from './nodeHeader.vue'
  
  export default defineComponent({
      components: {
          nodeHeader
      },
      setup() {
          const el = ref(null);
          const nodeId = ref(0);
          const df = getCurrentInstance().appContext.config.globalProperties.$df.value;
  
          onMounted(async () => {
              await nextTick();
              nodeId.value = el.value.parentElement.parentElement.id.slice(5);
              const nodeData = df.getNodeFromId(nodeId.value);
          });
          
          return {
              el
          }
      }    
  })
  </script>
  