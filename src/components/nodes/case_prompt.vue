<template>
  <div ref="el">
    <nodeHeader title="Case Prompt" />
    <p>Open in navbar</p>
    <el-button type="info" size="small" @click="drawer = true">Edit</el-button>
    <teleport to="body">
      <el-drawer
        v-model="drawer"
        :direction="direction"
        :before-close="handleClose"
      >
        <p>case Prompt:</p>
        <div class="prompt-editor">
          <textarea
v-model="casePrompt"
:rows="10"
placeholder="Enter your case prompt here"
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
    const casePrompt = ref('');
    let df = null;
    const nodeId = ref(0);
    const dataNode = ref({});
    const drawer = ref(false);
    const direction = ref('rtl');
    const savedcasePrompt = ref('');
    const isSaved = computed(() => casePrompt.value === savedcasePrompt.value);

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
        deepData.casePrompt = casePrompt.value;
      } else {
        nodeData.data = { casePrompt: casePrompt.value };
      }
      df.updateNodeDataFromId(nodeId.value, { casePrompt: casePrompt.value });
    }

    const saveChanges = () => {
      savedcasePrompt.value = casePrompt.value;
      updateSelect(); // This will now update the model only when save is clicked.
    }

    onMounted(async () => {
      await nextTick()
      nodeId.value = el.value.parentElement.parentElement.id.slice(5)
      const nodeData = df.getNodeFromId(nodeId.value);
      console.log("Initial node data:", nodeData);
      
      let deepData = findDeepestData(nodeData);
      console.log("Deepest data found:", deepData);
      
      if (deepData && deepData.casePrompt !== undefined) {
        casePrompt.value = deepData.casePrompt;
        console.log("case prompt value set to:", casePrompt.value);
      } else {
        console.warn("No case prompt data found in the deepest object");
        casePrompt.value = ''; // Set a default value
      }
      savedcasePrompt.value = casePrompt.value;
    });

    return {
      el,
      drawer,
      direction,
      handleClose,
      casePrompt,
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