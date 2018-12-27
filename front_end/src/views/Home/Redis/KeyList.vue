<template>
    <div>
    <el-button @click="loadRedisDBKeys">Refresh</el-button>
    <el-table 
        :data="data"
        border
        stripe>
        <el-table-column
            prop=""
            width="100"
            label="#">
        </el-table-column>
        <el-table-column
            prop="index"
            width="100"
            align="center"
            label="Index">
        </el-table-column>
        <el-table-column
            prop="key"
            width=""
            label="Key">
        </el-table-column>
        <el-table-column
            prop="type"
            width="100"
            label="Type"
            :filters="typeFilters"
            :filter-method="filterRedisDataType"
            filter-placement="bottom-end">
            <template slot-scope="scope">
                <el-tag :type="'primary'">{{ scope.row.type }}</el-tag>
            </template>
        </el-table-column>
    </el-table>
    </div>

    <!-- <el-pagination
  small
  layout="prev, pager, next"
  :total="50">
</el-pagination> -->
</template>

<script>
import * as ActionTypes from '~/store/action-types'

export default {

    props: {
        'server-id': null,
        'db-num': null
    },

    data() {
        return {
            data: [],

            _serverId: null,
            _dbNum: null,

            typeFilters: [
                { text: 'STRING', value: 'STRING' }, 
                { text: 'LIST', value: 'LIST' }, 
                { text: 'HASH', value: 'HASH' },
                { text: 'SET', value: 'SET' },
                { text: 'ZSET', value: 'ZSET' }
            ]
        }
    },

    mounted() {

        this._serverId = this.serverId
        this._dbNum = this.dbNum

        this.loadRedisDBKeys()
    },
    
    methods: {
        filterRedisDataType(value, row) {
            return value === row.type
        },

        loadRedisDBKeys() {
            this.$store.dispatch(ActionTypes.REDIS_DB_GET_KEYS, 
            { 
                serverId: this._serverId, 
                dbNum: this._dbNum 
            }).then(data => {
                this.data = data
            })
        }
    }
}
</script>
