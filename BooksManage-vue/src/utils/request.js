import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
    baseURL: 'http://localhost:5000',
    timeout:1000000,
})

request.interceptors.request.use((config) => {
    config.headers['token']=localStorage.getItem('token')
    return config
}, (error) => {
    return Promise.reject(error)
})

request.interceptors.response.use((res) => {
    if (res.data.code === 200) {
        if(res.data.tip!==0){
        ElMessage({
            message: res.data.message,
            type: 'success',
            duration:1500
        })}
    }
    if (res.data.code !== 200) {
        ElMessage({
            message: res.data.message,
            type: 'warning',
            duration:1500
        })
    }
    return res
}, (error) => {
    return error
})

export default request