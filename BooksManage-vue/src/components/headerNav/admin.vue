<template>
  <div class="header">
    <div class="main">
      <div class="text">
        <h2>欢迎使用图书管理系统</h2>
      </div>
      <div class="information">
        <el-text class="student" size="large">{{ admin_name }}，已登录</el-text>
        <div class="button">
          <el-button type="primary" @click="logout">退出登录</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import request from "../../utils/request";
import { ElMessage } from "element-plus";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const admin_id = ref(route.params.id);
const admin_name = ref(admin_id.value === "1" ? "hzy" : "gyx");

// 退出登录
function logout() {
  localStorage.setItem("token", "");
  router.push("/");
}
</script>

<style lang="less" scoped>
.header {
  background: #409eff;
  .main {
    .buttonGroup {
      margin-left: 19%;
    }
    margin-left: 15%;
    width: 70%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    .text {
      color: #f4f4f4;
    }
    .visibleForm {
      max-width: 65%;
      margin-top: 5%;
      margin-left: 15%;
      .verifyGet {
        :deep(.el-form-item__content) {
          display: flex;
          flex-wrap: nowrap;
          .el-button {
            margin-left: 5%;
          }
        }
      }
      :deep(.button) {
        .el-form-item__content {
          margin-left: 15%;
          display: flex;
          justify-content: space-around;
        }
      }
    }
    .information {
      width: 20%;
      display: flex;
      .student {
        color: #f4f4f4;
        margin-right: 5%;
      }
    }
  }
}
</style>
