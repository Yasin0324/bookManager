<template>
  <div class="header">
    <div class="main">
      <div class="text">
        <h2>欢迎使用图书管理系统</h2>
      </div>
      <div class="information">
        <el-text class="student" size="large"
          >{{ student_name }}，已登录</el-text
        >
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
const student_id = ref(route.params.id);
const student_name = ref("");

// 获取学生信息
function getStudent() {
  request({
    url: "/getStudent/",
    method: "get",
    params: { student_id: student_id.value },
  })
    .then((res) => {
      console.log(student_id.value);
      console.log(res.data.result.student_name);
      student_name.value = res.data.result.student_name;
    })
    .catch((error) => {
      console.log(error);
    });
}

// 退出登录
function logout() {
  localStorage.setItem("token", "");
  router.push("/");
}

onMounted(() => {
  getStudent();
});
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
