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
    },

    mutations: {

        [MutationTypes.REDIS_SERVER_GET_SERVERS](state, data) {
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

        async [ActionTypes.LOGIN]({ state }, form) {
            let data = await util.ajax.post('/auth/login', form)
            state.token = data['token']
            window.localStorage.setItem('token', state.token)
            return state.token 
        },

        async [ActionTypes.SIGNUP](context, form) {
            let data = await util.ajax.post('/user/signup', form)
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

        async [ActionTypes.REDIS_SERVER_GET_SERVERS]({ state }, params) {
            let data = await util.ajax.post('/redis_server/list', params)
            state.redisServerList = data
            return data
        },

        [ActionTypes.REDIS_SERVER_ADD_SERVER](context, data) {
            let promsie = new Promise((resolve, reject) => {
                util.ajax.post('/redis_server/add', data).then(({ data }) => {
                    resolve(data)
                }).catch(error => reject(error))
            })
            return promsie
        },

        async [ActionTypes.REDIS_SERVER_GET_DATABASES]({ state }, connectionId) {
            let data = await util.ajax.get(`/redis_server/${connectionId}/databases`)
            const node = state.redisServerList.find(i => i.value == connectionId)
            node['children'] = data
            return data
        },

        async [ActionTypes.REDIS_DB_GET_KEYS](context, { serverId, dbNum }) {
            let data = await util.ajax.get(`/redis_db/${serverId}/${dbNum}/key_list`)
            return data
        },

        async [ActionTypes.REDIS_DB_SET_KEY_VALUE](context, { serverId, dbNum, params }) {
            let data = await util.ajax.post(`/redis_db/${serverId}/${dbNum}/save_key_value`, params)
        }
    },

    getters: {

    }
})