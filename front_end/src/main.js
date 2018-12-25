import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import App from './App.vue'
import util from './libs/util'
import store from './store'
import router from './router'
import * as ActionTypes from './store/action-types'


store.dispatch(ActionTypes.RELOGIN)

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
        return response
    },

    function (error) {
        if (error.response.status === 401) {
            store.dispatch(ActionTypes.LOGOUT)
            router.replace({
                name: 'login',
            })
        }
        return Promise.reject(error)
    }
)

Vue.use(ElementUI, { size: 'small' });

const vm = new Vue({
    el: '#app',
    store,
    router,
    render: h => h(App)
})