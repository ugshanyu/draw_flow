<template>
  <nodeHeader title="Add"/>
</template>

<script>
import { defineComponent, ref, getCurrentInstance, nextTick, onMounted } from 'vue'
import nodeHeader from './nodeHeader.vue'
import { ElMessageBox } from 'element-plus'

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
        const handleClose = (done) => {
            ElMessageBox.confirm('Are you sure you want to close this?')
                .then(() => {
                    done();
                })
                .catch(() => {
                    // catch error
                });
        };

        onMounted(async () => {
            await nextTick();
            if (el.value && el.value.parentElement && el.value.parentElement.parentElement) {
                nodeId.value = parseInt(el.value.parentElement.parentElement.id.slice(5));
                dataNode.value = df.getNodeFromId(nodeId.value);
                textarea.value = dataNode.value.data.script;
            }
        });

        df = getCurrentInstance().appContext.config.globalProperties.$df?.value;

        const updateSelect = (value) => {
            dataNode.value.data.script = value;
            df.updateNodeDataFromId(nodeId.value, dataNode.value);
        };

        return {
            el,
            drawer,
            direction,
            handleClose,
            textarea,
            updateSelect
        };
    }
})
</script>

<style scoped>
p {
    margin: 5px;
    margin-bottom: 10px;
}
</style>
