<template>
  <div class="Echarts">
    <div>
      <el-button type="primary" style="margin-top: 10px" @click="load()">载入数据</el-button>
      <div v-show="show" style="width: 100%;">
        <el-table
            :data="loadtata"
            border="true"
            style="width: 100%;margin-top: 15px">
          <el-table-column
              type="index"
              width="50">
          </el-table-column>
          <el-table-column
              prop="one"
              align="center"
              label="1">
          </el-table-column>
          <el-table-column
              align="center"
              prop="two"
              label="2">
          </el-table-column>
          <el-table-column
              align="center"
              prop="three"
              label="3">
          </el-table-column>
          <el-table-column
              align="center"
              prop="four"
              label="4">
          </el-table-column>
        </el-table>
      </div>
    </div>
  <div>
      <div style="width: 50%;float: left;">
        <h5>minSupport：</h5>
        <el-input placeholder="minSupport" v-model="minSupport"></el-input>
      </div>
    <div style="width: 50%;float: left;">
      <h5>minConf：</h5>
      <el-input placeholder="minConf" v-model="minConf"></el-input>
    </div>
      <el-button type="primary" style="margin-top: 10px" @click="submit()">提交</el-button>
    </div>
    <div style="width: 100%">
      <div id="main" style="width: 70%;height:800px;float: left"></div>
      <label style="float: left;width: 30%;margin-top: 80px">
        <textarea v-show="show2"  style="width: 100%;height: 400px;font-size: 18px;resize:none" v-text="string" readonly></textarea>
      </label>
    </div>
</div>
</template>
<script>
import axios from "_axios@0.21.1@axios";
let myChart
export default {
  name: 'Echarts',
  data () {
    return {
      data: [[]],
      labels:[],
      minSupport:0.2,
      minConf:0.15,
      show:false,
      show2:false,
      loadtata: [{}],
      string:''
    }
  },
  methods: {
    load () {
      const _this = this
      axios.get('http://127.0.0.1:5000/one/shop').then(function (resp) {
        _this.loadtata = resp.data.data
      })
      this.show = true
    },
    submit () {
      if (this.minSupport === '' || this.minConf ===''){
        alert("请完善输入")
        return
      }
      const _this = this
      axios.get('http://127.0.0.1:5000/one', {
        params: {
          minSupport: _this.minSupport,
          minConf:_this.minConf
        }
      }).then(function (resp) {
        _this.show2 = true
        _this.myEcharts(resp.data.data1)
        _this.string = resp.data.data2
      })
    },
    myEcharts (dd) {
      // 基于准备好的dom，初始化echarts实例
      myChart = this.$echarts.init(document.getElementById('main'))
      // 指定图表的配置项和数据
      var option;

      var hours = ['面包', '可乐', '麦片', '牛奶', '鸡蛋'];

      var days = ['面包', '可乐', '麦片', '牛奶', '鸡蛋'];

      var data = dd;

      data = data.map(function (item) {
        return [item[1], item[0], item[2] || '-'];
      });

      option = {
        tooltip: {
          position: 'top'
        },
        grid: {
          height: '50%',
          top: '10%'
        },
        xAxis: {
          type: 'category',
          data: hours,
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: days,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 2,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '25%'
        },
        series: [{
          name: 'Punch Card',
          type: 'heatmap',
          data: data,
          label: {
            show: true
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.9)'
            }
          }
        }]
      };

      option && myChart.setOption(option);
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
