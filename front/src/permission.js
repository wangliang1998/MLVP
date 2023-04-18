import router from './router'
import Element from 'element-ui'
// 路由判断登录 根据路由配置文件的参数
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireAuth)) { // 判断该路由是否需要登录权限
    const token = localStorage.getItem('code')
    if (token==='1') { // 判断当前的token是否存在 ； 登录存入的token
      next()
    } else {
      Element.Message.error('请登录')
      next({
        path: '/'
      })
    }
  } else{
    next()
  }
})
