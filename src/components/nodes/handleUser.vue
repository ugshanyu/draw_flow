<template>
    <div ref="el">
        <nodeHeader title="HandleUser"/>
        <p>User Info Variable</p>
        <el-input v-model="key" placeholder="UserInfoVariable" size="small"></el-input>
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
        const key = ref('');

        // Function to handle data updates
        const updateNodeData = () => {
            const nodeData = df.getNodeFromId(nodeId.value);
            nodeData.data = { key: key.value };
            df.updateNodeDataFromId(nodeId.value, nodeData);
        };

        // Watch for changes in the key field and update node data accordingly
        watch(key, updateNodeData);

        onMounted(async () => {
            await nextTick();
            nodeId.value = el.value.parentElement.parentElement.id.slice(5);
            const nodeData = df.getNodeFromId(nodeId.value);
            const data = findDeepestData(nodeData);
            if (data) {
                key.value = data.key || '';
            }
        });

        return {
            el, key
        }
    }
})
</script>
