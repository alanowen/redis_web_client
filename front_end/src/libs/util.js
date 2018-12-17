import axios from 'axios'
import env from '../config/env'

let util = {

}


const ajaxUrl = env === 'development' ? 'http://127.0.0.1:5000' : config.apiServer


let ajax = axios.create({
    baseURL: ajaxUrl,
    paramsSerializer: function (params) {
        return JSON.parse(JSON.stringify(params))
    },
    onDownloadProgress: function (progressEvent) {
        //let percentCompleted = Math.floor((progressEvent.loaded * 100) / progressEvent.total)
    }
})

util.ajax = ajax
util.ajaxUrl = ajaxUrl

export default util