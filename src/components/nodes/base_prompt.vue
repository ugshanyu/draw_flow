<template>
    <div ref="el">
      <nodeHeader title="Base Prompt" />
      <p>Open in navbar</p>
      <el-button type="info" size="small" @click="drawer = true">Edit</el-button>
      <teleport to="body">
        <el-drawer
          v-model="drawer"
          :direction="direction"
          :before-close="handleClose"
        >
          <p>Base Prompt:</p>
          <div class="prompt-editor">
            <textarea
              v-model="basePrompt"
              :rows="10"
              @input="handleInput"
              placeholder="Enter your base prompt here"
              class="prompt-textarea"
            ></textarea>
          </div>
          <el-button 
            :type="isSaved ? 'success' : 'primary'" 
            @click="saveChanges"
          >
            {{ isSaved ? '✓ Saved' : 'Save' }}
          </el-button>
        </el-drawer>
      </teleport>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, computed, getCurrentInstance, nextTick, onMounted } from 'vue'
  import nodeHeader from './nodeHeader.vue'
  import { findDeepestData } from '../../utils'
  
  export default defineComponent({
    components: {
      nodeHeader
    },
    setup() {
      const el = ref(null);
      const basePrompt = ref('');
      let df = null;
      const nodeId = ref(0);
      const dataNode = ref({});
      const drawer = ref(false);
      const direction = ref('rtl');
      const savedBasePrompt = ref('');
      const isSaved = computed(() => basePrompt.value === savedBasePrompt.value);
  
      const handleClose = (done) => {
        if (!isSaved.value) {
          if (confirm('You have unsaved changes. Are you sure you want to close this?')) {
            done();
          }
        } else {
          done();
        }
      }
  
      df = getCurrentInstance().appContext.config.globalProperties.$df.value;
  
      const handleInput = () => {
        updateSelect();
      }
  
      const updateSelect = () => {
        const nodeData = df.getNodeFromId(nodeId.value);
        let deepData = findDeepestData(nodeData);
        if (deepData) {
          deepData.basePrompt = basePrompt.value;
        } else {
          nodeData.data = { basePrompt: basePrompt.value };
        }
        df.updateNodeDataFromId(nodeId.value, nodeData);
      }
  
      const saveChanges = () => {
        savedBasePrompt.value = basePrompt.value;
        updateSelect();
      }
  
      onMounted(async () => {
        await nextTick()
        nodeId.value = el.value.parentElement.parentElement.id.slice(5)
        const nodeData = df.getNodeFromId(nodeId.value);
        console.log("Initial node data:", nodeData);
        
        let deepData = findDeepestData(nodeData);
        console.log("Deepest data found:", deepData);
        
        if (deepData && deepData.basePrompt !== undefined) {
          basePrompt.value = deepData.basePrompt;
          console.log("Base prompt value set to:", basePrompt.value);
        } else {
          console.warn("No base prompt data found in the deepest object");
          basePrompt.value = ''; // Set a default value
        }
        savedBasePrompt.value = basePrompt.value;
      });
  
      return {
        el,
        drawer,
        direction,
        handleClose,
        basePrompt,
        handleInput,
        saveChanges,
        isSaved
      }
    },
  })
  </script>
  
  <style scoped>
  p {
    margin: 5px;
    margin-bottom: 10px;
  }
  
  .prompt-editor {
    width: 100%;
    height: 300px;
    margin-bottom: 10px;
  }
  
  .prompt-textarea {
    width: 100%;
    height: 100%;
    font-family: monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    resize: vertical;
  }
  </style>