import Vue from 'vue'
import VueRouter from 'vue-router'
import back from "../views/back";
import hot from "../views/hot";
import score from "../views/score";
import julei from "../views/julei";
import fenlei from "../views/fenlei";
import huigui from "../views/huigui";
import login from "../views/login";


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/back',
    name: 'back',
    component: back,
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/back/hot',
    name: 'hot',
    components: {
      movieMain: hot
    },
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/back/score',
    name: 'score',
    components: {
      movieMain: score
    },
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/back/julei',
    name: 'julei',
    components: {
      movieMain: julei
    },
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/back/fenlei',
    name: 'feilei',
    components: {
      movieMain: fenlei
    },
    meta: {
      requireAuth: true
    }
  },
  {
    path: '/back/huigui',
    name: 'huihui',
    components: {
      movieMain: huigui
    },
    meta: {
      requireAuth: true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
