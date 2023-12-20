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
        </el-table>
      </el-main>
    </div>
  </el-container>
</template>

<script setup>
import headerNav from "../../components/headerNav/visitor.vue";
import asideNav from "../../components/asideNav/visitor.vue";
import request from "../../utils/request";
import { ref, onMounted } from "vue";

const title = ref();
const author = ref();
const books = ref([]);

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

// 页面挂载阶段获取初识数据
onMounted(() => {
  searchBooks();
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
}
</style>
