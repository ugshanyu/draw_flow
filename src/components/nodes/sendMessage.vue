<template>
    <div ref="el">
        <nodeHeader title="Send Message"/>
        <p>UserId</p>
        <el-input v-model="userId" placeholder="UserId" size="small"></el-input>
        <p>Text</p>
        <el-input v-model="text" placeholder="Text" size="small"></el-input>
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
        const userId = ref('');
        const text = ref('');

        // Function to handle data updates
        const updateNodeData = () => {
            const nodeData = df.getNodeFromId(nodeId.value);
            nodeData.data = { userId: userId.value, text: text.value };
            df.updateNodeDataFromId(nodeId.value, nodeData);
        };

        // Watch for changes in the input fields and update node data accordingly
        watch(userId, updateNodeData);
        watch(text, updateNodeData);

        onMounted(async () => {
            await nextTick();
            nodeId.value = el.value.parentElement.parentElement.id.slice(5);
            const nodeData = df.getNodeFromId(nodeId.value);
            const data = findDeepestData(nodeData)
            if (data) {
                userId.value = data.userId || '';
                text.value = data.text || '';
            }
        });
        
        return {
            el, userId, text
        }
    }    
})
</script>
