import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)


export default new VueRouter({
    mode: 'hash',
    routes: [
        {
            path: '/login',
            name: 'login',
            component: resolve => require(['~/views/Login'], resolve)
        },
        {
            path: '/signup',
            name: 'signup',
            component: resolve => require(['~/views/Signup'], resolve)
        },
        {
            path: '/page-not-found',
            name: '404',
            component: resolve => require(['~/views/404'], resolve)
        },
        {
            path: '/',
            name: 'home',
            component: resolve => require(['~/views/Home/Home'], resolve),
            children: [

            ]
        }
    ]
})