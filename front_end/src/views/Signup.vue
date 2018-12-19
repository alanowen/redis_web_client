<template>
    <el-form ref="form" :model="form" :rules="rules" :style="{'width': '500px', 'margin': '200px auto 0'}">
        <el-form-item label="Email" prop="email">
            <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
            <el-input type="password" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="Confirm Password" prop="confirmPassword">
            <el-input type="password" v-model="form.confirmPassword"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm">Submit</el-button>
            <el-button type="text" @click="() => this.$router.push({'name': 'login'})">Login</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
import * as ActionTypes from '@@ActionTypes'

export default {
    data() {

        const confirmPasswordEqual = (rule, value, callback) => {
            if (value && value !== this.form.password) {
                callback(new Error('The two passwords don`t match.'))
            } else {
                callback()
            }
        };

        return {
            form: {
                name: null,
                email: null,
                password: null,
                confirmPassword: null
            },

            rules: {
                email: [
                    { required: true, message: 'Please input the email.',  trigger: 'blur' },
                    { type: 'email', message: 'Please input correct email address.', trigger: ['blur', 'change'] }
                ],
                password: [
                    { required: true, message: 'Please input the password.', trigger: 'blur' }
                ],
                confirmPassword: [
                    { required: true, message: 'Please input the confirm passsword.', trigger: 'blur' },
                    { validator: confirmPasswordEqual, trigger: 'blur' }
                ]
            }
        }
    },

    methods: {
        submitForm() {
            this.$refs.form.validate(valid => {
                if (valid) {
                    this.$store.dispatch(ActionTypes.SIGNUP, {...this.form}).then(data => {
                        for (let i in data['formError']) {
                            let field = this.$refs.form.fields.find(j => j.prop === i)
                            if (field) {
                                field.validateState = 'error'
                                field.validateMessage = data['formError'][i][0]
                            }
                        }
                    }).catch(error => {

                    })
                }
                return false
            })
        }
    }
}
</script>