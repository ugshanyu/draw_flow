<template>
    <div ref="el">
        <nodeHeader title="Change"/>
        <p>Key</p>
        <el-input v-model="key" df-key placeholder="Key" size="small"></el-input>
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
        let df = null;
        const key = ref('');
        const dataNode = ref({});

        df = getCurrentInstance().appContext.config.globalProperties.$df.value;

        watch(key, (newKey) => {
            dataNode.value.data.key = newKey;
            df.updateNodeDataFromId(nodeId.value, dataNode.value);
        });

        onMounted(async () => {
            await nextTick();
            nodeId.value = el.value.parentElement.parentElement.id.slice(5);
            dataNode.value = df.getNodeFromId(nodeId.value);

            key.value = dataNode.value.data.key;
        });

        return {
            el,
            key
        }
    }
})
</script>