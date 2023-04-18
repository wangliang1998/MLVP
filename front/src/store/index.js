import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    code:0
  },
  mutations: {
    SET_CODE: (state, code) => {
      state.code = code
      localStorage.setItem('code', code)
    },
    REMOVE_CODE: (state) => {
      state.code = 0
      localStorage.setItem('code', '0')
    }
  },
  getters:{
    // get
    getCode: state => {
      return state.code
    }
  },
  actions: {
  },
  modules: {
  }
})
