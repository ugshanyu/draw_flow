<template>
    <div ref="el">
      <nodeHeader title="Script" />
      <p>Open in navbar</p>
      <el-button type="info" size="small" @click="drawer = true">Edit</el-button>
      <teleport to="body">
        <el-drawer
          v-model="drawer"
          title="Edit Options"
          :direction="direction"
          :before-close="handleClose"
        >
          <p>Autosave</p>
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
      let df = null;
      const nodeId = ref(0);
      const dataNode = ref({});
      const drawer = ref(false);
      const direction = ref('rtl');
      const savedValue = ref('');
      const isSaved = computed(() => textarea.value === savedValue.value);
  
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
        df.updateNodeDataFromId(nodeId.value, dataNode.value);
      }
  
      const saveChanges = () => {
        savedValue.value = textarea.value;
        updateSelect();
      }
  
      onMounted(async () => {
        await nextTick()
        nodeId.value = el.value.parentElement.parentElement.id.slice(5)
        dataNode.value = df.getNodeFromId(nodeId.value)
        textarea.value = dataNode.value.data.script;
        savedValue.value = textarea.value;
      });
  
      return {
        el,
        drawer,
        direction,
        handleClose,
        textarea,
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
    height: 400px;
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