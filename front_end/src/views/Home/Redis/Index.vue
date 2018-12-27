<template>
    <div>
        <el-row>
            <el-col :span="6">
                <div class="grid-content">
                    <el-button @click="dialogVisible = true">Add Server</el-button>
                    <el-button @click="freshDatabases">Refresh</el-button>
                    <el-tree 
                        :data="redisServerList" 
                        lazy 
                        :load="loadDatabases"
                        :props="dataBaseTreeProps"
                        @node-click="clickDatabase">
                    </el-tree>
                 </div>
            </el-col>
            <el-col :span="18">
                <div class="grid-content">
                    <el-tabs :value="activeTab.tabName" type="card" v-show="redisServerDbTabs.length != 0" @tab-remove="removeTab">
                        <el-tab-pane
                            :key="item.tabName"
                            closable 
                            :label="item.tabLabel" 
                            :name="item.tabName" 
                            v-for="(item, index) in redisServerDbTabs">
                            <key-list :server-id="activeTab.serverId" :db-num="activeTab.dbNum"></key-list>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </el-col>
        </el-row>

        <el-dialog :visible.sync="dialogVisible">
            <el-form :model="form">
                <el-form-item label="Connection Name" :label-width="labelWidth">
                    <el-input v-model="form.connectionName" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Host" :label-width="labelWidth">
                    <el-input v-model="form.host" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="Port" :label-width="labelWidth">
                    <el-input v-model="form.port" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="Password" :label-width="labelWidth">
                    <el-input v-model="form.password" auto-complete="off"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">Cancel</el-button>
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
        ...mapState(['redisServerList', 'redisServerDbTabs'])
    },

    data() {
        return {
            activeTab: {
                tabName: null,
                serverId: null,
                dbNum: null,
            },

            dialogVisible: false,

            labelWidth: '',

            form: {
                connectionName: null,
                host: '127.0.0.1',
                port: 6379,
                password: null
            },

            dataBaseTreeProps: {
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
            this.$store.dispatch(ActionTypes.REDIS_SERVER_ADD_SERVER, {...this.form})
        },

        freshDatabases() {
            this.$store.dispatch(ActionTypes.REDIS_SERVER_GET_SERVERS)
        },

        removeTab(targetName) {
            let activeName = this.activeTab.tabName
            let tabs = this.redisServerDbTabs
            if (activeName === targetName) {
                this.redisServerDbTabs.forEach((tab, index) => {
                    if (tab.tabName === targetName) {
                        let nextTab = tabs[index + 1] || tabs[index - 1]
                        if (nextTab) {
                            activeName = nextTab.tabName
                        }
                    }
                })
            }
            this.activeTab.tabName = activeName
            this.$store.state.redisServerDbTabs = tabs.filter(tab => tab.tabName !== targetName)
        },

        clickDatabase(data, node) {

            if (node.level == 1) {

            }

            if (node.level == 2) {
                let tabName = `${node.parent.data.value}-${data.value}`
                let tab = this.redisServerDbTabs.find(i => i.tabName === tabName)
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
        }
    }
}
</script>

<style>
.grid-content {

}
</style>
