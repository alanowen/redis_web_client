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

util.setFormErrors = async function(data, form) {
    if (data && 'formErrors' in data) {
        for (let i in data['formErrors']) {
            let field = form.fields.find(j => j.prop === i)
            if (field) {
                field.validateState = 'error'
                field.validateMessage = data['formErrors'][i][0]
            }
        }
        return false
    }
    return true
}

util.validateForm = async function(form) {
    let promise = new Promise((resolve, reject) => {
        form.validate(isValidate => {
            resolve(isValidate)
        })
    })
    return promise
}

export default util