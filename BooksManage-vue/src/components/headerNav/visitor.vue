<template>
  <div class="header">
    <div class="main">
      <div class="text">
        <h2>欢迎使用图书管理系统</h2>
      </div>
      <el-button type="primary" @click="loginVisible = true">登录</el-button>

      <el-dialog
        v-model="loginVisible"
        width="30%"
        align-center
        draggable="true"
      >
        <el-radio-group class="buttonGroup" v-model="selectedOption">
          <el-radio-button label="studentLogin" @click="user_type = 1"
            >学生登录</el-radio-button
          >
          <el-radio-button label="studentSignup" @click="user_type = 2"
            >学生注册</el-radio-button
          >
          <el-radio-button label="adminLogin" @click="user_type = 0"
            >管理员登录</el-radio-button
          >
        </el-radio-group>
        <el-form
          class="visibleForm"
          label-width="20%"
          :model="studentLog"
          label-position="right"
          v-if="user_type === 1"
        >
          <el-form-item label="邮箱">
            <el-input
              v-model="studentLog.student_email"
              placeholder="请输入邮箱"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="studentLog.student_password"
              type="password"
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item class="button">
            <el-button type="primary" @click="login">登录</el-button>
            <el-button type="info" @click="close">取消</el-button>
          </el-form-item>
        </el-form>
        <el-form
          class="visibleForm"
          label-width="20%"
          :model="studentSign"
          label-position="right"
          v-if="user_type === 2"
        >
          <el-form-item label="学号">
            <el-input
              v-model="studentSign.student_id"
              placeholder="请输入学号"
            ></el-input>
          </el-form-item>
          <el-form-item label="姓名">
            <el-input
              v-model="studentSign.student_name"
              placeholder="请输入姓名"
            ></el-input>
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input
              v-model="studentSign.student_email"
              placeholder="请输入邮箱"
            ></el-input>
          </el-form-item>
          <el-form-item class="verifyGet" label="验证码">
            <el-input
              v-model="studentSign.verify"
              placeholder="请输入验证码"
            ></el-input>
            <el-button type="primary" :loading="isLoading" @click="verifyGet"
              >获取</el-button
            >
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="studentSign.student_password"
              type="password"
              placeholder="设置密码"
            ></el-input>
          </el-form-item>
          <el-form-item class="button">
            <el-button type="primary" @click="signup">注册</el-button>
            <el-button type="info" @click="close">取消</el-button>
          </el-form-item>
        </el-form>
        <el-form
          class="visibleForm"
          label-width="20%"
          :model="adminLog"
          label-position="right"
          v-if="user_type === 0"
        >
          <el-form-item label="姓名">
            <el-input
              v-model="adminLog.admin_name"
              placeholder="请输入管理员姓名"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="adminLog.admin_password"
              type="password"
              placeholder="请输入密码"
            ></el-input>
          </el-form-item>
          <el-form-item class="button">
            <el-button type="primary" @click="login">登录</el-button>
            <el-button type="info" @click="close">取消</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import request from "../../utils/request";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";

const router = useRouter();
const isLoading = ref(false);

const loginVisible = ref(false);
const selectedOption = ref("studentLogin");

const user_type = ref(1);
const studentLog = ref({});
const studentSign = ref({});
const adminLog = ref({});

// 关闭登录窗口
function close() {
  loginVisible.value = false;
  isLoading.value = false;
  resetInformation();
}

// 重置数据
function resetInformation() {
  studentLog.value = {};
  studentSign.value = {};
  adminLog.value = {};
}

// 学生/管理员登录
function login() {
  request({
    url: "/login/",
    method: "post",
    data: {
      user_type: user_type.value,
      student_email: studentLog.value.student_email,
      admin_name: adminLog.value.admin_name,
      password:
        user_type.value === 1
          ? studentLog.value.student_password
          : adminLog.value.admin_password,
    },
  })
    .then((res) => {
      localStorage.setItem("token", res.data.token);
      resetInformation();
      if (res.data.code === 200) {
        loginVisible.value = false;
        if (res.data.result.user_type === 1) {
          router.push(`/student/${res.data.result.student_id}`);
        }
        if (res.data.result.user_type === 0) {
          router.push(`/admin/${res.data.result.admin_id}`);
        }
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function verifyGet() {
  isLoading.value = true;
  request({
    url: "/verify/",
    method: "post",
    data: { student_email: studentSign.value.student_email },
  })
    .then((res) => {
      studentSign.value.verify_code = res.data.verify;
      setInterval(() => {
        isLoading.value = false;
      }, 10000);
      console.log(res.data);
    })
    .catch((error) => {
      console.log(error);
    });
}

function signup() {
  request({
    url: "/signUp/",
    method: "post",
    data: studentSign.value,
  })
    .then((res) => {
      user_type.value = 1;
      selectedOption.value = "studentLogin";
    })
    .catch((error) => {
      console.log(error);
    });
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
  }
}
</style>
