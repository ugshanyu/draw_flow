<template>
    <div ref="el">
      <nodeHeader title="Base prompt" />
      <p>Open in navbar</p>
      <el-button type="info" size="small" @click="drawer = true">Base prompt</el-button>
      <teleport to="body">
        <el-drawer
          v-model="drawer"
          :direction="direction"
          :before-close="handleClose"
        >
          <p>Base prompt:</p>
          <div class="prompt-editor">
            <textarea
              v-model="nodeData.data.basePrompt"
              :rows="10"
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
  import { defineComponent, ref, computed, watch, getCurrentInstance, nextTick, onMounted } from 'vue'
  import nodeHeader from './nodeHeader.vue'
  
  export default defineComponent({
    components: {
      nodeHeader
    },
    setup() {
      const el = ref(null);
      const nodeData = ref({});
      const savedBasePrompt = ref('');
      let df = null;
      const nodeId = ref(0);
      const drawer = ref(false);
      const direction = ref('rtl');
      const isSaved = computed(() => nodeData.value.data?.basePrompt === savedBasePrompt.value);
  
      const handleClose = (done) => {
        if (!isSaved.value) {
          if (confirm('You have unsaved changes. Are you sure you want to close this?')) {
            if (nodeData.value.data) {
                console.log("value", value)
            //   nodeData.value.data.basePrompt = savedBasePrompt.value; // Reset to last saved value
            }
            done();
          }
        } else {
          done();
        }
      }
  
      df = getCurrentInstance().appContext.config.globalProperties.$df.value;
  
      const updateNodeData = () => {
        df.updateNodeDataFromId(nodeId.value, nodeData.value);
      }
  
      const saveChanges = () => {
        savedBasePrompt.value = nodeData.value.data?.basePrompt || '';
        updateNodeData();
      }
  
      watch(() => nodeData.value, (newVal) => {
        if (newVal && typeof newVal === 'object') {
          if (!newVal.data || typeof newVal.data !== 'object') {
            newVal.data = {};
          }
          if (!newVal.data.hasOwnProperty('basePrompt')) {
            newVal.data.basePrompt = '';
          }
        }
      }, { deep: true });
  
      onMounted(async () => {
        await nextTick()
        nodeId.value = el.value.parentElement.parentElement.id.slice(5)
        nodeData.value = df.getNodeFromId(nodeId.value);
        
        if (!nodeData.value.data || typeof nodeData.value.data !== 'object') {
          nodeData.value.data = {};
        }
        if (!nodeData.value.data.hasOwnProperty('basePrompt')) {
          nodeData.value.data.basePrompt = '';
        }
        savedBasePrompt.value = nodeData.value.data.basePrompt;
      });
  
      return {
        el,
        drawer,
        direction,
        handleClose,
        nodeData,
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