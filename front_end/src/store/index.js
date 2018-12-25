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

        redisDatabaseTabs: []
    },

    mutations: {

        [MutationTypes.REDIS_GET_SERVERS](state, data) {
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
            window.localStorage.clear()
        },

        async [ActionTypes.LOGIN]({ state }, params) {
            let { data } = await util.ajax.post('/auth/login', params)
            let { token } = data
            if (token != undefined) {
                state.token = token
                window.localStorage.setItem('token', state.token)
                return token        
            }
        },

        async [ActionTypes.SIGNUP](context, params) {
            let { data } = await util.ajax.post('/user/signup', params)
            return data
        },

        [ActionTypes.COMMON_ADD_TAB]({ state }, params) {
            state.redisDatabaseTabs.push(params)    
        },

        [ActionTypes.REDIS_AUTHENTICATE_SERVER](context, data) {
            let promise = new Promise((resolve, reject) => {
                util.ajax.post('/redis_server/auth', data).then(({ data }) => {
                    resolve(data)
                }).catch(error => reject(error))
            })
            return promise
        },

        async [ActionTypes.REDIS_GET_SERVERS]({ state }, params) {
            let { data } = await util.ajax.post('/redis_server/list', params)
            state.redisServerList = data
            return data
        },

        [ActionTypes.REDIS_ADD_SERVER](context, data) {
            let promsie = new Promise((resolve, reject) => {
                util.ajax.post('/redis_server/add', data).then(({ data }) => {
                    resolve(data)
                }).catch(error => reject(error))
            })
            return promsie
        },

        async [ActionTypes.REDIS_GET_DATABASES]({ state }, connectionId) {
            let { data } = await util.ajax.get(`/redis_server/${connectionId}/databases`)
            const node = state.redisServerList.find(i => i.value == connectionId)
            node['children'] = data
            return data
        }
    },

    getters: {

    }
})