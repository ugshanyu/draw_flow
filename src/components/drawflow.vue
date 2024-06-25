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
        "74": {
          "id": 74,
          "name": "case_prompt",
          "data": {
            "id": 74,
            "name": "case_prompt",
            "data": {
              "id": 74,
              "name": "case_prompt",
              "data": {
                "id": 74,
                "name": "case_prompt",
                "data": {
                  "id": 74,
                  "name": "case_prompt",
                  "data": {
                    "id": 74,
                    "name": "case_prompt",
                    "data": {
                      "script": "213212312"
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
                    "pos_x": 1179.828979492187,
                    "pos_y": 833.4263916015623,
                    "script": "44",
                    "importStatements": "44"
                  },
                  "class": "case_prompt",
                  "html": "case_prompt",
                  "typenode": "vue",
                  "inputs": {
                    "input_1": {
                      "connections": [
                        {
                          "node": "76",
                          "input": "output_1"
                        }
                      ]
                    }
                  },
                  "outputs": {
                    "output_1": {
                      "connections": []
                    }
                  },
                  "pos_x": 1310,
                  "pos_y": 117.88888888888889,
                  "script": "33333333333333333",
                  "importStatements": "333"
                },
                "class": "case_prompt",
                "html": "case_prompt",
                "typenode": "vue",
                "inputs": {
                  "input_1": {
                    "connections": [
                      {
                        "node": "76",
                        "input": "output_1"
                      }
                    ]
                  }
                },
                "outputs": {
                  "output_1": {
                    "connections": []
                  }
                },
                "pos_x": 1293.5,
                "pos_y": 217,
                "script": "Ting",
                "importStatements": "Tes"
              },
              "class": "case_prompt",
              "html": "case_prompt",
              "typenode": "vue",
              "inputs": {
                "input_1": {
                  "connections": [
                    {
                      "node": "76",
                      "input": "output_1"
                    }
                  ]
                }
              },
              "outputs": {
                "output_1": {
                  "connections": []
                }
              },
              "pos_x": 1293.5,
              "pos_y": 217,
              "script": "Ting",
              "importStatements": "Test"
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
            "pos_x": 973,
            "pos_y": 437
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
          "pos_x": 973,
          "pos_y": 437
        },
        "75": {
          "id": 75,
          "name": "switch",
          "data": {
            "id": 75,
            "name": "switch",
            "data": {
              "input": "case1"
            },
            "class": "switch",
            "html": "switch",
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
            "pos_x": 584.9090909090909,
            "pos_y": 444
          },
          "class": "switch",
          "html": "switch",
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
          "pos_x": 584.9090909090909,
          "pos_y": 444
        },
        "76": {
          "id": 76,
          "name": "base_prompt",
          "data": {
            "id": 76,
            "name": "base_prompt",
            "data": {
              "id": 76,
              "name": "base_prompt",
              "data": {
                "id": 76,
                "name": "base_prompt",
                "data": {
                  "id": 76,
                  "name": "base_prompt",
                  "data": {
                    "id": 76,
                    "name": "base_prompt",
                    "data": {
                      "id": 76,
                      "name": "base_prompt",
                      "data": {
                        "id": 76,
                        "name": "base_prompt",
                        "data": {
                          "id": 76,
                          "name": "base_prompt",
                          "data": {
                            "id": 76,
                            "name": "base_prompt",
                            "data": {
                              "basePrompt": "what"
                            },
                            "class": "base_prompt",
                            "html": "base_prompt",
                            "typenode": "vue",
                            "inputs": {},
                            "outputs": {},
                            "pos_x": 877,
                            "pos_y": 288
                          },
                          "class": "base_prompt",
                          "html": "base_prompt",
                          "typenode": "vue",
                          "inputs": {},
                          "outputs": {},
                          "pos_x": 877,
                          "pos_y": 288
                        },
                        "class": "base_prompt",
                        "html": "base_prompt",
                        "typenode": "vue",
                        "inputs": {},
                        "outputs": {},
                        "pos_x": 877,
                        "pos_y": 288
                      },
                      "class": "base_prompt",
                      "html": "base_prompt",
                      "typenode": "vue",
                      "inputs": {},
                      "outputs": {},
                      "pos_x": 877,
                      "pos_y": 288
                    },
                    "class": "base_prompt",
                    "html": "base_prompt",
                    "typenode": "vue",
                    "inputs": {},
                    "outputs": {},
                    "pos_x": 877,
                    "pos_y": 288
                  },
                  "class": "base_prompt",
                  "html": "base_prompt",
                  "typenode": "vue",
                  "inputs": {},
                  "outputs": {},
                  "pos_x": 877,
                  "pos_y": 288
                },
                "class": "base_prompt",
                "html": "base_prompt",
                "typenode": "vue",
                "inputs": {},
                "outputs": {},
                "pos_x": 877,
                "pos_y": 288
              },
              "class": "base_prompt",
              "html": "base_prompt",
              "typenode": "vue",
              "inputs": {},
              "outputs": {},
              "pos_x": 877,
              "pos_y": 288
            },
            "class": "base_prompt",
            "html": "base_prompt",
            "typenode": "vue",
            "inputs": {},
            "outputs": {},
            "pos_x": 877,
            "pos_y": 288
          },
          "class": "base_prompt",
          "html": "base_prompt",
          "typenode": "vue",
          "inputs": {},
          "outputs": {},
          "pos_x": 877,
          "pos_y": 288
        }
      }
    }
  }
})


//        editor.value.import({
//   "drawflow": {
//     "Home": {
//       "data": {
//         "5": {
//           "id": 5,
//           "name": "handleUser",
//           "data": {
//             "id": 5,
//             "name": "handleUser",
//             "data": {
//               "key": "userInfoVariable "
//             },
//             "class": "handleUser",
//             "html": "handleUser",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "8",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "7",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 612,
//             "pos_y": 800.8333333333334
//           },
//           "class": "handleUser",
//           "html": "handleUser",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "8",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "7",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 612,
//           "pos_y": 800.8333333333334
//         },
//         "6": {
//           "id": 6,
//           "name": "fbWebhook",
//           "data": {},
//           "class": "fbWebhook",
//           "html": "fbWebhook",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": []
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "8",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": -169,
//           "pos_y": 826.5
//         },
//         "7": {
//           "id": 7,
//           "name": "switch",
//           "data": {
//             "id": 7,
//             "name": "switch",
//             "data": {
//               "input": "sendMessage"
//             },
//             "class": "switch",
//             "html": "switch",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "5",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "9",
//                     "output": "input_1"
//                   },
//                   {
//                     "node": "10",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 986.8333333333334,
//             "pos_y": 798
//           },
//           "class": "switch",
//           "html": "switch",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "5",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "9",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "10",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 986.8333333333334,
//           "pos_y": 798
//         },
//         "8": {
//           "id": 8,
//           "name": "variableSet",
//           "data": {
//             "id": 8,
//             "name": "variableSet",
//             "data": {
//               "id": 8,
//               "name": "variableSet",
//               "data": {
//                 "id": 8,
//                 "name": "variableSet",
//                 "data": {
//                   "key": "incomingMessage"
//                 },
//                 "class": "variableSet",
//                 "html": "variableSet",
//                 "typenode": "vue",
//                 "inputs": {
//                   "input_1": {
//                     "connections": []
//                   }
//                 },
//                 "outputs": {
//                   "output_1": {
//                     "connections": []
//                   }
//                 },
//                 "pos_x": 564.5234680175781,
//                 "pos_y": 1243.0078430175781,
//                 "key": "incomingMessage"
//               },
//               "class": "variableSet",
//               "html": "variableSet",
//               "typenode": "vue",
//               "inputs": {
//                 "input_1": {
//                   "connections": [
//                     {
//                       "node": "6",
//                       "input": "output_1"
//                     }
//                   ]
//                 }
//               },
//               "outputs": {
//                 "output_1": {
//                   "connections": [
//                     {
//                       "node": "5",
//                       "output": "input_1"
//                     }
//                   ]
//                 }
//               },
//               "pos_x": 219,
//               "pos_y": 797.2307692307693,
//               "key": "incomingMessage"
//             },
//             "class": "variableSet",
//             "html": "variableSet",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "6",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "5",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 219,
//             "pos_y": 797.2307692307693
//           },
//           "class": "variableSet",
//           "html": "variableSet",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "6",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "5",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 219,
//           "pos_y": 794.5
//         },
//         "9": {
//           "id": 9,
//           "name": "switchCase",
//           "data": {
//             "id": 9,
//             "name": "switchCase",
//             "data": {
//               "input": "True"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "7",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "11",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 1281,
//             "pos_y": 598
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "7",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "11",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 1281,
//           "pos_y": 598
//         },
//         "10": {
//           "id": 10,
//           "name": "switchCase",
//           "data": {
//             "id": 10,
//             "name": "switchCase",
//             "data": {
//               "input": "False"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "7",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 1281.8333333333333,
//             "pos_y": 1028
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "7",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 1281.8333333333333,
//           "pos_y": 1028
//         },
//         "11": {
//           "id": 11,
//           "name": "llmGenerate",
//           "data": {
//             "id": 11,
//             "name": "llmGenerate",
//             "data": {
//               "systemPrompt": "system_prompt",
//               "userPrompt": "\"User says:\" + incomingMessage[\"text\"]"
//             },
//             "class": "llmGenerate",
//             "html": "llmGenerate",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "9",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "13",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 1712,
//             "pos_y": 576
//           },
//           "class": "llmGenerate",
//           "html": "llmGenerate",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "9",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "13",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 1712,
//           "pos_y": 576
//         },
//         "12": {
//           "id": 12,
//           "name": "globalVariable",
//           "data": {
//             "id": 12,
//             "name": "globalVariable",
//             "data": {
//               "id": 12,
//               "name": "globalVariable",
//               "data": {
//                 "key": "system_prompt",
//                 "valueHolder": "This is new prompt",
//                 "method": "string"
//               },
//               "class": "globalVariable",
//               "html": "globalVariable",
//               "typenode": "vue",
//               "inputs": {},
//               "outputs": {},
//               "pos_x": 1306.0161590576167,
//               "pos_y": 284.12837982177723,
//               "key": "system_prompt",
//               "valueholder": "This is new prompt",
//               "valueHolder": "This is new prompt"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1301,
//             "pos_y": 266
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1301,
//           "pos_y": 266
//         },
//         "13": {
//           "id": 13,
//           "name": "extractOutput",
//           "data": {},
//           "class": "extractOutput",
//           "html": "extractOutput",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "11",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "21",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 2077,
//           "pos_y": 623
//         },
//         "14": {
//           "id": 14,
//           "name": "switch",
//           "data": {
//             "id": 14,
//             "name": "switch",
//             "data": {
//               "input": "type"
//             },
//             "class": "switch",
//             "html": "switch",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "21",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "15",
//                     "output": "input_1"
//                   },
//                   {
//                     "node": "16",
//                     "output": "input_1"
//                   },
//                   {
//                     "node": "17",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 2661,
//             "pos_y": 604
//           },
//           "class": "switch",
//           "html": "switch",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "21",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "15",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "16",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "17",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "24",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 2661,
//           "pos_y": 604
//         },
//         "15": {
//           "id": 15,
//           "name": "switchCase",
//           "data": {
//             "id": 15,
//             "name": "switchCase",
//             "data": {
//               "input": "text"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "14",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "18",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 2949,
//             "pos_y": 326
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "14",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "18",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 2949,
//           "pos_y": 326
//         },
//         "16": {
//           "id": 16,
//           "name": "switchCase",
//           "data": {
//             "id": 16,
//             "name": "switchCase",
//             "data": {
//               "input": "function"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "14",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "22",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 3028,
//             "pos_y": 604
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "14",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "22",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3028,
//           "pos_y": 604
//         },
//         "17": {
//           "id": 17,
//           "name": "switchCase",
//           "data": {
//             "id": 17,
//             "name": "switchCase",
//             "data": {
//               "input": "handle_assistant"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "14",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "23",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 2954,
//             "pos_y": 879
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "14",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "23",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3031,
//           "pos_y": 774
//         },
//         "18": {
//           "id": 18,
//           "name": "sendMessage",
//           "data": {
//             "id": 18,
//             "name": "sendMessage",
//             "data": {
//               "userId": "incomingMessage[\"id\"]",
//               "text": "llm_generated[\"text']"
//             },
//             "class": "sendMessage",
//             "html": "sendMessage",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "15",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 3379,
//             "pos_y": 302
//           },
//           "class": "sendMessage",
//           "html": "sendMessage",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "15",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 3379,
//           "pos_y": 302
//         },
//         "21": {
//           "id": 21,
//           "name": "variableSet",
//           "data": {
//             "id": 21,
//             "name": "variableSet",
//             "data": {
//               "id": 21,
//               "name": "variableSet",
//               "data": {
//                 "key": "llm_generated"
//               },
//               "class": "variableSet",
//               "html": "variableSet",
//               "typenode": "vue",
//               "inputs": {
//                 "input_1": {
//                   "connections": []
//                 }
//               },
//               "outputs": {
//                 "output_1": {
//                   "connections": []
//                 }
//               },
//               "pos_x": 2379.3740012428975,
//               "pos_y": 229.47265624999994,
//               "key": "llm_generated"
//             },
//             "class": "variableSet",
//             "html": "variableSet",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "13",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "14",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 2371,
//             "pos_y": 196
//           },
//           "class": "variableSet",
//           "html": "variableSet",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "13",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "14",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 2370,
//           "pos_y": 196
//         },
//         "22": {
//           "id": 22,
//           "name": "functionWrapper",
//           "data": {},
//           "class": "functionWrapper",
//           "html": "functionWrapper",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "16",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "35",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3383,
//           "pos_y": 600.375
//         },
//         "23": {
//           "id": 23,
//           "name": "handleAssistant",
//           "data": {
//             "id": 23,
//             "name": "handleAssistant",
//             "data": {
//               "key": "userInfoVariable "
//             },
//             "class": "handleAssistant",
//             "html": "handleAssistant",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "17",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 3389,
//             "pos_y": 881
//           },
//           "class": "handleAssistant",
//           "html": "handleAssistant",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "17",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "36",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3379,
//           "pos_y": 774
//         },
//         "24": {
//           "id": 24,
//           "name": "switchCase",
//           "data": {
//             "id": 24,
//             "name": "switchCase",
//             "data": {
//               "input": "change_topic"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "14",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 3026,
//             "pos_y": 961
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "14",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "34",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3037,
//           "pos_y": 960.625
//         },
//         "27": {
//           "id": 27,
//           "name": "globalVariable",
//           "data": {
//             "id": 27,
//             "name": "globalVariable",
//             "data": {
//               "key": "current_topic",
//               "valueHolder": "",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1880.0283813476562,
//             "pos_y": 93.26080322265625,
//             "key": "current_topic",
//             "valueholder": ""
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1714,
//           "pos_y": 264
//         },
//         "28": {
//           "id": 28,
//           "name": "globalVariable",
//           "data": {
//             "id": 28,
//             "name": "globalVariable",
//             "data": {
//               "key": "prompt_1",
//               "valueHolder": "Testing we are testing",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1858.7661743164056,
//             "pos_y": -41.12152099609375,
//             "key": "prompt_1",
//             "valueholder": "Testing we are testing"
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1061.625,
//           "pos_y": -629
//         },
//         "29": {
//           "id": 29,
//           "name": "globalVariable",
//           "data": {
//             "id": 29,
//             "name": "globalVariable",
//             "data": {
//               "key": "prompt_2",
//               "valueHolder": "Testing we are testing",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1872.5161743164053,
//             "pos_y": -224.87152099609366,
//             "key": "prompt_2",
//             "valueholder": "Testing we are testing"
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1391,
//           "pos_y": -629
//         },
//         "30": {
//           "id": 30,
//           "name": "globalVariable",
//           "data": {
//             "id": 30,
//             "name": "globalVariable",
//             "data": {
//               "key": "prompt_3",
//               "valueHolder": "We are testing",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1863.76609802246,
//             "pos_y": -520.4966735839843,
//             "key": "prompt_3",
//             "valueholder": "We are testing"
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1723,
//           "pos_y": -628
//         },
//         "31": {
//           "id": 31,
//           "name": "globalVariable",
//           "data": {
//             "id": 31,
//             "name": "globalVariable",
//             "data": {
//               "key": "prompt_4",
//               "valueHolder": "Testing we are testing",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1334.3911743164058,
//             "pos_y": -328.62167358398426,
//             "key": "prompt_4",
//             "valueholder": "Testing we are testing"
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1058,
//           "pos_y": -351
//         },
//         "32": {
//           "id": 32,
//           "name": "globalVariable",
//           "data": {
//             "id": 32,
//             "name": "globalVariable",
//             "data": {
//               "key": "prompt_5",
//               "valueHolder": "Testing we are testing",
//               "method": "string"
//             },
//             "class": "globalVariable",
//             "html": "globalVariable",
//             "typenode": "vue",
//             "inputs": {},
//             "outputs": {},
//             "pos_x": 1501.2661743164058,
//             "pos_y": -201.74659729003895,
//             "key": "prompt_5",
//             "valueholder": "Testing we are testing"
//           },
//           "class": "globalVariable",
//           "html": "globalVariable",
//           "typenode": "vue",
//           "inputs": {},
//           "outputs": {},
//           "pos_x": 1394,
//           "pos_y": -348
//         },
//         "33": {
//           "id": 33,
//           "name": "llmGenerate",
//           "data": {
//             "id": 33,
//             "name": "llmGenerate",
//             "data": {
//               "systemPrompt": "system_prompt",
//               "userPrompt": "current_topic + \"\\nUser says:\" + incomingMessage[\"text\"]"
//             },
//             "class": "llmGenerate",
//             "html": "llmGenerate",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "34",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 3781,
//             "pos_y": 933
//           },
//           "class": "llmGenerate",
//           "html": "llmGenerate",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "34",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "41",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3783,
//           "pos_y": 940
//         },
//         "34": {
//           "id": 34,
//           "name": "changeTopic",
//           "data": {
//             "id": 34,
//             "name": "changeTopic",
//             "data": {
//               "key": "current_topic = llm_generated[0]"
//             },
//             "class": "changeTopic",
//             "html": "changeTopic",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": []
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 3570.057983398436,
//             "pos_y": 1053.3367156982417,
//             "key": "current_topic = llm_generated[0]"
//           },
//           "class": "changeTopic",
//           "html": "changeTopic",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "24",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "33",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3380,
//           "pos_y": 960
//         },
//         "35": {
//           "id": 35,
//           "name": "llmGenerate",
//           "data": {
//             "id": 35,
//             "name": "llmGenerate",
//             "data": {
//               "systemPrompt": "system_prompt",
//               "userPrompt": ""
//             },
//             "class": "llmGenerate",
//             "html": "llmGenerate",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "22",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4454,
//             "pos_y": 200
//           },
//           "class": "llmGenerate",
//           "html": "llmGenerate",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "22",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 4451.888888888889,
//           "pos_y": 200
//         },
//         "36": {
//           "id": 36,
//           "name": "switch",
//           "data": {
//             "id": 36,
//             "name": "switch",
//             "data": {
//               "input": "status"
//             },
//             "class": "switch",
//             "html": "switch",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "23",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": [
//                   {
//                     "node": "38",
//                     "output": "input_1"
//                   },
//                   {
//                     "node": "37",
//                     "output": "input_1"
//                   }
//                 ]
//               }
//             },
//             "pos_x": 3809,
//             "pos_y": 776
//           },
//           "class": "switch",
//           "html": "switch",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "23",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "38",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "37",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 3809,
//           "pos_y": 776
//         },
//         "37": {
//           "id": 37,
//           "name": "switchCase",
//           "data": {
//             "id": 37,
//             "name": "switchCase",
//             "data": {
//               "input": "True"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "36",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4359,
//             "pos_y": 702
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "36",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "39",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 4359,
//           "pos_y": 702
//         },
//         "38": {
//           "id": 38,
//           "name": "switchCase",
//           "data": {
//             "id": 38,
//             "name": "switchCase",
//             "data": {
//               "input": "False"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "36",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4358,
//             "pos_y": 860.625
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "36",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "40",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 4358,
//           "pos_y": 860.625
//         },
//         "39": {
//           "id": 39,
//           "name": "sendMessage",
//           "data": {
//             "id": 39,
//             "name": "sendMessage",
//             "data": {
//               "userId": "incomingMessage[\"id\"]",
//               "text": "\"Амжилттай явууллаа\""
//             },
//             "class": "sendMessage",
//             "html": "sendMessage",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "37",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4860,
//             "pos_y": 546.625
//           },
//           "class": "sendMessage",
//           "html": "sendMessage",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "37",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 4860,
//           "pos_y": 546
//         },
//         "40": {
//           "id": 40,
//           "name": "sendMessage",
//           "data": {
//             "id": 40,
//             "name": "sendMessage",
//             "data": {
//               "userId": "incomingMessage[\"id\"]",
//               "text": "\"Алдаа гарлаа\""
//             },
//             "class": "sendMessage",
//             "html": "sendMessage",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "38",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4863,
//             "pos_y": 830
//           },
//           "class": "sendMessage",
//           "html": "sendMessage",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "38",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 4864,
//           "pos_y": 835
//         },
//         "41": {
//           "id": 41,
//           "name": "extractOutput",
//           "data": {},
//           "class": "extractOutput",
//           "html": "extractOutput",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "33",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "42",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 4066,
//           "pos_y": 1527
//         },
//         "42": {
//           "id": 42,
//           "name": "variableSet",
//           "data": {
//             "id": 42,
//             "name": "variableSet",
//             "data": {
//               "key": "llm_generated"
//             },
//             "class": "variableSet",
//             "html": "variableSet",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": []
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4616.145019531249,
//             "pos_y": 1553.7032645089284,
//             "key": "llm_generated"
//           },
//           "class": "variableSet",
//           "html": "variableSet",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "41",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "43",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 4509,
//           "pos_y": 1509.4285714285713
//         },
//         "43": {
//           "id": 43,
//           "name": "switch",
//           "data": {
//             "id": 43,
//             "name": "switch",
//             "data": {
//               "input": "type"
//             },
//             "class": "switch",
//             "html": "switch",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "42",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 4928,
//             "pos_y": 1505
//           },
//           "class": "switch",
//           "html": "switch",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "42",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "44",
//                   "output": "input_1"
//                 },
//                 {
//                   "node": "46",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 4928,
//           "pos_y": 1505
//         },
//         "44": {
//           "id": 44,
//           "name": "switchCase",
//           "data": {
//             "id": 44,
//             "name": "switchCase",
//             "data": {
//               "input": "text"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "43",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 5216,
//             "pos_y": 1231
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "43",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "45",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 5225,
//           "pos_y": 1232.375
//         },
//         "45": {
//           "id": 45,
//           "name": "sendMessage",
//           "data": {
//             "id": 45,
//             "name": "sendMessage",
//             "data": {
//               "userId": "incomingMessage[\"id\"]",
//               "text": "llm_generated[\"text']"
//             },
//             "class": "sendMessage",
//             "html": "sendMessage",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "44",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 5653,
//             "pos_y": 1213
//           },
//           "class": "sendMessage",
//           "html": "sendMessage",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "44",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 5654,
//           "pos_y": 1208
//         },
//         "46": {
//           "id": 46,
//           "name": "switchCase",
//           "data": {
//             "id": 46,
//             "name": "switchCase",
//             "data": {
//               "input": "function"
//             },
//             "class": "switchCase",
//             "html": "switchCase",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "43",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 5209,
//             "pos_y": 1788
//           },
//           "class": "switchCase",
//           "html": "switchCase",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "43",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "47",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 5209,
//           "pos_y": 1788
//         },
//         "47": {
//           "id": 47,
//           "name": "functionWrapper",
//           "data": {},
//           "class": "functionWrapper",
//           "html": "functionWrapper",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "46",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": [
//                 {
//                   "node": "48",
//                   "output": "input_1"
//                 }
//               ]
//             }
//           },
//           "pos_x": 5666,
//           "pos_y": 1786
//         },
//         "48": {
//           "id": 48,
//           "name": "llmGenerate",
//           "data": {
//             "id": 48,
//             "name": "llmGenerate",
//             "data": {
//               "systemPrompt": "system_prompt",
//               "userPrompt": ""
//             },
//             "class": "llmGenerate",
//             "html": "llmGenerate",
//             "typenode": "vue",
//             "inputs": {
//               "input_1": {
//                 "connections": [
//                   {
//                     "node": "47",
//                     "input": "output_1"
//                   }
//                 ]
//               }
//             },
//             "outputs": {
//               "output_1": {
//                 "connections": []
//               }
//             },
//             "pos_x": 6110,
//             "pos_y": 1761
//           },
//           "class": "llmGenerate",
//           "html": "llmGenerate",
//           "typenode": "vue",
//           "inputs": {
//             "input_1": {
//               "connections": [
//                 {
//                   "node": "47",
//                   "input": "output_1"
//                 }
//               ]
//             }
//           },
//           "outputs": {
//             "output_1": {
//               "connections": []
//             }
//           },
//           "pos_x": 6110,
//           "pos_y": 1761
//         }
//       }
//     }
//   }
// })
      
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