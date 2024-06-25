<template>
    <div ref="el">
      <nodeHeader title="Case Prompt" />
      <p>Open in navbar</p>
      <el-button type="info" size="small" @click="drawer = true">Edit</el-button>
      <teleport to="body">
        <el-drawer
          v-model="drawer"
          title="Edit Options"
          :direction="direction"
          :before-close="handleClose"
        >
          <p>Import Statements</p>
          <div class="python-editor">
            <textarea
              v-model="importStatements"
              :rows="4"
              @input="handleInput"
              placeholder="Enter import statements here"
              class="python-textarea"
            ></textarea>
          </div>
          <p>def handle_classified(user_message, sender_id, senderId_info):</p>
          <div class="python-editor">
            <textarea
              v-model="textarea"
              :rows="4"
              df-script
              @input="handleInput"
              placeholder="Please input your Python code here"
              class="python-textarea"
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
  
  export default defineComponent({
    components: {
      nodeHeader
    },
    setup() {
      const el = ref(null);
      const textarea = ref('');
      const importStatements = ref('');
      let df = null;
      const nodeId = ref(0);
      const dataNode = ref({});
      const drawer = ref(false);
      const direction = ref('rtl');
      const savedTextarea = ref('');
      const savedImportStatements = ref('');
      const isSaved = computed(() => 
        textarea.value === savedTextarea.value && 
        importStatements.value === savedImportStatements.value
      );
  
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
        dataNode.value.data.script = textarea.value;
        dataNode.value.data.importStatements = importStatements.value;
        df.updateNodeDataFromId(nodeId.value, dataNode.value);
      }
  
      const saveChanges = () => {
        savedTextarea.value = textarea.value;
        savedImportStatements.value = importStatements.value;
        updateSelect();
      }
  
      onMounted(async () => {
        await nextTick()
        nodeId.value = el.value.parentElement.parentElement.id.slice(5)
        dataNode.value = df.getNodeFromId(nodeId.value)
        textarea.value = dataNode.value.data.script || '';
        importStatements.value = dataNode.value.data.importStatements || '';
        savedTextarea.value = textarea.value;
        savedImportStatements.value = importStatements.value;
      });
  
      return {
        el,
        drawer,
        direction,
        handleClose,
        textarea,
        importStatements,
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
  
  .python-editor {
    width: 100%;
    height: 200px;
    margin-bottom: 10px;
  }
  
  .python-textarea {
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