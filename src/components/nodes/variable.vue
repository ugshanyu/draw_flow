<template>
    <div ref="el">
        <nodeHeader  title="GlobalVariable"/>
        <p>Key</p>
    <el-input v-model="key" df-key  placeholder="Key" size="small">
    </el-input>
    <p>Type</p>
    <el-select v-model="method" placeholder="Type" @change="updateSelect" size="small" df-method>
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            >
        </el-option>
    </el-select>
    <p>Value</p>
    <el-input v-model="valueHolder" df-valueHolder placeholder="Value" size="small">
    </el-input>
</div>
</template>
<script>
import { defineComponent, onMounted, getCurrentInstance, readonly, ref, nextTick, watch } from 'vue'
import nodeHeader from './nodeHeader.vue'
import { findDeepestData } from '../../utils'

export default defineComponent({
    components: {
        nodeHeader
    },
    setup() {
        const el = ref(null);
        const nodeId = ref(0);
        let df = null
        const key = ref('');
        const valueHolder = ref('');
        const method = ref('string');
        const dataNode = ref({});
        const options = readonly([
            {
                value: 'int',
                label: 'INT'
            },
            {
                value: 'string',
                label: 'STRING'
            },
            {
                value: 'boolean',
                label: 'BOOLEAN'
            }
        ]);
        
        df = getCurrentInstance().appContext.config.globalProperties.$df.value;

        const updateSelect = (value) => {
            dataNode.value.data.method = value;
            df.updateNodeDataFromId(nodeId.value, dataNode.value);
        }
        
        watch([key, valueHolder], ([newKey, newValueHolder]) => {
            dataNode.value.data.key = newKey;
            dataNode.value.data.valueHolder = newValueHolder;
            df.updateNodeDataFromId(nodeId.value, dataNode.value);
        });
        
        onMounted(async () => {
            await nextTick()
            nodeId.value = el.value.parentElement.parentElement.id.slice(5)
            dataNode.value = df.getNodeFromId(nodeId.value)
            let data = findDeepestData(dataNode.value);
            if(data){
                key.value = data.key;
                valueHolder.value = data.valueHolder;
                method.value = data.method;
            }
        });
        
        return {
            el, key, valueHolder, method, options, updateSelect
        }

    }    
    
})
</script>