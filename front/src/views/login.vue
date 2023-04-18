<template>
<div id="iframeId" style="text-align: center;background: url('/img/login.jpeg');background-size:100% 100%;background-attachment: fixed;">
  <div id="login">
    <h1 style="font-size: large;color: white">请登录</h1>
    <input type="text" required="required" placeholder="用户名" v-model="username">
    <input type="password" required="required" placeholder="密码" v-model="password">
    <Verify @success="login(0)" @error="login(1)" :type="1" codeLength="4" height="30px" width="120px"></Verify>
  </div>
</div>
</template>
<script>

import axios from '_axios@0.21.1@axios'
import Element from 'element-ui'
import Verify from 'vue2-verify'
export default {
  name: 'login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login (sta) {
      if(sta===1){
        Element.Message.error('验证码错误')
        return;
      }
      if (this.username === '' || this.password === '') {
        Element.Message.error('用户名或密码不能为空')
        return
      }
      const _this = this
      axios.get('http://127.0.0.1:5000/login', {
        params: {
          username: _this.username,
          password: _this.password
        }
      }).then(function (resp) {
        const code = resp.data.code
        // 把数据共享出去
        _this.$store.commit('SET_CODE', code)
        // 获取
       if (code === 0){
         Element.Message.error('用户名或密码错误')
       }else{
         _this.$router.push('/back')
       }
      })
    }
  },
  components: {
    Verify
  },
  mounted () {
    /**
     * iframe-宽高自适应显示
     */
    const oIframe = document.getElementById('iframeId')
    const deviceWidth = document.documentElement.clientWidth
    const deviceHeight = document.documentElement.clientHeight
    oIframe.style.width = (Number(deviceWidth)) + 'px'
    oIframe.style.height = (Number(deviceHeight)) + 'px'
  },
  created () {
    document.title = '登录'
  }

}
</script>
<style scoped>
#login{
  position: absolute;
  top: 50%;
  left:50%;
  margin: -150px 0 0 -150px;
  width: 300px;
  height: 300px;
}
#login h1{
  color: black;
  letter-spacing: 1px;
  text-align: center;
}
h1{
  font-size: 15px;
  margin: 0.67em 0;
}
input{
  width: 278px;
  height: 25px;
  margin-bottom: 10px;
  outline: none;
  padding: 10px;
  font-size: 13px;
  color: black;
  text-shadow:1px 1px 1px;
  border-top: 1px solid #312E3D;
  border-left: 1px solid #312E3D;
  border-right: 1px solid #312E3D;
  border-bottom: 1px solid #56536A;
  border-radius: 4px;
  background-color: white;
}
.but{
  width: 298px;
  min-height: 25px;
  display: block;
  background-color: #4a77d4;
  border: 1px solid #3762bc;
  color: #fff;
  padding: 9px 14px;
  font-size: 15px;
  line-height: normal;
  border-radius: 5px;
  margin: 0;
}
</style>
