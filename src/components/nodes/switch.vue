<template>
    <div ref="el">
        <nodeHeader title="Switch"/>
        <p>Input</p>
        <el-input v-model="input" placeholder="Input" size="small"></el-input>
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
        const input = ref('');
  
        // Function to handle data updates
        const updateNodeData = () => {
            const nodeData = df.getNodeFromId(nodeId.value);
            nodeData.data = { input: input.value };
            df.updateNodeDataFromId(nodeId.value, nodeData);
        };
  
        // Watch for changes in the input field and update node data accordingly
        watch(input, updateNodeData);
  
        onMounted(async () => {
            await nextTick();
            nodeId.value = el.value.parentElement.parentElement.id.slice(5);
            const nodeData = df.getNodeFromId(nodeId.value);
            let data = findDeepestData(nodeData);
            console.log("datadatadata", data)
            if (data) {
                input.value = data.input || '';
            }
        });
        
        return {
            el, input
        }
    }    
  })
  </script>