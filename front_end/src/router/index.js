import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let router = new VueRouter({
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
            component: resolve => require(['~/views/Home/Index'], resolve),
            meta: {
                requireAuth: true
            },
            children: [
                {
                    path: '/redis',
                    name: 'redis',
                    component: resolve => require(['~/views/Home/Redis/Index'], resolve),
                    children: [
                        {
                            path: '/string-list',
                            name: 'stringList',
                            component: resolve => require(['~/views/Home/Redis/StringList'], resolve)   
                        },
                        {
                            path: '/set-list',
                            name: 'setList',
                            component: resolve => require(['~/views/Home/Redis/SetList'], resolve)   
                        },
                        {
                            path: '/hash-list',
                            name: 'hashList',
                            component: resolve => require(['~/views/Home/Redis/HashList'], resolve)   
                        },
                        {
                            path: '/zset-list',
                            name: 'zsetList',
                            component: resolve => require(['~/views/Home/Redis/ZSetList'], resolve)   
                        }
                    ]
                }
            ]
        }
    ]
})


router.beforeEach((to, from, next) => {
    if (to.matched.some(i => i.meta.requireAuth)) {
        if (!window.localStorage.getItem('token')) {
            next({
                name: 'login',
                query: { nextUrl: to.fullPath }
            })
        } else {
            next()
        }
    } else {
        next()
    }
})


export default router