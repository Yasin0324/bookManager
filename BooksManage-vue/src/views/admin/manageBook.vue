<template>
  <div class="button">
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
    <el-button class="add" type="primary" @click="add">新增</el-button>
  </div>
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
        <el-button size="small" @click="update(scope)">编辑</el-button>
        <el-button type="danger" size="small" @click="del(scope)"
          >删除</el-button
        >
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
    class="dialog"
    :title="visibleTitle"
    v-model="manageBookVisible"
    align-center
    draggable="true"
    width="25%"
  >
    <el-form :model="book" label-width="100px">
      <el-form-item label="书名">
        <el-input v-model="book.book_title" placeholder="请输入书名"></el-input>
      </el-form-item>
      <el-form-item label="作者">
        <el-input
          v-model="book.book_author"
          placeholder="请输入作者"
        ></el-input>
      </el-form-item>
      <el-form-item label="出版社">
        <el-input
          v-model="book.book_publisher"
          placeholder="请输入出版社"
        ></el-input>
      </el-form-item>
      <el-form-item label="类别">
        <el-input v-model="book.book_type" placeholder="请输入类别"></el-input>
      </el-form-item>
      <el-form-item label="定价">
        <el-input v-model="book.book_price" placeholder="请设置定价"></el-input>
      </el-form-item>
      <el-form-item label="数量">
        <el-input
          v-model="book.book_number"
          placeholder="请设置数量"
        ></el-input>
      </el-form-item>
      <el-form-item class="dialogButton">
        <el-button
          type="primary"
          @click="action === 'add' ? addBook() : updateBook()"
          >{{ action === "add" ? "添加" : "修改" }}</el-button
        >
        <el-button type="info" @click="close">取消</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
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
const manageBookVisible = ref(false);
const action = ref("");
const visibleTitle = ref("");
const book = ref({});

// 打开新增图书窗口
function add() {
  action.value = "add";
  visibleTitle.value = "新增";
  manageBookVisible.value = true;
  console.log(action.value, action.value === "add");
}

// 打开编辑图书窗口
function update(scope) {
  action.value = "update";
  visibleTitle.value = "编辑";
  manageBookVisible.value = true;
  book.value = scope.row;
  console.log(scope.row);
  console.log(book.value);
}

// 关闭新增/编辑窗口
function close() {
  manageBookVisible.value = false;
  book.value = {};
}

// 添加图书
function addBook() {
  request({
    url: "/addBook/",
    method: "post",
    data: {
      action: 0,
      book_title: book.value.book_title,
      book_type: book.value.book_type,
      book_price: book.value.book_price,
      book_author: book.value.book_author,
      book_publisher: book.value.book_publisher,
      book_number: book.value.book_number,
      admin_id: admin_id.value,
    },
  })
    .then((res) => {
      console.log(res.data);
      manageBookVisible.value = false;
      searchBooks();
    })
    .catch((error) => {
      console.log(error);
    });
}

// 修改图书信息
function updateBook() {
  request({
    url: "/addBook/",
    method: "post",
    data: {
      action: 1,
      book_id: book.value.book_id,
      book_title: book.value.book_title,
      book_type: book.value.book_type,
      book_price: book.value.book_price,
      book_author: book.value.book_author,
      book_publisher: book.value.book_publisher,
      book_number: book.value.book_number,
      admin_id: admin_id.value,
    },
  })
    .then((res) => {
      console.log(res.data);
      manageBookVisible.value = false;
      searchBooks();
    })
    .catch((error) => {
      console.log(error);
    });
}

// 删除图书
function del(scope) {
  request({
    url: "/addBook/",
    method: "post",
    data: {
      book_id: scope.row.book_id,
      action: 2,
    },
  })
    .then((res) => {
      console.log(scope.row.book_id);
      console.log(res);
      searchBooks();
    })
    .catch((error) => {
      console.log(error);
    });
}

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
.button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  .add {
    margin-right: 8%;
  }
}
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
.dialog {
  .el-form {
    .el-form-item {
      width: 90%;
    }
  }
}
</style>
