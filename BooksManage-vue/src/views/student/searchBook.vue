<template>
  <el-card
    style="margin-bottom: 1%"
    shadow="hover"
    class="search"
    height="1000"
  >
    <el-input v-model="title" placeholder="请输入书名"></el-input>
    <el-input v-model="author" placeholder="请输入作者"></el-input>
    <el-button type="primary" @click="searchBooks">查询</el-button>
    <el-button @click="reset">重置</el-button>
  </el-card>
  <el-table :data="books" style="width: 100%" stripe>
    <el-table-column prop="book_id" label="书号" />
    <el-table-column prop="book_title" label="书名" />
    <el-table-column prop="book_author" label="作者" />
    <el-table-column prop="book_publisher" label="出版社" />
    <el-table-column prop="book_type" label="类别" />
    <el-table-column prop="book_price" label="定价" />
    <el-table-column prop="book_number" label="数量" />
    <el-table-column label="操作">
      <template #default="scope">
        <el-button
          v-if="scope.row.book_number !== 0"
          type="primary"
          size="small"
          @click="read(scope)"
          >借阅</el-button
        >
        <el-button v-else type="info" size="small" disabled>已空</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import request from "../../utils/request";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const title = ref();
const author = ref();
const books = ref([]);
const route = useRoute();
const student_id = ref(route.params.id);

// 查询图书
function searchBooks() {
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

// 重置
function reset() {
  title.value = "";
  author.value = "";
  searchBooks();
}

// 借阅图书
function read(scope) {
  request({
    url: "/read_back/",
    method: "post",
    data: {
      action: 0,
      book_id: scope.row.book_id,
      student_id: student_id.value,
    },
  })
    .then((res) => {
      console.log(scope.row.book_id);
      console.log(student_id.value);
      searchBooks();
    })
    .catch((error) => {
      console.log(error);
    });
}

// 页面挂载阶段获取初识数据
onMounted(() => {
  searchBooks();
});
</script>

<style lang="less" scoped>
.search {
  padding: 0;
  width: 35%;
  display: flex;
  flex-wrap: nowrap;
  .el-input {
    width: 30%;
    margin-right: 12px;
  }
}
</style>
