import Vue from 'vue'
import Vuex from 'vuex'

import util from '@libs/util'
import * as ActionTypes from './action-types'
import * as MutationTypes from './mutation-types'


Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: null,

        redisServerList: [],

        redisServerTabs: [],

        redisDatabaseList: [],
    },

    mutations: {

        [MutationTypes.REDIS_SERVER_GET_SERVER_LIST](state, data) {
            state.redisServerList = data
        }
    },

    actions: {

        [ActionTypes.RELOGIN]({ state }) {
            const token = window.localStorage.getItem('token')
            if (token) {
                state.token = token
            }
        },

        [ActionTypes.LOGOUT]({ state }) {
            state.token = null
            state.redisServerTabs = []
            window.localStorage.clear()
        },

        async [ActionTypes.LOGIN]({ state }, params) {
            let data = await util.ajax.post('/auth/login', params)
            if (data) {
                state.token = data
                window.localStorage.setItem('token', data)
                return true
            } else {
                return false
            }
        },

        async [ActionTypes.SIGNUP](context, params) {
            let data = await util.ajax.post('/user/signup', params)
            return data
        },

        [ActionTypes.COMMON_ADD_TAB]({ state }, tab) {
            state.redisServerTabs.push(tab)    
        },

        [ActionTypes.COMMON_REMOVE_TAB]({ state }, name) {
            let index = state.redisServerTabs.findIndex(i => i.tabName == name)
            if (index > -1) {
                state.redisServerTabs.splice(index, 1)
            }
        },

        [ActionTypes.REDIS_SERVER_AUTHENTICATE](context, data) {
            let promise = new Promise((resolve, reject) => {
                util.ajax.post('/redis_server/auth', data).then(({ data }) => {
                    resolve(data)
                }).catch(error => reject(error))
            })
            return promise
        },

        async [ActionTypes.REDIS_SERVER_GET_SERVER_LIST]({ state }, params) {
            let data = await util.ajax.post('/redis_server/list', params)
            state.redisServerList = data
            return data
        },

        async [ActionTypes.REDIS_SERVER_ADD_SERVER](context, params) {
            const data = await util.ajax.post('/redis_server/save', params)
            return data
        },

        async [ActionTypes.REDIS_SERVER_GET_DATABASE_LIST]({ state }, connectionId) {
            let data = await util.ajax.get(`/redis_server/${connectionId}/database_list`)
            const node = state.redisServerList.find(i => i.value == connectionId)
            node['children'] = data
            return data
        },

        async [ActionTypes.REDIS_DATABASE_GET_KEY_LIST](context, { serverId, dbNum, page }) {
            let data = await util.ajax.get(`/redis_db/${serverId}/${dbNum}/key_list/${page}`)
            return data
        },

        async [ActionTypes.REDIS_DATABASE_SET_KEY_VALUE](context, { serverId, dbNum, params }) {
            let data = await util.ajax.post(`/redis_db/${serverId}/${dbNum}/save_key_value`, params)
            return data
        }
    },

    getters: {

    }
})