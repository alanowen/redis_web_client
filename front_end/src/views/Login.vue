<template>
    <el-form ref="form" :model="form" :rules="rules" :style="{'width': '500px', 'margin': '200px auto 0'}">
        <el-form-item label="Email" prop="email">
            <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
            <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm">Login</el-button>
            <div :style="{'display': 'inline'}">
                <span>Don`t have a account ?</span>
                <el-button type="text" @click="() => this.$router.push({ 'name': 'signup' })">Singup</el-button>
            </div>
        </el-form-item>
    </el-form>
</template>

<script>
import * as ActionTypes from '@@ActionTypes'

export default {
    data() {

        return {
            form: {
                email: null,
                password: null
            },

            rules: {
                email: [
                    { required: true, message: 'Please input the email.', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: 'Please input the password.', trigger: 'blur' }
                ]
            }
        }
    },

    methods: {
        submitForm() {
            this.$refs.form.validate(valid => {
                if (valid) {
                    this.$store.dispatch(ActionTypes.LOGIN, {...this.form}).then(data => {

                    }).catch(error => {
                        
                    })
                }
                return false
            })
        }
    }
}
</script>
