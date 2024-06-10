<template>
    <div ref="el">
      <nodeHeader title="Switch Case"/>
      <p>Switch Case</p>
      <el-input v-model="switchCase" placeholder="SwitchCase" size="small"></el-input>
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
      const df = getCurrentInstance().appContext.config.globalProperties.$df;
      const switchCase = ref('');
  
      onMounted(async () => {
        await nextTick();
        nodeId.value = el.value.parentElement.parentElement.id.slice(5);
        const nodeData = df.value.getNodeFromId(nodeId.value);
        if (nodeData && nodeData.data) {
          switchCase.value = nodeData.data.switchCase || '';
        }
      });
  
      watch(switchCase, (newValue) => {
        const nodeData = df.value.getNodeFromId(nodeId.value);
        if (nodeData && nodeData.data) {
          nodeData.data.switchCase = newValue;
        }
      });
  
      return {
        el, switchCase
      }
    }    
  })
  </script>