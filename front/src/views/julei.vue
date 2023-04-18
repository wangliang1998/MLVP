<template>
  <div class="Echarts">
    <div>
      <div style="width: 24%;float: left;">
        <h5>samples：</h5>
        <el-input placeholder="num" v-model="num"></el-input>
      </div>
      <div style="width: 24%;float: left">
        <h5>noise：</h5>
        <el-input placeholder="noise" v-model="noise"></el-input>
      </div>
      <div style="width: 24%;float: left">
        <h5>centers：</h5>
        <el-input placeholder="centers" v-model="centers"></el-input>
      </div>
      <div style="width: 24%;float: left">
        <h5>cluster_std：</h5>
        <el-input placeholder="cluster_std" v-model="cluster_std"></el-input>
      </div>
      <el-button type="primary" style="margin-top: 10px" @click="submit()">生成数据集</el-button>
    </div >
    <div v-if="show">
      <div class="demo-image">
          <el-image
              :src = 'require("D:\\machine_img\\two\\one\\1.png")'
              fit="fit"></el-image>
      </div>
    </div>
    <div style="width: 98%;float: left;">
      <h5>聚类个数：</h5>
      <el-input placeholder="count" v-model="count"></el-input>
      <el-button type="primary" style="margin-top: 10px" @click="julei()">进行聚类</el-button>
    </div>

    <div v-if="show2">
      <div class="demo-image">
        <el-image
            :src = 'require("D:\\machine_img\\two\\one\\2.png")'
            fit="fit"></el-image>
      </div>
    </div>
    <div style="width: 49%;float: left;">
      <h5>eps：</h5>
      <el-input placeholder="eps" v-model="eps"></el-input>
    </div>
    <div style="width: 49%;float: left">
      <h5>min_samples：</h5>
      <el-input placeholder="min_samples" v-model="min_samples"></el-input>
    </div>
    <el-button type="primary" style="margin-top: 10px" @click="dbscan()">DBSCAN</el-button>
    <div v-if="show3">
      <div class="demo-image">
        <el-image
            :src = 'require("D:\\machine_img\\two\\one\\3.png")'
            fit="fit"></el-image>
      </div>
    </div>
</div>
</template>
<script>
//import axios from "_axios@0.21.1@axios";
import axios from "_axios@0.21.1@axios";
export default {
  name: 'Echarts',
  data () {
    return {
      num:500,
      noise:0.5,
      centers:3,
      cluster_std:0.1,
      show:false,
      show2:false,
      show3:false,
      count: 3,
      eps:0.15,
      min_samples:5
      }
  },
  methods: {
    submit () {
      const _this = this
      _this.show = false
      axios.get('http://127.0.0.1:5000/two/one/create', {
        params: {
          num: _this.num,
          noise: _this.noise,
          centers: _this.centers,
          cluster_std:_this.cluster_std
        }
      }).then(function () {
        _this.show = true
      })
    },
    dbscan () {
      const _this = this
      _this.show3 = false
      axios.get('http://127.0.0.1:5000/two/one/dbscan', {
        params: {
          eps: _this.eps,
          min_samples: _this.min_samples,
        }
      }).then(function () {
        _this.show3 = true
      })
    },
    julei () {
      const _this = this
      _this.show2 = false
      axios.get('http://127.0.0.1:5000/two/one/julei', {
        params: {
          k:_this.count
        }
      }).then(function () {
        _this.show2 = true
      })
    }
  },
  created () {
  },
  mounted () {
    /**
     * iframe-宽高自适应显示
     */
    const oIframe = document.getElementById('main')
    const deviceWidth = document.documentElement.clientWidth
    const deviceHeight = document.documentElement.clientHeight
    oIframe.style.width = (Number(deviceWidth)) + 'px'
    oIframe.style.height = (Number(deviceHeight)) + 'px'
  }
}
</script>
<style scoped>
</style>
