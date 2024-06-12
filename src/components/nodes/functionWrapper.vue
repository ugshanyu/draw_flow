<template>
    <div ref="el">
      <nodeHeader title="Function Wrapper" />
      <p>Input Value</p>
      <el-input v-model="inputValue" placeholder="Enter input value" size="small"></el-input>
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
      const inputValue = ref('');
  
      // Function to handle data updates
      const updateNodeData = () => {
        const nodeData = df.getNodeFromId(nodeId.value);
        nodeData.data = { inputValue: inputValue.value };
        df.updateNodeDataFromId(nodeId.value, nodeData);
      };
  
      // Watch for changes in the input field and update node data accordingly
      watch(inputValue, updateNodeData);
  
      onMounted(async () => {
        await nextTick();
        nodeId.value = el.value.parentElement.parentElement.id.slice(5);
        const nodeData = df.getNodeFromId(nodeId.value);
        if (nodeData && nodeData.data) {
          inputValue.value = nodeData.data.inputValue || '';
        }
      });
  
      return {
        el, inputValue
      }
    }
  })
  </script>