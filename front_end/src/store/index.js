import Vue from 'vue'
import Vuex from 'vuex'

import util from '@libs/util'
import * as ActionTypes from './action-types'
import * as MutationTypes from './mutation-types'


Vue.use(Vuex)

export default new Vuex.Store({
    state: {

    },

    mutations: {

    },

    actions: {
        [ActionTypes.LOGIN](context) {
            let promise = new Promise((resolve, reject) => {
                util.ajax.post('/auth/login', data).then(({ data }) => {
                    context.commit(MutationTypes.LOGIN, data)
                    resolve(data)
                }).catch(error => reject(error))
            })
        },

        [ActionTypes.SIGNUP]({ state }, data) {
            let promise = new Promise((resolve, reject) => {
                util.ajax.post('/user/signup', data).then(({ data }) => {
                    resolve(data)
                }).catch(error => reject(error))
            })

            return promise
        }
    },

    getters: {

    }
})