<template>
  <el-menu router class="el-menu-vertical-demo" :default-active="$route.path">
    <el-menu-item v-for="item in menuData" :key="item.name" :index="item.path">
      <el-icon><component :is="item.icon"></component></el-icon>
      <template v-slot:title>
        <span class="right-align">{{ item.label }}</span>
      </template>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref } from "vue";

const menuData = ref([
  {
    path: "/",
    name: "searchBooks",
    label: "图书查询",
    icon: "Search",
  },
]);
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 1px solid #c6c6c;
  height: 100vh;
}
</style>
