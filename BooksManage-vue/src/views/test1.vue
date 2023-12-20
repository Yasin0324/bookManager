<template>
  <el-button type="primary" @click="login">登录</el-button>
  <el-input v-model="title" placeholder="请输入书名"></el-input>
  <el-input v-model="author" placeholder="请输入作者"></el-input>
  <el-button type="primary" @click="test1">test</el-button>
  <el-button @click="test3">reset</el-button>

  <el-table :data="books" style="width: 100%">
    <el-table-column prop="book_title" label="书名" />
    <el-table-column prop="book_author" label="作者" />
    <el-table-column prop="book_publisher" label="出版社" />
  </el-table>

  <el-form
    :label-position="labelPosition"
    label-width="100px"
    :model="formLabelAlign"
    style="max-width: 460px"
  >
    <el-form-item label="书名">
      <el-input v-model="addbook.book_title" />
    </el-form-item>
    <el-form-item label="id">
      <el-input v-model="addbook.book_id" />
    </el-form-item>
    <el-form-item label="作者">
      <el-input v-model="addbook.book_author" />
    </el-form-item>
    <el-form-item label="类型">
      <el-input v-model="addbook.book_type" />
    </el-form-item>
    <el-form-item label="出版社">
      <el-input v-model="addbook.book_publisher" />
    </el-form-item>
    <el-form-item label="定价">
      <el-input v-model="addbook.book_price" />
    </el-form-item>
    <el-form-item label="数量">
      <el-input v-model="addbook.book_number" />
    </el-form-item>
    <el-button type="primary" @click="test2">test</el-button>
  </el-form>
</template>

<script setup>
import request from "../utils/request";
import { ref, onMounted } from "vue";

const title = ref();
const author = ref();
const books = ref([]);
const addbook = ref({
  book_title: "",
  book_author: "",
  book_publisher: "",
  book_price: 0,
  book_id: 1,
  book_type: "",
  book_number: 0,
  admin_id: 1,
});
const user_type = ref(1);

function login() {
  request({
    url: "/login/",
    method: "post",
    data: {
      user_type: user_type.value,
      student_email: "1848737490@qq.com",
      password: "1224",
    },
  })
    .then((res) => {
      console.log(user_type.value);
      console.log(res.data);
      localStorage.setItem("token", res.data.token);
    })
    .catch((error) => {
      console.log(error);
    });
}

function test1() {
  request({
    url: `/getBooks/`,
    method: "get",
    params: { book_title: title.value, book_author: author.value },
  })
    .then((res) => {
      console.log(res.data);
      books.value = res.data.results;
      console.log(books.value);
      console.log(res.data.results);
    })
    .catch((error) => {
      console.log(error);
    });
}
function test2() {
  request({
    url: "/addBook/",
    method: "post",
    data: addbook.value,
  })
    .then((res) => {
      console.log(addbook.value);
      console.log(res.data);
    })
    .catch((error) => {
      console.log(error);
    });
}
function test3() {
  title.value = "";
  author.value = "";
  test1();
}
// onMounted(() => {
//   test1();
// });
</script>

<style lang="less" scoped></style>
