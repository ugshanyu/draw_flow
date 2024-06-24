<template>
    <div ref="el">
      <nodeHeader title="FbWebook"/>
    </div>
</template>

<script>
import { defineComponent, ref, getCurrentInstance, nextTick, onMounted, watch } from 'vue'
import nodeHeader from './nodeHeader.vue'
import { ElMessageBox } from 'element-plus'

export default defineComponent({
    components: {
        nodeHeader
    },
    setup() {
        const el = ref(null);
        const keyText = ref('');
        const valueText = ref('');
        let df = null;
        const nodeId = ref(0);
        const dataNode = ref({});
        const drawer = ref(false);
        const direction = ref('rtl');

        // Debugging changes in inputs
        // watch(keyText, (newVal, oldVal) => {
        // //   console.log(`KeyText changed from ${oldVal} to ${newVal}`);
        // });

        // watch(valueText, (newVal, oldVal) => {
        // //   console.log(`ValueText changed from ${oldVal} to ${newVal}`);
        // });

        const handleClose = (done) => {
            ElMessageBox.confirm('Are you sure you want to close this?')
                .then(() => {
                    done();
                })
                .catch(() => {
                    // Handle error
                });
        };

        onMounted(async () => {
            await nextTick();
            df = getCurrentInstance().appContext.config.globalProperties.$df;
            if (el.value && el.value.parentElement && el.value.parentElement.parentElement) {
                nodeId.value = parseInt(el.value.parentElement.parentElement.id.slice(5));
                dataNode.value = df.getNodeFromId(nodeId.value);
                keyText.value = dataNode.value.data.key;
                valueText.value = dataNode.value.data.value;
            }
        });

        const saveData = () => {
            dataNode.value.data.key = keyText.value;
            dataNode.value.data.value = valueText.value;
            df.updateNodeDataFromId(nodeId.value, dataNode.value);
            console.log('Data saved:', keyText.value, valueText.value);
        };

        return {
            el,
            drawer,
            direction,
            handleClose,
            keyText,
            valueText,
            saveData
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
