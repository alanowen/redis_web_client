<template>
    <div>
        <div class="op-btns">
            <el-button @click="() => {this.currentPage = 1; loadRedisDBKeys(1)}">Refresh</el-button>
            <el-button @click="openEditDialog">Add</el-button>
        </div>
        <div v-loading="loading">
            <el-table
                :data="data"
                border
                stripe>
                <el-table-column
                    type="selection"
                    width="55">
                </el-table-column>
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
                    <template slot-scope="scope">
                        <el-button class="key-link" type="text" v-if="scope.row.type !== 'STRING'">{{ scope.row.key }}</el-button>
                        <template v-else>{{ scope.row.key }}</template>
                    </template>
                </el-table-column>
                <el-table-column
                    prop="type"
                    width="100"
                    label="Type"
                    :filters="redisDataTypeDict"
                    :filter-method="filterRedisDataType"
                    filter-placement="bottom-end">
                    <template slot-scope="scope">
                        <el-tag :type="'primary'">{{ scope.row.type }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column
                    fixed="right"
                    label="Operation"
                    width="100">
                    <template slot-scope="scope">
                        <!-- <el-button @click="vieRedisKey(scope.row)" type="text" size="small">View</el-button> -->
                        <el-button type="text" size="small">Edit</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                :current-page.sync="currentPage"
                :page-size="20"
                small
                layout="prev, pager, next"
                @current-change="changePage"
                :total="total">
            </el-pagination>
        </div>
        
        <!-- EditKeyDialog -->
        <el-dialog :visible.sync="showEditDialog" :width="editDialogWidth">
            <el-form :model="form" ref="form" :label-position="'left'">
                <el-form-item label="Key"
                    :label-width="formLabelWidth" 
                    :rules="[
                        { required: true, message: 'Key is required.'}
                    ]"
                    prop="key">
                    <el-input v-model="form.key" auto-complete="off" :style="{ 'width': formInputWidth }"></el-input>
                </el-form-item>
                <el-form-item 
                    label="Data Type" 
                    :label-width="formLabelWidth" 
                    prop="dataType">
                    <el-select v-model="form.dataType" @change="selectChange">
                        <el-option 
                            v-for="item in redisDataType"
                            :key="item"
                            :label="item"
                            :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>

                <!-- STRING -->
                <template v-if="form.dataType == 'STRING'">
                    <el-form-item 
                        label="String Value" 
                        :label-width="formLabelWidth" 
                        :rules="[
                            { required: true, message: 'String value is required.' }
                        ]"
                        prop="stringValue">
                        <el-input v-model="form.stringValue" auto-complete="off" :style="{ 'width': formInputWidth }"></el-input>
                    </el-form-item>
                </template>

                <!-- LIST -->
                <template v-else-if="form.dataType == 'LIST'">
                    <el-form-item 
                        v-for="(item, index) in form.listValues"
                        :key="`List Value${index+1}`"
                        :label="`List Value${index+1}`"
                        :label-width="formLabelWidth"
                        :rules="[
                            { required: true, message: `List value${index+1} is required.` }
                        ]"
                        :prop="`listValues.${index}.value`">
                        <el-input v-model="item.value" auto-complete="off" :style="{ 'width': formInputWidth }"></el-input>
                        <el-button @click="removeFormItem(item, form.listValues)" v-if="index !== 0">Delete</el-button>
                    </el-form-item>
                    <el-button @click="form.listValues.push({ value: null })">Add</el-button>
                </template>

                <!-- SET -->
                <template v-else-if="form.dataType == 'SET'">
                    <el-form-item 
                        v-for="(item, index) in form.setValues"
                        :key="`Set Value${index+1}`"
                        :label="`Set Value${index+1}`"
                        :label-width="formLabelWidth"
                        :rules="[
                            { required: true, message: `Set value${index+1} is required.` }
                        ]"
                        :prop="`setValues.${index}.value`">
                        <el-input v-model="item.value" auto-complete="off" :style="{ 'width': formInputWidth }"></el-input>
                        <el-button @click="removeFormItem(item, form.setValues)" v-if="index !== 0">Delete</el-button>
                    </el-form-item>
                    <el-button @click="form.setValues.push({ value: null })">Add</el-button>
                </template>

                <!-- ZSET -->
                <template v-else-if="form.dataType == 'ZSET'">
                    <el-form-item
                        label="ZSet Value"
                        :label-width="formLabelWidth"
                        :rules="[
                            { required: true, message: 'ZSet value is required.' }
                        ]"
                        prop="zsetValue">
                        <el-input v-model="form.zsetValue" auto-complete="off" :style="{ 'width': formInputWidth }"></el-input>
                    </el-form-item>
                </template>

                <!-- HASH -->
                <template v-else>
                    <el-form-item 
                        v-for="(item, index) in form.hashValues"
                        :key="`Hash Field${index+1}`">
                        <!-- Field -->
                        <el-form-item 
                            :label="`Hash Field${index+1}`"
                            :label-width="formLabelWidth"
                            :rules="[
                                { required: true, message: `Hash field${index+1} is required.` }
                            ]"
                            :prop="`hashValues.${index}.value`">
                            <el-input v-model="item.field" auto-complete="off" :style="{ 'width': formHashInputWidth }"></el-input>
                        </el-form-item>
                        <!-- Value -->
                        <el-form-item 
                            :label="`Hash Value${index+1}`"
                            :label-width="formLabelWidth"
                            :rules="[
                                { required: true, message: `Hash value${index+1} is required.` }
                            ]"
                            :prop="`hashValues.${index}.value`">
                            <el-input v-model="item.value" auto-complete="off" :style="{ 'width': formHashInputWidth }"></el-input>
                            <el-button @click="removeFormItem(item, form.hashValues)" v-if="index !== 0">Delete</el-button>
                        </el-form-item>
                    </el-form-item>
                    <el-button @click="form.hashValues.push({ field: null, value: null })">Add</el-button>
                </template>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="closeEditDialog">Cancel</el-button>
                <el-button type="primary" @click="addRedisKeyValue" :disabled="disableSubmitButton">Confirm</el-button>
            </span>
        </el-dialog>
    </div>


</template>

<script>
import * as ActionTypes from '~/store/action-types'
import util from '~/libs/util'

export default {

    props: {
        'server-id': null,
        'db-num': null
    },

    data() {
        return {
            total: 0,
            data: [],

            loading: false,

            currentPage: 1,

            showEditDialog: false,
            disableSubmitButton: false,

            editDialogWidth: '50%',
            formLabelWidth: '110px',
            formInputWidth: '70%',
            formHashInputWidth: '70%',

            form: {
                key: null,
                dataType: 'STRING',
                stringValue: null,
                listValues: [
                    {
                        value: null
                    }
                ],
                setValues: [
                    {
                        value: null
                    }
                ],
                zsetValue: null,
                hashValues: [
                    {
                        field: null,
                        value: null
                    }
                ]
            },

            _serverId: null,
            _dbNum: null,

            redisDataType: ['STRING', 'LIST', 'SET', 'ZSET', 'HASH']
        }
    },

    computed: {
        redisDataTypeDict() {
            return this.redisDataType.map(i => {
                return { 'text': i, 'value': i }
            })
        }
    },

    watch: {
        showEditDialog(n, o) {
            if (n && this.$refs.form) {
                this.$nextTick(() => {
                    this.$refs.form.resetFields()
                })
            }
        }
    },

    mounted() {

        this._serverId = this.serverId
        this._dbNum = this.dbNum

        this.loadRedisDBKeys(1)
    },
    
    methods: {
        filterRedisDataType(value, row) {
            return value === row.type
        },

        loadRedisDBKeys(page) {
            this.loading = true
            this.$store.dispatch(ActionTypes.REDIS_DATABASE_GET_KEY_LIST, 
            { 
                serverId: this._serverId,
                page: page,
                dbNum: this._dbNum 
            }).then(data => {
                this.data = data.rows
                this.total = data.total
            }).finally(() => {
                setTimeout(() => {
                    this.loading = false                    
                }, 700);
            })
        },

        openEditDialog() {
            this.showEditDialog = true
        },

        closeEditDialog() {
            this.showEditDialog = false
        },

        async addRedisKeyValue() {
            this.disableSubmitButton = true
            const isValid = await util.validateForm(this.$refs.form)
            
            try {
                if (isValid) {
                    const data = await this.$store.dispatch(ActionTypes.REDIS_DATABASE_SET_KEY_VALUE, {
                        serverId: this._serverId, 
                        dbNum: this._dbNum, 
                        params: {...this.form}
                    })

                    const flag = await util.setFormErrors(data, this.$refs.form)
                    if (flag) {
                        this.showEditDialog = false
                        this.loadRedisDBKeys(this.currentPage)
                    }
                }
                return isValid
            } catch(error) {

            } finally {
                this.disableSubmitButton = false
            }
        },

        selectChange(value) {
            if (this.$refs.form != undefined) {
                this.$refs.form.resetFields()
            }
            this.form.dataType = value
        },

        removeFormItem(item, itemList) {
            const index = itemList.indexOf(item)
            if (index !== -1) {
                itemList.splice(index, 1)
            }
            if (this.form.dataType == 'HASH') {
                item.field = null
            } else {
                item.value = null
            }
        },

        changePage(page) {
            this.loadRedisDBKeys(this.currentPage)
        },

        vieRedisKey() {

        }
    }
}
</script>

<style lang="stylus">
.key-link{
    span {
        color: #606266;
        text-decoration: none; border-bottom:1px dotted 
    }
}

.op-btns {
    margin-bottom: 15px;
}
</style>

