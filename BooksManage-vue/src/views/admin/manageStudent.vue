<template>
  <el-card
    style="margin-bottom: 1%"
    shadow="hover"
    class="search"
    height="1000"
  >
    <el-input v-model="name" placeholder="查询学生姓名"></el-input>
    <el-button type="primary" @click="getStudent">查询</el-button>
    <el-button @click="reset">重置</el-button>
  </el-card>
  <el-table :data="students" style="width: 100%" stripe>
    <el-table-column prop="student_id" label="学号" />
    <el-table-column prop="student_name" label="姓名" />
    <el-table-column prop="student_email" label="联系邮箱" />
    <el-table-column label="密码">
      <template #default="scope">
        <el-popover
          placement="top-start"
          trigger="hover"
          :content="scope.row.student_password"
        >
          <template #reference>
            <el-button class="m-2" size="small">查看</el-button>
          </template>
        </el-popover>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import request from "../../utils/request";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const admin_id = ref(route.params.id);
const name = ref();
const students = ref([]);

// 查询学生信息
function getStudent() {
  request({
    url: `/studentInformation/`,
    method: "get",
    params: { student_name: name.value },
  })
    .then((res) => {
      students.value = res.data.results;
      console.log(res.data.results);
    })
    .catch((error) => {
      console.log(error);
    });
}

// 重置
function reset() {
  name.value = '';
  getStudent();
}

// 页面挂载阶段获取初识数据
onMounted(() => {
  getStudent();
});
</script>

<style lang="less" scoped>
.search {
  padding: 0;
  width: 23%;
  display: flex;
  flex-wrap: nowrap;
  .el-input {
    width: 50%;
    margin-right: 12px;
  }
}
</style>
