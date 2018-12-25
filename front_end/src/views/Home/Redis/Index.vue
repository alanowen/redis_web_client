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
                    <el-tabs v-model="currentDatabase" type="card" v-show="redisDatabaseTabs.length != 0">
                        <el-tab-pane 
                            :label="item.tabLabel" 
                            :name="item.tabName" 
                            v-for="item in redisDatabaseTabs">
                            <key-list></key-list>
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
        ...mapState(['redisServerList', 'redisDatabaseTabs'])
    },

    data() {
        return {
            currentDatabase: null,

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
        this.$store.dispatch(ActionTypes.REDIS_GET_SERVERS)
    },

    methods: {

        loadDatabases(node, resolve) {
            if (node.level === 0) {
                return resolve([])
            }

            this.$store.dispatch(ActionTypes.REDIS_GET_DATABASES, node.data.value).then(data => {
                resolve(data)
            })
            
        },

        saveRedisServer() {
            this.$store.dispatch(ActionTypes.REDIS_ADD_SERVER, {...this.form})
        },

        freshDatabases() {
            this.$store.dispatch(ActionTypes.REDIS_GET_SERVERS)
        },

        clickDatabase(data, node) {
            if (node.level == 1) {

            }

            if (node.level == 2) {
                let tabName = `${node.parent.data.value}-${data.value}`
                let tab = this.redisDatabaseTabs.find(i => i.tabName === tabName)
                if (tab == null) {
                    let tab = {
                        tabName: `${node.parent.data.value}-${data.value}`,
                        tabLabel: `${node.parent.data.label} - ${data.label}`,
                    }
                    this.$store.dispatch(ActionTypes.COMMON_ADD_TAB, tab)
                }
                this.currentDatabase = tabName
            }
        }
    }
}
</script>

<style>
.grid-content {

}
</style>
