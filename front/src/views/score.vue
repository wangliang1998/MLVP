<template>
  <div class="Echarts">
    <el-button type="primary" style="margin-top: 10px" @click="load()">载入数据</el-button>
    <div v-show="show">
    <el-table
        :data="tableData3"
        border="true"
        height="250"
        style="width: 100%;margin-top: 20px">
      <el-table-column
          prop="num"
          label="账号/学号"
          align="center"
          width="">
      </el-table-column>
      <el-table-column
          prop="name"
          align="center"
          label="学生姓名">
      </el-table-column>
      <el-table-column
          prop="ppt"
          align="center"
          label="PPT的形式和内容">
      </el-table-column>
      <el-table-column
          prop="jiangjie"
          align="center"
          label="讲解的条理、可理解性">
      </el-table-column>
      <el-table-column
          prop="answer"
          align="center"
          label="回答提问的准确性">
      </el-table-column>
      <el-table-column
          prop="class"
          align="center"
          label="讲课小组名">
      </el-table-column>
    </el-table>

    <h3>数据预处理前</h3>
    <el-table
        :data="tableData"
        border="true"
        style="width: 100%">
      <el-table-column
          type="index"
          width="100"
          :index="indexMethod">
      </el-table-column>
      <el-table-column
          prop="num"
          label="账号/学号"
          align="center"
          width="">
      </el-table-column>
      <el-table-column
          prop="name"
          align="center"
          label="学生姓名">
      </el-table-column>
      <el-table-column
          prop="ppt"
          align="center"
          label="PPT的形式和内容">
      </el-table-column>
      <el-table-column
          prop="jiangjie"
          align="center"
          label="讲解的条理、可理解性">
      </el-table-column>
      <el-table-column
          prop="answer"
          align="center"
          label="回答提问的准确性">
      </el-table-column>
      <el-table-column
          prop="class"
          align="center"
          label="讲课小组名">
      </el-table-column>
    </el-table>
    <h3>数据预处理后</h3>
    <el-table
        border="true"
        :data="tableData2"
        style="width: 100%">
      <el-table-column
          type="index"
          width="100"
          :index="indexMethod2">
      </el-table-column>
      <el-table-column
          prop="one"
          label="A"
          align="center"
          width="">
      </el-table-column>
      <el-table-column
          prop="two"
          align="center"
          label="B">
      </el-table-column>
      <el-table-column
          prop="three"
          align="center"
          label="C">
      </el-table-column>
    </el-table>

    <div id="main" style="width: 600px;height:400px;margin-top: 50px">
    </div>
    </div>
  </div>
</template>
<script>
//import axios from "_axios@0.21.1@axios";
import axios from "_axios@0.21.1@axios";

let myChart
export default {
  name: 'Echarts',
  data () {
    return {
      data1: [{}],
      data2: [{}],
      data3: [{}],
      tableData: [{}],
      tableData2: [{}],
      tableData3: [{}],
      show:false
    }
  },
  methods: {
    load () {
      const _this = this
      axios.get('http://127.0.0.1:5000/one/score').then(function (resp) {
        _this.tableData3 = resp.data.data
        _this.show = true
      })
    },
    indexMethod(index) {
      if (index ===0 )
        return 'count'
      if (index ===1)
        return 'unique'
      if (index ===2)
        return 'top'
      if (index ===3)
        return 'freq'
    },
    indexMethod2(index) {
      if (index ===0 )
        return 'count'
      if (index ===1)
        return 'mean'
      if (index ===2)
        return 'std'
      if (index ===3)
        return 'min'
      if (index ===4)
        return '25%'
      if (index ===5)
        return '50%'
      if (index ===6)
        return '75%'
      if (index ===7)
        return 'max'
    },
    myEcharts () {
      // 基于准备好的dom，初始化echarts实例
      myChart = this.$echarts.init(document.getElementById('main'))
      // 指定图表的配置项和数据
      var option;
      option = {
        title: [{
          text: '小组各项评分图',
          left: 'center',
        }, {
          subtext: 'ppt形式与内容',
          left: '16.67%',
          top: '75%',
          textAlign: 'center'
        }, {
          subtext: '讲解条理性',
          left: '50%',
          top: '75%',
          textAlign: 'center'
        }, {
          subtext: '回答问题准确性',
          left: '83.33%',
          top: '75%',
          textAlign: 'center'
        }],
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
        },
        series: [{
          type: 'pie',
          radius: '45%',
          center: ['50%', '50%'],
          data: this.data1,
          label: {
            position: 'outer',
            alignTo: 'none',
            bleedMargin: 5,
            normal : {
              formatter: '{b}: {d}%',
              textStyle : {
                fontWeight : 'normal',
                fontSize : 15
              }
            }
          },
          left: 0,
          right: '66.6667%',
          top: 0,
          bottom: 0
        }, {
          type: 'pie',
          radius: '45%',
          center: ['50%', '50%'],
          data: this.data2,
          label: {
            position: 'outer',
            alignTo: 'labelLine',
            bleedMargin: 5,
            normal : {
              formatter: '{b}: {d}%',
              textStyle : {
                fontWeight : 'normal',
                fontSize : 15
              }
            }
          },
          left: '33.3333%',
          right: '33.3333%',
          top: 0,
          bottom: 0
        }, {
          type: 'pie',
          radius: '45%',
          center: ['50%', '50%'],
          data: this.data3,
          label: {
            position: 'outer',
            alignTo: 'edge',
            margin: 20,
            normal : {
              formatter: '{b}: {d}%',
              textStyle : {
                fontWeight : 'normal',
                fontSize : 15
              }
            }
          },
          left: '66.6667%',
          right: 0,
          top: 0,
          bottom: 0
        }]
      };
      option && myChart.setOption(option);
    }
  },
  created () {
    const _this = this
    axios.get('http://127.0.0.1:5000/two').then(function (resp) {
      _this.data1 = resp.data.data1
      _this.data2 = resp.data.data2
      _this.data3 = resp.data.data3
      _this.tableData = resp.data.data4
      _this.tableData2 = resp.data.data5
      _this.myEcharts()
    })
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
