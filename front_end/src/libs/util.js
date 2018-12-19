import axios from 'axios'
import env from '~/config/env'


let ajaxUrl = env === 'development' ? 'http://127.0.0.1:5000' : config.apiServer


let util = {
    ajaxUrl,

    ajax: axios.create(
        {
            baseURL: ajaxUrl,
            paramsSerializer: function (params) {
                return JSON.parse(JSON.stringify(params))
            },
            //withCredentials: true
        }
    )
}

util.ajax.interceptors.request.use(
    function (config) {
        return config
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
        return Promise.reject(error)
    }
)

export default util