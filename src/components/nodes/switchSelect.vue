<template>
    <div ref="el">
      <nodeHeader title="Switch"/>
      <p>Select Option</p>
      <el-select v-model="selectedOption" placeholder="Select option" size="small">
        <el-option label="Function" value="function"></el-option>
        <el-option label="Scenario" value="scenario"></el-option>
      </el-select>
    </div>
  </template>
  
  <script>
  import { defineComponent, onMounted, getCurrentInstance, ref, nextTick, watch } from 'vue'
  import nodeHeader from './nodeHeader.vue'
  import { findDeepestData } from '../../utils'
  
  export default defineComponent({
    components: {
      nodeHeader
    },
    setup() {
      const el = ref(null);
      const nodeId = ref(0);
      const df = getCurrentInstance().appContext.config.globalProperties.$df.value;
      const selectedOption = ref('');
  
      // Function to handle data updates
      const updateNodeData = () => {
        const nodeData = df.getNodeFromId(nodeId.value);
        nodeData.data = { selectedOption: selectedOption.value };
        df.updateNodeDataFromId(nodeId.value, { selectedOption: selectedOption.value });
      };
  
      // Watch for changes in the selected option and update node data accordingly
      watch(selectedOption, updateNodeData);
  
      onMounted(async () => {
        await nextTick();
        nodeId.value = el.value.parentElement.parentElement.id.slice(5);
        const nodeData = df.getNodeFromId(nodeId.value);
        let data = findDeepestData(nodeData);
        if (data) {
          selectedOption.value = data.selectedOption || '';
        }
      });
      
      return {
        el, selectedOption
      }
    }    
  })
  </script>