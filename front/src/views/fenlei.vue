<template>
  <div class="Echarts">
    <el-button type="primary" style="margin-top: 10px" @click="load()">载入数据</el-button>
    <div v-show="show2">
    <el-table
        :data="tableData"
        border="true"
        height="250"
        style="width: 100%;margin-top: 20px">
      <el-table-column
          prop="num"
          label="id"
          align="center"
          width="">
      </el-table-column>
      <el-table-column
          prop="name"
          align="center"
          label="Sepal.Length">
      </el-table-column>
      <el-table-column
          prop="ppt"
          align="center"
          label="Sepal.Width">
      </el-table-column>
      <el-table-column
          prop="jiangjie"
          align="center"
          label="Petal.Length">
      </el-table-column>
      <el-table-column
          prop="answer"
          align="center"
          label="Petal.Width">
      </el-table-column>
      <el-table-column
          prop="class"
          align="center"
          label="Species">
      </el-table-column>
    </el-table>
    </div>
    <div>
      <div style="width: 49%;float: left;">
        <h5>max_depth：</h5>
        <el-input placeholder="max_depth" v-model="max_depth"></el-input>
      </div>
      <div style="width: 49%;float: left">
        <h5>min_samples_leaf：</h5>
        <el-input placeholder="min_samples_leaf" v-model="min_samples_leaf"></el-input>
      </div>
      <el-button type="primary" style="margin-top: 10px" @click="submit()">提交</el-button>
    </div>
    <div v-if="show">
      <div class="demo-image" style="width: 49%;float: left">
        <h3>决策树</h3>
        <el-image
            style="width: 600px;height: 400px"
            :src = 'require("D:\\machine_img\\three\\1.png")'
            fit="fit"></el-image>
      </div>
      <div class="demo-image" style="width: 49%;float: left">
        <h3>最优决策树</h3>
        <el-image
            style="width: 600px;height: 400px"
            :src = 'require("D:\\machine_img\\three\\2.png")'
            fit="fit"></el-image>
      </div>
    </div>
      <div style="width: 49%;float: left">
        <h4 v-if="show">DecisionTreeClassifier参数调优前后对比(训练集)</h4>
        <div id="main" style="width: 600px;height:400px;margin-top: 20px;">
        </div>
      </div>
      <div style="width: 49%;float: left">
        <h4 v-if="show">DecisionTreeClassifier参数调优前后对比(测试集)</h4>
        <div id="main2" style="width: 600px;height:400px;">
        </div>
      </div>

  </div>
</template>
<script>
import axios from "_axios@0.21.1@axios";
let myChart
let myChart2
export default {
  name: 'Echarts',
  data () {
    return {
      tableData:[{}],
      data: [[]],
      labels:[],
      max_depth:3,
      min_samples_leaf:10,
      show:false,
      show2:false
    }
  },
  methods: {
    load () {
      const _this = this
      axios.get('http://127.0.0.1:5000/three/iris').then(function (resp) {
        _this.tableData = resp.data.data
        _this.show2 = true
      })
    },
    submit () {
      const _this = this
      _this.show = false
      axios.get('http://127.0.0.1:5000/three/create', {
        params: {
          max_depth: _this.max_depth,
          min_samples_leaf: _this.min_samples_leaf
        }
      }).then(function (resp) {
        _this.show = true
        _this.myEcharts(resp.data.data1)
        _this.myEcharts2(resp.data.data2)
      })
    },
    myEcharts (da) {
      // 基于准备好的dom，初始化echarts实例
      myChart = this.$echarts.init(document.getElementById('main'))
      // 指定图表的配置项和数据
      var option;
      option = {
        legend: {
        },
        tooltip: {},
        dataset: {
          source: da
        },
        xAxis: {type: 'category'},
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [

          {type: 'bar',
            itemStyle: {
              normal: {
                label: {
                  show: true, //开启显示
                  position: 'top', //在上方显示
                  textStyle: { //数值样式
                    color: 'black',
                    fontSize: 16
                  }
                }
              }
            },
          },
          {type: 'bar',
            itemStyle: {
              normal: {
                label: {
                  show: true, //开启显示
                  position: 'top', //在上方显示
                  textStyle: { //数值样式
                    color: 'black',
                    fontSize: 16
                  }
                }
              }
            },
          }
        ]
      };
      myChart.setOption(option);
    },
    myEcharts2 (da) {
      // 基于准备好的dom，初始化echarts实例
      myChart2 = this.$echarts.init(document.getElementById('main2'))
      // 指定图表的配置项和数据
      var option;
      option = {
        legend: {},
        tooltip: {},
        dataset: {
          source: da
        },
        xAxis: {type: 'category'},
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          {type: 'bar',
            itemStyle: {
              normal: {
                label: {
                  show: true, //开启显示
                  position: 'top', //在上方显示
                  textStyle: { //数值样式
                    color: 'black',
                    fontSize: 16
                  }
                }
              }
            },},
          {type: 'bar',
            itemStyle: {
              normal: {
                label: {
                  show: true, //开启显示
                  position: 'top', //在上方显示
                  textStyle: { //数值样式
                    color: 'black',
                    fontSize: 16
                  }
                }
              }
            },}
        ]
      };
      myChart2.setOption(option);
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
