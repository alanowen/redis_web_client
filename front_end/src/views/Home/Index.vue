<template>
    <el-container style="height: 100%">
        <el-header :style="{'padding': '0px'}">
            <el-menu
                :default-active="activeIndex2"
                class="el-menu-demo"
                mode="horizontal"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b">
                <el-menu-item index="1">Processing Center</el-menu-item>
                <el-submenu index="2">
                    <template slot="title">Workspace</template>
                    <el-menu-item index="2-1">item one</el-menu-item>
                    <el-menu-item index="2-2">item two</el-menu-item>
                    <el-menu-item index="2-3">item three</el-menu-item>
                    <el-submenu index="2-4">
                    <template slot="title">item four</template>
                    <el-menu-item index="2-4-1">item one</el-menu-item>
                    <el-menu-item index="2-4-2">item two</el-menu-item>
                    <el-menu-item index="2-4-3">item three</el-menu-item>
                    </el-submenu>
                </el-submenu>
                <el-menu-item index="3" disabled>Info</el-menu-item>
                <el-menu-item index="4" @click="logout">Logout</el-menu-item>
            </el-menu>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <el-menu :router="true">
                    <el-menu-item index="redis">
                        <i class="el-icon-menu"></i>
                        <span>redis</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import * as ActionTypes from '~/store/action-types'

export default {
    data() {
        return {
            activeIndex2: ''
        }
    },

    methods: {
        logout() {
            this.$store.dispatch(ActionTypes.LOGOUT).then(() => {
                this.$router.replace({ name: 'login' })
            })
        }
    }
}
</script>

<style lang="stylus" scoped>
.el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
}
</style>

