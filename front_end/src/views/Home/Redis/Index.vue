<template>
    <div>
        <el-row type="flex" :gutter="20">
            <el-col :span="4">
                <div class="grid-content">
                    <el-button @click="editDialogVisible = true">Add Server</el-button>
                    <el-button @click="freshDatabases">Refresh</el-button>
                    <el-tree 
                        :data="redisServerList" 
                        lazy 
                        :load="loadDatabases"
                        highlight-current
                        :props="redisServerTreeProps"
                        @node-click="clickDatabase">
                        <span class="custom-tree-node" slot-scope="{ node, data }">
                            {{ node.label }}
                            <template v-if="node.level === 1">
                                <span>
                                    <el-button
                                        type="text"
                                        size="mini"
                                        @click.stop="() => openEditDialog(node, data)">
                                        Edit
                                    </el-button>
                                    <el-button
                                        type="text"
                                        size="mini"
                                        @click="() => remove(node, data)">
                                        Delete
                                    </el-button>
                                </span>
                            </template>
                        </span>
                    </el-tree>
                 </div>
            </el-col>
            <el-col :span="20">
                <div class="grid-content">
                    <el-tabs v-model="activeTab.tabName" type="card" v-show="redisServerTabs.length != 0" @tab-remove="removeTab">
                        <el-tab-pane
                            :key="item.tabName"
                            closable 
                            :label="item.tabLabel" 
                            :name="item.tabName" 
                            v-for="(item, index) in redisServerTabs">
                            <key-list :server-id="activeTab.serverId" :db-num="activeTab.dbNum"></key-list>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </el-col>
        </el-row>

        <el-dialog :visible.sync="editDialogVisible">
            <el-form :model="form" ref="form">
                <el-form-item 
                    label="Connection Name" 
                    :label-width="labelWidth" 
                    prop="connectionName"
                    :rules="[
                        { required: true, message: 'Connection name is required.' }
                    ]">
                    <el-input v-model="form.connectionName" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item 
                    label="Host" 
                    :label-width="labelWidth" 
                    prop="host"
                    :rules="[
                        { required: true, message: 'Host is required.' }
                    ]">
                    <el-input v-model="form.host" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item 
                    label="Port" 
                    :label-width="labelWidth" 
                    prop="port"
                    :rules="[
                        { required: true, message: 'Port is required.' }
                    ]">
                    <el-input v-model="form.port" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item 
                    label="Password" 
                    :label-width="labelWidth" 
                    prop="password">
                    <el-input v-model="form.password" auto-complete="off"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="closeEditDialog">Cancel</el-button>
                <el-button type="primary" @click="saveRedisServer">Confirm</el-button>
            </span>
        </el-dialog>  
    </div>
</template>

<script>
import { mapState } from 'vuex'
import * as ActionTypes from '~/store/action-types.js'
import KeyList from './KeyList'

export default {
    components: {
        KeyList
    },
    computed: {
        ...mapState(['redisServerList', 'redisServerTabs'])
    },

    watch: {
        editDialogVisible(n, o) {
            if (n) {
                if (this.$refs.form != undefined) {
                    this.$refs.form.resetFields()
                }
            }
        }
    },

    data() {
        return {
            activeTab: {
                tabName: null,
                serverId: null,
                dbNum: null,
            },

            editDialogVisible: false,

            labelWidth: '',

            form: {
                id: null,
                connectionName: null,
                host: '127.0.0.1',
                port: 6379,
                password: null
            },

            redisServerTreeProps: {
                label: 'label',
                children: 'children',
                isLeaf: 'leaf'
            }
        }
    },

    mounted() {
        this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_SERVERS)
    },

    methods: {

        loadDatabases(node, resolve) {
            if (node.level === 0) {
                return resolve([])
            }

            this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_DATABASES, node.data.value).then(data => {
                resolve(data)
            })
            
        },

        saveRedisServer() {
            this.$refs.form.validate(validate => {
                if (validate) {
                    this.$store.dispatch(ActionTypes.REDIS_SERVER_ADD_SERVER, {...this.form})
                    return true
                }
                return false
            })
        },

        freshDatabases() {
            this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_SERVERS)
        },

        removeTab(targetName) {
            let activeName = this.activeTab.tabName
            let tabs = this.redisServerTabs
            if (activeName === targetName) {
                this.redisServerTabs.forEach((tab, index) => {
                    if (tab.tabName === targetName) {
                        let nextTab = tabs[index + 1] || tabs[index - 1]
                        if (nextTab) {
                            activeName = nextTab.tabName
                        }
                    }
                })
            }
            this.$store.state.redisServerTabs = tabs.filter(tab => tab.tabName !== targetName)
            this.activeTab.tabName = activeName
        },

        clickDatabase(data, node) {

            if (node.level == 1) {

            }

            if (node.level == 2) {
                let tabName = `${node.parent.data.value}-${data.value}`
                let tab = this.redisServerTabs.find(i => i.tabName === tabName)
                if (tab == null) {
                    let tab = {
                        tabName: `${node.parent.data.value}-${data.value}`,
                        tabLabel: `${node.parent.data.label} - ${data.label}`,
                    }
                    this.$store.dispatch(ActionTypes.COMMON_ADD_TAB, tab)
                }
                this.activeTab.tabName = tabName
                this.activeTab.serverId = node.parent.data.value
                this.activeTab.dbNum = data.value
            }
        },

        openEditDialog(node, data) {
            this.editDialogVisible = true
        },

        closeEditDialog() {
            this.editDialogVisible = false
        },

        remove(node, data) {

        }
    }
}
</script>

<style>
.grid-content {

}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
</style>

