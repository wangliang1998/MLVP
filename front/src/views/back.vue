<template>
  <div id="iframeId">
    <el-container>
      <el-header style="background: url('/img/bg.jpg')  no-repeat 0 -1000px" height="70">
        <div  style="width: 100%;">
          <div style="text-align: left;width: 80%;float:left;">
            <h1 style="margin: 0 auto;color: white">机器学习可视化平台</h1>
          </div>
          <el-button type="danger" icon="el-icon-switch-button" size="medium"  round="true" @click="exit">退出登录</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" id="el-aside">
          <el-row class="tac">
            <el-col :span="12" style="width: 200px">
              <el-menu
                default-active="2"
                class="el-menu-vertical-demo"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b"
                @open="handleOpen"
                @close="handleClose">
                <el-submenu index="1">
                  <template slot="title">
                    <i class="el-icon-menu"></i>
                    <span>实验一</span>
                  </template>
                  <el-menu-item-group>
                    <el-menu-item index="1-1" @click="to(1)"><i class="el-icon-user"></i>Apriori算法画热力图</el-menu-item>
                    <el-menu-item index="1-2" @click="to(2)"><i class="el-icon-user"></i>打分表指标分析饼图</el-menu-item>
                  </el-menu-item-group>
                </el-submenu>
                <el-submenu index="2">
                  <template slot="title">
                    <i class="el-icon-menu"></i>
                    <span>实验二：聚类</span>
                  </template>
                  <el-menu-item-group>
                    <el-menu-item index="2-1" @click="to(3)"><i class="el-icon-user"></i>人工数据集</el-menu-item>
                  </el-menu-item-group>
                </el-submenu>
                <el-submenu index="3">
                  <template slot="title">
                    <i class="el-icon-menu"></i>
                    <span>实验三：分类</span>
                  </template>
                  <el-menu-item-group>
                    <el-menu-item index="3-1" @click="to(4)"><i class="el-icon-user"></i>决策树</el-menu-item>
                  </el-menu-item-group>
                </el-submenu>
                <el-submenu index="4">
                  <template slot="title">
                    <i class="el-icon-menu"></i>
                    <span>实验四：回归</span>
                  </template>
                  <el-menu-item-group>
                    <el-menu-item index="4-1" @click="to(5)"><i class="el-icon-user"></i>回归模型</el-menu-item>
                  </el-menu-item-group>
                </el-submenu>
              </el-menu>
            </el-col>
          </el-row>
        </el-aside>
        <el-main style="overflow-y: hidden">
          <iframe style="border: none;overflow-y: hidden"  rameborder="0" :src="url" width="100%" height="100%"></iframe>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'back',
  data () {
    return {
      height: '600px',
      url: ''
    }
  },
  methods: {
    exit () {
      const _this = this
      _this.$store.commit('REMOVE_CODE')
      _this.$router.push('/')
      Element.Message.success('退出成功')
    },
    to (index) {
      if (index === 1) {
        this.url = '/back/hot'
      } else if (index === 2) {
        this.url = '/back/score'
      } else if (index === 3) {
        this.url = '/back/julei'
      }else if (index === 4) {
        this.url = '/back/fenlei'
      }else if (index === 5) {
        this.url = '/back/huigui'
      }
    }
  },
  created () {
    document.title = '后台管理系统'
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
    document.getElementById('el-aside').style.height = (Number(deviceHeight) - 70) + 'px'
    document.getElementById('el-aside').style.background = '#545c64'
  }
}
</script>
<style scoped>
.el-header, .el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 70px;
  height: 70px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  line-height: 500px;
}

.el-main {
  background-color: white;
  color: #333;
  text-align: left;
  line-height: 500px;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>
