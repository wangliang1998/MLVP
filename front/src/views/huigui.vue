<template>
  <div class="Echarts">
    <div>
      <div style="width: 49%;float: left;">
        <h5>n_samples：</h5>
        <el-input placeholder="n_samples" v-model="n_samples"></el-input>
      </div>
      <div style="width: 49%;float: left">
        <h5>n_outliers：</h5>
        <el-input placeholder="n_outliers" v-model="n_outliers"></el-input>
      </div>
      <el-button type="primary" style="margin-top: 10px" @click="submit()">生成</el-button>
    </div>
    <div style="width: 49%;float: left">
      <div id="main" style="width: 600px;height:400px;">
      </div>
    </div>
    <div style="width: 49%;float: left">
      <div id="main2" style="width: 600px;height:400px;">
      </div>
    </div>
    <el-button type="primary" style="margin-top: 10px" @click="submit2()">回归</el-button>
    <div style="width: 100%;text-align: center">
      <div style="width: 49%;float: left">
        <div id="main3" style="width: 600px;height:400px;">
        </div>
      </div>
      <div style="width: 49%;float: left">
        <div id="main4" style="width: 600px;height:400px;">
        </div>
      </div>
    </div>
    <div style="width: 100%">
      <div style="width: 25%;float: left;">
        <h5>min_samples：</h5>
        <el-input placeholder="min_samples" v-model="min_samples"></el-input>
      </div>
      <div style="width: 25%;float: left;">
        <h5>residual_threshold：</h5>
        <el-input placeholder="residual_threshold" v-model="residual_threshold"></el-input>
      </div>
      <div style="width: 25%;float: left;">
        <h5>stop_n_inliers：</h5>
        <el-input placeholder="stop_n_inliers" v-model="stop_n_inliers"></el-input>
      </div>
      <div style="width: 25%;float: left;">
        <h5>max_trials：</h5>
        <el-input placeholder="max_trials" v-model="max_trials"></el-input>
      </div>
    </div>
    <el-button type="primary" style="margin-top: 10px" @click="submit3()">RANSAC回归</el-button>
    <div id="main5" style="width: 600px;height:400px;margin: 0 auto;margin-top: 30px">
      </div>
  </div>
</template>
<script>
import axios from "_axios@0.21.1@axios";
let myChart
let myChart2
let myChart3
let myChart4
let myChart5
export default {
  name: 'Echarts',
  data () {
    return {
      data: [[]],
      labels:[],
      n_samples:500,
      n_outliers:100,
      train:[[]],
      min_samples:10,
      residual_threshold:25.0,
      stop_n_inliers:320,
      max_trials:100
    }
  },
  methods: {
    submit3 () {
      const _this = this
      axios.get('http://127.0.0.1:5000/four/ransac',{
        params:{
          min_samples:_this.min_samples,
          residual_threshold:_this.residual_threshold,
          stop_n_inliers:_this.stop_n_inliers,
          max_trials:_this.max_trials
        }
      }).then(function (resp) {
        _this.myEcharts5(resp.data.data1,resp.data.data2,resp.data.data3)
      })

    },
    submit2 () {
      const _this = this
      axios.get('http://127.0.0.1:5000/four/huihui').then(function (resp) {
        _this.myEcharts3(_this.train,resp.data.data1)
        _this.myEcharts4(_this.train,resp.data.data2)
      })

    },
    submit () {
      const _this = this
      _this.show = false
      axios.get('http://127.0.0.1:5000/four/create', {
        params: {
          n_samples: _this.n_samples,
          n_outliers: _this.n_outliers
        }
      }).then(function (resp) {
        _this.train = resp.data.train
        _this.myEcharts(resp.data.train)
        _this.myEcharts2(resp.data.test)
      })
    },
    myEcharts (da) {
      // 基于准备好的dom，初始化echarts实例
      myChart = this.$echarts.init(document.getElementById('main'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: {
          text: '训练集',
          left: 'center',
          top: 0
        },
        xAxis: {},
        yAxis: {},
        series: [{
          symbolSize: 5,
          data: da,
          type: 'scatter'
        }]
      };
      myChart.setOption(option);
    },
    myEcharts2 (dd) {
      // 基于准备好的dom，初始化echarts实例
      myChart2 = this.$echarts.init(document.getElementById('main2'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: {
          text: '测试集',
          left: 'center',
          top: 0
        },
        xAxis: {},
        yAxis: {},
        series: [{
          symbolSize: 5,
          data: dd,
          type: 'scatter'
        }]
      };
      myChart2.setOption(option);
    },
    myEcharts3 (da,line) {
      // 基于准备好的dom，初始化echarts实例
      myChart3 = this.$echarts.init(document.getElementById('main3'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: {
          text: '一元线性回归',
          left: 'center',
          top: 0
        },
        xAxis: {},
        yAxis: {},
        series: [{
          symbolSize: 5,
          data: da,
          type: 'scatter'
        },
          {
            data: line,
            smooth: true,
            type: 'line',
            symbol: 'none',
            lineStyle: {
                  type: 'solid',
                  color:'blue'
                }
          }]
      };
      myChart3.setOption(option);
    },
    myEcharts4 (da,line) {
      // 基于准备好的dom，初始化echarts实例
      myChart4 = this.$echarts.init(document.getElementById('main4'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: {
          text: '二元线性回归',
          left: 'center',
          top: 0
        },
        xAxis: {},
        yAxis: {},
        series: [{
          symbolSize: 5,
          data: da,
          type: 'scatter'
        },
          {
            data: line,
            type: 'line',
            smooth: true,
            symbol: 'none',
            lineStyle: {
              type: 'solid',
              color:'blue'
            }
          }]
      };
      myChart4.setOption(option);
    },
    myEcharts5 (data1,data2,data3) {
      // 基于准备好的dom，初始化echarts实例
      myChart5 = this.$echarts.init(document.getElementById('main5'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: {
          text: 'RANSAC回归',
          left: 'center',
          top: 0
        },
        xAxis: {},
        yAxis: {},
        series: [{
          color:'blue',
          symbolSize: 5,
          data: data1,
          type: 'scatter'
        },
          {
            color:'red',
            symbolSize: 5,
            data: data2,
            type: 'scatter'
          },
          {
            data: data3,
            type: 'line',
            smooth: true,
            symbol: 'none',
            lineStyle: {
              type: 'solid',
              color:'black'
            }
          }]
      };
      myChart5.setOption(option);
    }
  },
  created () {
    // const _this = this
    // axios.get('http://127.0.0.1:5000/one').then(function (resp) {
    //   _this.myEcharts(resp.data.data,resp.data.name)
    //   //alert(resp.data.data)
    // })
  },
  mounted () {
    /**
     * iframe-宽高自适应显示
     */
  }
}
</script>
<style scoped>
</style>
