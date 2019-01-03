<template>
    <el-form ref="form" :model="form" :rules="rules" :style="{'width': '500px', 'margin': '200px auto 0'}">
        <el-form-item label="Email" prop="email">
            <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
            <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" :disabled="disableSubmitButton" @click="submitForm">Login</el-button>
            <div :style="{'display': 'inline'}">
                <span>Don`t have a account ?</span>
                <el-button type="text" @click="() => this.$router.push({ 'name': 'signup' })">Singup</el-button>
            </div>
        </el-form-item>
    </el-form>
</template>

<script>
import * as ActionTypes from '~/store/action-types'
import util from '~/libs/util'

export default {
    data() {

        return {
            disableSubmitButton: false,
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
        async submitForm() {
            try {
                this.disableSubmitButton = true
                const isValid = await util.validateForm(this.$refs.form)
                if (isValid) {
                    let flag = await this.$store.dispatch(ActionTypes.LOGIN, {...this.form})
                    if (flag) {
                        this.$message({
                            message: 'Congrats, you`ve logged in.',
                            type: 'success',
                            duration: 800,
                            onClose: () => {
                                if ('nextUrl' in this.$route.query) {
                                    this.$router.replace(this.$route.query['nextUrl'])
                                } else {
                                    this.$router.replace({ name: 'home' })
                                }
                            }
                        })
                    }
                }
            } catch (error) {
                throw error
            } finally {
                this.disableSubmitButton = false
            }
        }
    }
}
</script>
