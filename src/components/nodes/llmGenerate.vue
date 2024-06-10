<template>
    <div ref="el">
        <nodeHeader title="LLM Generate"/>
        <p>System Prompt</p>
        <el-input v-model="systemPrompt" placeholder="System Prompt" size="small"></el-input>
        <p>User Prompt</p>
        <el-input v-model="userPrompt" placeholder="User Prompt" size="small"></el-input>
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
          const systemPrompt = ref('');
          const userPrompt = ref('');
  
          // Function to handle data updates
          const updateNodeData = () => {
              const nodeData = df.getNodeFromId(nodeId.value);
              nodeData.data = { systemPrompt: systemPrompt.value, userPrompt: userPrompt.value };
              df.updateNodeDataFromId(nodeId.value, nodeData);
          };
  
          // Watch for changes in the input fields and update node data accordingly
          watch(systemPrompt, updateNodeData);
          watch(userPrompt, updateNodeData);
  
          onMounted(async () => {
              await nextTick();
              nodeId.value = el.value.parentElement.parentElement.id.slice(5);
              const nodeData = df.getNodeFromId(nodeId.value);
              if (nodeData && nodeData.data) {
                  systemPrompt.value = nodeData.data.systemPrompt || '';
                  userPrompt.value = nodeData.data.userPrompt || '';
              }
          });
          
          return {
              el, systemPrompt, userPrompt
          }
      }    
  })
  </script>
  