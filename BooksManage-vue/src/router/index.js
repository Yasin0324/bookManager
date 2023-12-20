import { createRouter, createWebHashHistory } from "vue-router"
import { ElMessage } from 'element-plus'

import visitor from "../views/visitor/index.vue"
import student from '../views/student/index.vue'
import student_searchBook from '../views/student/searchBook.vue'
import student_readInformation from '../views/student/readInformation.vue'

import admin from '../views/admin/index.vue'
import manageBook from '../views/admin/manageBook.vue'
import manageStudent from '../views/admin/manageStudent.vue'
import admin_readInformation from '../views/admin/readInformation.vue'

const routes = [
    {
        name: 'visitor',
        path: '/',
        component: visitor,
    },
    {
        path: '/student/:id',
        component: student,
        children: [
            {
                path: 'searchBook', name: 'searchBook',component:student_searchBook
            },
            {
                path: 'readInformation', name: 'sreadInformation',component:student_readInformation
            }
        ]
    },
    {
        path: '/admin/:id',
        component: admin,
        children: [
            {
                path: 'manageBook', name: 'manageBook',
                component:manageBook
            },
            {
                path: 'manageStudent', name: 'manageStudent',
                component:manageStudent
            },
            {
                path: 'readInformation', name: 'readInformation',
                component:admin_readInformation
            }
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

router.beforeEach((to, form, next) => {
    const authRequired = to.name !=='visitor'

    const token = localStorage.getItem('token')

    if (authRequired&&!token) {
        ElMessage({
            message: '请先登录',
            type: 'warning',
            duration:3000
        })
        next(false)
    } else {
        next()
    }
})

export default router