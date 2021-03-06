<template>
    <div class="container">
        <div class="grid-content">
            <div class="server-btns">
                <el-button @click="addRedisServer">Add Server</el-button>
                <el-button @click="freshDatabaseList">Refresh</el-button>
            </div>
            <div class="server-list" v-loading="loadingDatabaseList">
                <el-tree 
                    :data="redisServerList" 
                    lazy 
                    :load="loadDatabaseList"
                    highlight-current
                    :props="redisServerTreeProps"
                    @node-contextmenu="rightClickTreeNode"
                    @node-click="clickTreeNode">
                    <span class="custom-tree-node" slot-scope="{ node, data }">
                        {{ node.label }}
                        <template v-if="node.level === 1">
                            <span>
                                <el-button
                                    type="text"
                                    size="mini"
                                    @click.stop="() => editRedisServer(node, data)">
                                    Edit
                                </el-button>
                                <el-button
                                    type="text"
                                    size="mini"
                                    @click.stop="() => removeRedisServer(node, data)">
                                    Delete
                                </el-button>
                            </span>
                        </template>
                    </span>
                </el-tree>
            </div>
        </div>
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

        <!-- edit redis server -->
        <el-dialog :visible.sync="showingEditDialog">
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
                    <el-input v-model="form.password" :type="showingPasswordPlainText ? 'password': 'text'" auto-complete="off">
                        <el-button slot="append" icon="el-icon-view" @click="showingPasswordPlainText = !showingPasswordPlainText"></el-button>
                    </el-input>
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

    data() {
        return {
            activeTab: {
                tabName: null,
                serverId: null,
                dbNum: null,
            },

            loadingDatabaseList: false,
            showingPasswordPlainText: false,
            showingEditDialog: false,

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
        this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_SERVER_LIST)
    },

    methods: {

        loadDatabaseList(node, resolve) {
            this.loadingDatabaseList = true
            if (node.level === 0) {
                setTimeout(() => {
                    this.loadingDatabaseList = false
                }, 700)
                return resolve([])
            }

            if (node.data.children.length != 0) {
            }

            this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_DATABASE_LIST, node.data.value).then(data => {
                resolve(data)
            }).catch(error => resolve([])
            ).finally(() => {
                setTimeout(() => {
                    this.loadingDatabaseList = false                  
                }, 700)
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

        freshDatabaseList() {
            this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_SERVER_LIST)
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

        rightClickTreeNode(event, node) {
        },

        clickTreeNode(data, node) {

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

        editRedisServer(node, data) {
            if (this.$refs.form != undefined) {
                this.$refs.form.resetFields()
            }
            this.form.id = data.value
            this.form.connectionName = data.label
            this.form.host = data.host
            this.form.port = data.port
            this.form.password = data.password

            this.showingEditDialog = true
        },

        addRedisServer() {
            if (this.$refs.form != undefined) {
                this.$refs.form.resetFields()
            }
            this.showingEditDialog = true
        },

        closeEditDialog() {
            this.showingEditDialog = false
        },

        removeRedisServer(node, data) {
            this.$confirm('Do you want to delete this redis server connection?', 'Warning', {
                type: 'warning'
            })
        }
    }
}
</script>

<style lang="stylus" scoped>

.container {
    display: flex;
    display: -webkit-flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-start;

    .grid-content {
        &:nth-child(1) {
            flex-shrink: 0;
            flex-grow: 0;
            width: 300px;
            padding-right: 20px;

            .server-btns {
                margin-bottom: 15px;
            }

            .server-list {
            }
        }
        &:nth-child(2) {
            flex-basis: auto;
            flex-shrink: 1;
            flex-grow: 1;
        }
    }
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

