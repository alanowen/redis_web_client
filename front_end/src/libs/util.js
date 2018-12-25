import axios from 'axios'
import env from '~/config/env'


let ajaxUrl = env === 'development' ? 'http://127.0.0.1:5000' : config.apiServer

let util = {}
util.ajaxUrl = ajaxUrl
util.ajax = axios.create({
    baseURL: ajaxUrl,   
    paramsSerializer: function (params) {
        return JSON.parse(JSON.stringify(params))
    },
    withCredentials: true
})

export default util