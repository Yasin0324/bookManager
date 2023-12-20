<template>
  <el-table :data="books" style="width: 100%" stripe>
    <el-table-column prop="book_id" label="书号" />
    <el-table-column prop="book_title" label="书名" />
    <el-table-column prop="book_author" label="作者" />
    <el-table-column prop="book_publisher" label="出版社" />
    <el-table-column prop="read_time" label="借阅时间" />
    <el-table-column prop="back_time" label="归还时间" />
    <el-table-column label="操作">
      <template #default="scope">
        <el-button
          v-if="scope.row.back_time === null"
          type="primary"
          size="small"
          @click="back(scope)"
          >归还</el-button
        >
        <el-button v-else type="info" size="small" disabled>已还</el-button>
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

// 时间格式化
function formatDate(dateString) {
  if (!dateString) {
    return null;
  }
  let date = new Date(dateString);
  return date.toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

// 查询借阅记录
function searchBooks() {
  request({
    url: `/readInformation/${student_id.value}`,
    method: "get",
  })
    .then((res) => {
      books.value = res.data.results.map((book) => {
        return {
          ...book,
          read_time: formatDate(book.read_time),
          back_time: formatDate(book.back_time),
        };
      });
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

// 归还图书
function back(scope) {
  request({
    url: "/read_back/",
    method: "post",
    data: {
      action: 1,
      book_id: scope.row.book_id,
      read_id: scope.row.read_id,
      student_id: student_id.value,
    },
  })
    .then((res) => {
      console.log(scope.row.read_id);
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
