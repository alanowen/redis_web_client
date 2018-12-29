import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import App from './App.vue'
import util from './libs/util'
import store from './store'
import router from './router'
import * as ActionTypes from './store/action-types'


store.dispatch(ActionTypes.RELOGIN)

Vue.use(ElementUI, { size: 'small' });

const vm = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
})

util.ajax.interceptors.request.use(
    function (config) {
        if (store.state.token) {
            config.headers.AUTHORIZATION = `Bearer ${store.state.token}`;
        }
        return config;
    },
    
    function (error) {
        return Promise.reject(error)
    }
)

util.ajax.interceptors.response.use(
    function (response) {
        const data = response.data
        return data
    },

    function (error) {
        if  (error && error.response) {
            switch(error.response.status) {
                case 400:
                    // bad request
                    break
                case 401:
                    // not authorized
                    store.dispatch(ActionTypes.LOGOUT)
                    router.replace({
                        name: 'login',
                    })
                    break
                case 403:
                    // access denied
                    break
                case 404:
                    // not found
                    break
                case 408:
                    // request timeout
                    break
                case 500:
                    // server internal error
                    vm.$message({
                        message: 'Error occurred, please try again later.',
                        type: 'error'
                    })
                    break
                case 501:
                    // not implemented
                    break
                case 502:
                    // bad gateway
                    break
                case 503:
                    // service unavaliable
                    break
                case 504:
                    // gateway timeout
                    break
                case 505:
                    // not supported http version 
                    break
            }
        }
        return Promise.reject(error)
    }
)