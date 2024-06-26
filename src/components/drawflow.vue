<template>
  <el-container>
    <el-header class="header">
      <h3>Drawflow Example vue3</h3>
      <el-button type="primary" @click="exportEditor">Export</el-button>
    </el-header>
    <el-container class="container">
      <el-aside width="250px" class="column">
        <div class="node-list-container">
          <ul>
            <li v-for="n in listNodes" :key="n" draggable="true" :data-node="n.item" @dragstart="drag($event)" class="drag-drawflow">
              <div class="node" :style="`background: ${n.color}`">{{ n.name }}</div>
            </li>
          </ul>
        </div>
      </el-aside>
      <el-main>
        <div id="drawflow" @drop="drop($event)" @dragover="allowDrop($event)"></div>
      </el-main>
    </el-container>
  </el-container>
  <el-dialog
    v-model="dialogVisible"
    title="Export"
    width="50%"
  >
    <span>Data:</span>
    <pre><code>{{dialogData}}</code></pre>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogVisible = false">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<script>

import Drawflow from 'drawflow'
import styleDrawflow from 'drawflow/dist/drawflow.min.css'
import style from '../assets/style.css' 
import { onMounted, shallowRef, h, getCurrentInstance, render, readonly, ref } from 'vue'
import Node1 from './nodes/node1.vue'
import Node2 from './nodes/node2.vue'
import Node3 from './nodes/node3.vue'
import BasePrompt from './nodes/base_prompt.vue'
import CasePrompt from './nodes/case_prompt.vue'
import Input from './nodes/input.vue'
import Add from './nodes/add.vue'
import GlobalVariable from './nodes/variable.vue'
import LlmGenerate from './nodes/llmGenerate.vue'
import FbWebhook from './nodes/fbWebhook.vue'
import Switch from './nodes/switch.vue'
import SwitchSelect from './nodes/switchSelect.vue'
import SwitchCase from './nodes/switchCase.vue'
import ExtractOutput from './nodes/extractOutput.vue'
import FunctionWrapper from './nodes/functionWrapper.vue'
import VariableSet from './nodes/variableSet.vue'
import ChangeTopic from './nodes/changeTopic.vue'
import HandleAssistant from './nodes/handleAssistant.vue'
import SendMessage from './nodes/sendMessage.vue'
import HandleUser from './nodes/handleUser.vue'

export default {
  name: 'drawflow',
  setup() {
   const listNodes = readonly([
        {
            name: 'Get/Post',
            color: '#49494970',
            item: 'Node1',
            input:0,
            output:1
        },
        {
            name: 'Script',
            color: 'blue',
            item: 'Node2',
            input:1,
            output:1
        },
         {
            name: 'console.log',
            color: '#ff9900',
            item: 'Node3',
            input:1,
            output:0
        },
        {
            name: 'Base prompt',
            color: 'purple',
            item: 'base_prompt',
            input:0,
            output:0
        },
        {
            name: 'Case prompt',
            color: 'green',
            item: 'case_prompt',
            input:1,
            output:1
        },
        {
          name: 'Input',
          color: 'darkblue',
          item: 'input',
          input:0,
          output:1
        },
        {
          name: 'Add',
          color: 'darkpurple',
          item: 'add',
          input:2,
          output:1
        },
        {
          name: 'GlobalVariable',
          color: 'green',
          item: 'globalVariable',
          input:0,
          output:0
        },
        {
          name: 'LLMGenerate',
          color: 'darkwhite',
          item: 'llmGenerate',
          input:1,
          output:1
        },
        {
          name: 'FbWebhook',
          color: 'darkblue',
          item: 'fbWebhook',
          input:1,
          output:1
        },
        {
          name: 'Switch',
          color: 'darkblue',
          item: 'switch',
          input:1,
          output:1
        },
        {
          name: 'SwitchSelect',
          color: 'darkblue',
          item: 'switchSelect',
          input:1,
          output:1
        },
        {
          name: 'SwitchCase',
          color: 'darkblue',
          item: 'switchCase',
          input:1,
          output:1
        },
        {
          name: 'Extract Output',
          color: 'darkblue',
          item: 'extractOutput',
          input:1,
          output:1
        },
        {
          name: 'Function Wrapper',
          color: 'darkblue',
          item: 'functionWrapper',
          input:1,
          output:1
        },
        {
          name: 'Send Message',
          color: 'darkblue',
          item: 'sendMessage',
          input:1,
          output:1
        },
        {
          name: 'Variable Set',
          color: 'darkblue',
          item: 'variableSet',
          input:1,
          output:1
        },
        {
          name: 'Handle Assistant',
          color: 'darkblue',
          item: 'handleAssistant',
          input:1,
          output:1
        },
        {
          name: 'Handle User',
          color: 'darkblue',
          item: 'handleUser',
          input:1,
          output:1
        },
        {
          name: 'Change Topic',
          color: 'darkblue',
          item: 'changeTopic',
          input:1,
          output:1
        }
    ])
   
   const editor = shallowRef({})
   const dialogVisible = ref(false)
   const dialogData = ref({})
   const Vue = { version: 3, h, render };
   const internalInstance = getCurrentInstance()
   internalInstance.appContext.app._context.config.globalProperties.$df = editor;
   
    function exportEditor() {
      dialogData.value = editor.value.export();
      dialogVisible.value = true;
    }

    const drag = (ev) => {
      if (ev.type === "touchstart") {
        mobile_item_selec = ev.target.closest(".drag-drawflow").getAttribute('data-node');
      } else {
      ev.dataTransfer.setData("node", ev.target.getAttribute('data-node'));
      }
    }
    const drop = (ev) => {
      if (ev.type === "touchend") {
        var parentdrawflow = document.elementFromPoint( mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY).closest("#drawflow");
        if(parentdrawflow != null) {
          addNodeToDrawFlow(mobile_item_selec, mobile_last_move.touches[0].clientX, mobile_last_move.touches[0].clientY);
        }
        mobile_item_selec = '';
      } else {
        ev.preventDefault();
        var data = ev.dataTransfer.getData("node");
        addNodeToDrawFlow(data, ev.clientX, ev.clientY);
      }

    }
    const allowDrop = (ev) => {
      ev.preventDefault();
    }

   let mobile_item_selec = '';
   let mobile_last_move = null;
   function positionMobile(ev) {
     mobile_last_move = ev;
   }

    function addNodeToDrawFlow(name, pos_x, pos_y) {
      pos_x = pos_x * ( editor.value.precanvas.clientWidth / (editor.value.precanvas.clientWidth * editor.value.zoom)) - (editor.value.precanvas.getBoundingClientRect().x * ( editor.value.precanvas.clientWidth / (editor.value.precanvas.clientWidth * editor.value.zoom)));
      pos_y = pos_y * ( editor.value.precanvas.clientHeight / (editor.value.precanvas.clientHeight * editor.value.zoom)) - (editor.value.precanvas.getBoundingClientRect().y * ( editor.value.precanvas.clientHeight / (editor.value.precanvas.clientHeight * editor.value.zoom)));
    
      const nodeSelected = listNodes.find(ele => ele.item == name);
      editor.value.addNode(name, nodeSelected.input,  nodeSelected.output, pos_x, pos_y, name, {}, name, 'vue');
      
    }


   onMounted(() => {

      var elements = document.getElementsByClassName('drag-drawflow');
      for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('touchend', drop, false);
        elements[i].addEventListener('touchmove', positionMobile, false);
        elements[i].addEventListener('touchstart', drag, false );
      }
        
       const id = document.getElementById("drawflow");
       editor.value = new Drawflow(id, Vue, internalInstance.appContext.app._context);
       editor.value.start();
       
       editor.value.registerNode('Node1', Node1, {}, {});
       editor.value.registerNode('Node2', Node2, {}, {});
       editor.value.registerNode('Node3', Node3, {}, {});
       editor.value.registerNode('Node3', Node3, {}, {});
       editor.value.registerNode('base_prompt', BasePrompt, {}, {});
       editor.value.registerNode('case_prompt', CasePrompt, {}, {});
       editor.value.registerNode('input', Input, {}, {});
       editor.value.registerNode('add', Add, {}, {})
       editor.value.registerNode('globalVariable', GlobalVariable, {}, {})
       editor.value.registerNode('llmGenerate', LlmGenerate, {}, {})
       editor.value.registerNode('fbWebhook', FbWebhook, {}, {})
       editor.value.registerNode('switch', Switch, {}, {})
       editor.value.registerNode('switchCase', SwitchCase, {}, {})
       editor.value.registerNode('switchSelect', SwitchSelect, {}, {})
       editor.value.registerNode('extractOutput', ExtractOutput, {}, {})
       editor.value.registerNode('functionWrapper', FunctionWrapper, {}, {})
       editor.value.registerNode('variableSet', VariableSet, {}, {})
       editor.value.registerNode('handleAssistant', HandleAssistant, {}, {})
       editor.value.registerNode('changeTopic', ChangeTopic, {}, {})
       editor.value.registerNode('sendMessage', SendMessage, {}, {})
       editor.value.registerNode('handleUser', HandleUser, {}, {})
       editor.value.import({
  "drawflow": {
    "Home": {
      "data": {
        "80": {
          "id": 80,
          "name": "base_prompt",
          "data": {
            "basePrompt": "HelloWHatAreYou"
          },
          "class": "base_prompt",
          "html": "base_prompt",
          "typenode": "vue",
          "inputs": {},
          "outputs": {},
          "pos_x": 722,
          "pos_y": 527
        },
        "81": {
          "id": 81,
          "name": "case_prompt",
          "data": {
            "casePrompt": "Case Hello"
          },
          "class": "case_prompt",
          "html": "case_prompt",
          "typenode": "vue",
          "inputs": {
            "input_1": {
              "connections": []
            }
          },
          "outputs": {
            "output_1": {
              "connections": []
            }
          },
          "pos_x": 328,
          "pos_y": 186
        }
      }
    }
  }
})
      
      })

  return {
    exportEditor, listNodes, drag, drop, allowDrop, dialogVisible, dialogData
  }

  }
}

</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #494949;
}
.container {
  min-height: calc(100vh - 100px);
}
.column {
  border-right: 1px solid #494949;
  display: flex;
  flex-direction: column;
}
.node-list-container {
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 100px);
}
.column ul {
  padding-inline-start: 0px;
  padding: 10px 10px;
  margin: 0;
}
.column li {
  background: transparent;
}
.node {
  border-radius: 8px;
  border: 2px solid #494949;
  display: block;
  height: 60px;
  line-height: 40px;
  padding: 10px;
  margin: 10px 0px;
  cursor: move;
}
#drawflow {
  width: 100%;
  height: 100%;
  text-align: initial;
  background: #2b2c30;
  background-size: 20px 20px;
  background-image: radial-gradient(#494949 1px, transparent 1px);
}
</style>