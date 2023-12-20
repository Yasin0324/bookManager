<template>
  <el-table :data="mergedData" style="width: 100%" stripe>
    <el-table-column prop="book_id" label="书号" />
    <el-table-column prop="book_title" label="书名" />
    <el-table-column prop="student_name" label="学生" />
    <el-table-column prop="student_email" label="联系邮箱" />
    <el-table-column prop="read_time" label="借阅时间" />
    <el-table-column prop="back_time" label="归还时间" />
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
const admin_id = ref(route.params.id);

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

const students = ref([]);
// 查询学生信息
function getStudent() {
  request({
    url: "/studentInformation/",
    post: "get",
  })
    .then((res) => {
      console.log(res.data.results);
      students.value = res.data.results;
    })
    .catch((error) => {
      console.log(error);
    });
}

// 查询借阅记录
function searchBooks() {
  request({
    url: `/readInformation/`,
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
      console.log(books.value);
      setTimeout(() => {
        mergeBooksAndStudents();
      }, 500);
    })
    .catch((error) => {
      console.log(error);
    });
}

const mergedData = ref([]);
// 数据合并
function mergeBooksAndStudents() {
  // 先获取所有的书籍和学生信息
  Promise.all([books, students]).then(() => {
    // 遍历books数组
    for (let book of books.value) {
      // 在student数组中找到与当前book对象的student_id匹配的student对象
      let student = students.value.find(
        (s) => s.student_id === book.student_id
      );

      // 如果找到了匹配的student对象，就将book对象和student对象合并，并添加到mergedData数组中
      if (student) {
        mergedData.value.push({
          ...book,
          ...student,
        });
      }
    }

    // 打印出合并后的数据
    console.log(mergedData.value);
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
  getStudent();
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
