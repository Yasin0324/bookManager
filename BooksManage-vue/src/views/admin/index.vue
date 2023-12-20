<template>
  <el-container>
    <el-header class="test">
      <header-nav></header-nav>
    </el-header>
    <div class="main">
      <el-aside class="test">
        <aside-nav></aside-nav>
      </el-aside>
      <el-main class="test">
        <router-view></router-view>
      </el-main>
    </div>
  </el-container>
</template>

<script setup>
import headerNav from "../../components/headerNav/admin.vue";
import asideNav from "../../components/asideNav/admin.vue";
import manageBook from "./manageBook.vue";
import readInformation from "./readInformation.vue";
import manageStudent from "./manageStudent.vue";
import request from "../../utils/request";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
onMounted(() => {
  const admin_id = ref(route.params.id);
  router.push(`/admin/${admin_id.value}/manageBook`);
});
</script>

<style lang="less" scoped>
:deep(.el-header) {
  padding: 0;
}
.el-aside {
  width: 8%;
}
:deep(.el-main) {
  width: 20%;
}
.main {
  display: flex;
  justify-content: center;
}
</style>
