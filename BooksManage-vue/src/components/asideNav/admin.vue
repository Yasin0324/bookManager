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
import { useRoute } from "vue-router";

const route = useRoute();
const admin_id = ref(route.params.id);
const menuData = ref([
  {
    path: `/admin/${admin_id.value}/manageBook`,
    name: "manageBooks",
    label: "图书管理",
    icon: "Edit",
  },
  {
    path: `/admin/${admin_id.value}/manageStudent`,
    name: "manageStudents",
    label: "学生管理",
    icon: "User",
  },
  {
    path: `/admin/${admin_id.value}/readInformation`,
    name: "readInformation",
    label: "借阅信息",
    icon: "Notebook",
  },
]);
</script>

<style lang="less" scoped>
.el-menu {
  border-right: 1px solid #c6c6c;
  height: 100vh;
}
</style>
