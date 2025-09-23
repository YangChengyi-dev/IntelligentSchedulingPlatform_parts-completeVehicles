/**
 * 全站路由配置
 *
 * 建议:
 * 1. 代码中路由统一使用name属性跳转(不使用path属性)
 */
import Vue from 'vue'
import Router from 'vue-router'
import http from '@/utils/httpRequest'
import {
  isURL
} from '@/utils/validate'
import {
  clearLoginInfo
} from '@/utils'
import store from '@/store'
Vue.use(Router)


// 开发环境不使用懒加载, 因为懒加载页面太多的话会造成webpack热更新太慢, 所以只有生产环境使用懒加载
const _import = require('./import-' + process.env.NODE_ENV)

// 全局路由(无需嵌套上左右整体布局)
const globalRoutes = [{
  path: '/404',
  component: _import('modules/404'),
  name: 'g404',
  meta: {
    title: '404未找到'
  }
},
{
  path: '/login',
  component: _import('common/login'),
  name: 'login',
  meta: {
    title: '登录'
  }
}, {
  path: '/',
  component: _import('common/login'),
  redirect: {
    name: 'login'
  },

},
{
  path: '/register',
  component: _import('common/register'),
  name: 'register',
  meta: {
    title: '注册'
  }
}

]

// 主入口路由(需嵌套上左右整体布局)
const mainRoutes = {
  path: '/index',
  component: _import('index'),
  name: 'index',
  redirect: {
    path: '/index/chargeOperation/overview/overview'
  },
  meta: {
    title: '主入口整体布局'
  },
  children: [
    // 通过meta对象设置路由展示方式
    // 1. isTab: 是否通过tab展示内容, true: 是, false: 否
    // 2. iframeUrl: 是否通过iframe嵌套展示内容, '以http[s]://开头': 是, '': 否
    // 提示: 如需要通过iframe嵌套展示内容, 但不通过tab打开, 请自行创建组件使用iframe处理!
    {
      path: '/theme',
      component: _import('common/theme'),
      name: 'theme',
      meta: {
        title: '主题'
      }
    },
    {
      path: '/distribuUser',
      component: _import('modules/systemManager/role/distribuUser'),
      name: 'distribuUser',
      meta: {
        title: '分配用户',
        isTab: true
      }
    },
    {
      path: '/typeData',
      component: _import('modules/systemManager/type/typeData'),
      name: 'typeData',
      meta: {
        title: '字典数据',
        isTab: true
      }
    },
    {
      path: '/jobLog',
      component: _import('modules/monitor/job/typeData'),
      name: 'jobLog',
      meta: {
        title: '调度日志',
        isTab: true
      }
    },
    {
      path: '/userTag',
      component: _import('modules/systemManager/person/userTag'),
      name: 'userTag',
      meta: {
        title: '用户分配角色',
        isTab: true
      }
    },

  ],
  // beforeEnter(to, from, next) {
  //   let token = Vue.cookie.get('cookie');
  //   if (!token || !/\S/.test(token)) {
  //     clearLoginInfo()
  //     // next({ name: 'login' })
  //   }
  //   next()
  // }
}
const newMainRoutes = {
  path: '/index',
  component: _import('index'),
  name: 'index',
  redirect: {
    path: '/index/chargeOperation/overview/overview'
  },
  meta: {
    title: '主入口整体布局'
  },
  children: [
    // 通过meta对象设置路由展示方式
    // 1. isTab: 是否通过tab展示内容, true: 是, false: 否
    // 2. iframeUrl: 是否通过iframe嵌套展示内容, '以http[s]://开头': 是, '': 否
    // 提示: 如需要通过iframe嵌套展示内容, 但不通过tab打开, 请自行创建组件使用iframe处理!
    {
      path: '/theme',
      component: _import('common/theme'),
      name: 'theme',
      meta: {
        title: '主题'
      }
    },
    {
      path: '/distribuUser',
      component: _import('modules/systemManager/role/distribuUser'),
      name: 'distribuUser',
      meta: {
        title: '分配用户',
        isTab: true
      }
    },
    {
      path: '/typeData',
      component: _import('modules/systemManager/type/typeData'),
      name: 'typeData',
      meta: {
        title: '字典数据',
        isTab: true
      }
    },
    {
      path: '/jobLog',
      component: _import('modules/monitor/job/typeData'),
      name: 'jobLog',
      meta: {
        title: '调度日志',
        isTab: true
      }
    }, {
      path: '/userTag',
      component: _import('modules/systemManager/person/userTag'),
      name: 'userTag',
      meta: {
        title: '用户分配角色',
        isTab: true
      }
    },
  ],
  // beforeEnter(to, from, next) {
  //   let token = Vue.cookie.get('token');
  //   if (!token || !/\S/.test(token)) {
  //     clearLoginInfo()
  //     // next({ name: 'login' })
  //   }
  //   next()
  // }
}
const router = new Router({
  mode: 'hash',
  scrollBehavior: () => ({
    y: 0
  }),
  isAddDynamicMenuRoutes: false, // 是否已经添加动态(菜单)路由
  routes: globalRoutes.concat(mainRoutes)
})

router.beforeEach((to, from, next) => {
  // let token = Vue.cookie.get('cookie');
  // console.log(token)
  // 添加动态(菜单)路由
  // 1. 已经添加 or 全局路由, 直接访问
  // 2. 获取菜单列表, 添加并保存本地存储
  if (router.options.isAddDynamicMenuRoutes || fnCurrentRouteType(to, globalRoutes) === 'global') {
    next()
  } else {
    http({
      url: "./static/menu.json",
      method: "get",
      data: {},
    }).then((res) => {
      if (res) {
        if (store.state.common.menuList.length == 0) {
          console.log('重新生成动态路由')
          fnAddDynamicMenuRoutes(res.data.menus)
          router.options.isAddDynamicMenuRoutes = true
          store.commit("common/updateMenuList", JSON.parse(JSON.stringify(res.data.menus)));
          next({
            ...to,
            replace: true
          })
        } else {
          next();
        }
      } else {
        router.push({
          name: 'login'
        })
      }
    })
    // .catch(err => {
    //   console.log('拦截服务')
    //   router.push({
    //     name: 'login'
    //   })
    // });
  }
})

/**
 * 判断当前路由类型, global: 全局路由, main: 主入口路由
 * @param {*} route 当前路由
 */
function fnCurrentRouteType(route, globalRoutes = []) {
  var temp = []
  for (var i = 0; i < globalRoutes.length; i++) {
    if (route.path === globalRoutes[i].path) {
      return 'global'
    } else if (globalRoutes[i].children && globalRoutes[i].children.length >= 1) {
      temp = temp.concat(globalRoutes[i].children)
    }
  }
  return temp.length >= 1 ? fnCurrentRouteType(route, temp) : 'index'
}

/**
 * 添加动态(菜单)路由
 * @param {*} menuList 菜单列表
 * @param {*} routes 递归创建的动态(菜单)路由
 */
function fnAddDynamicMenuRoutes(menuList = [], routes = []) {
  var temp = [];
  for (var i = 0; i < menuList.length; i++) {
    if (menuList[i].children && menuList[i].children.length >= 1) {
      temp = temp.concat(menuList[i].children)
    } else if (menuList[i].url && /\S/.test(menuList[i].url)) {
      menuList[i].url = menuList[i].url.replace(/^\//, '')
      var route = {
        path: (menuList[i].url == "#" || menuList[i].url == "") ? '404' : menuList[i].url,
        component: null,
        name: menuList[i].menuName,
        meta: {
          menuId: menuList[i].menuId,
          title: menuList[i].menuName,
          isDynamic: true,
          isTab: true,
          iframeUrl: ''
        }
      }
      // url以http[s]://开头, 通过iframe展示
      if (isURL(menuList[i].url)) {
        route['path'] = `i-${menuList[i].menuId}`
        route['name'] = `i-${menuList[i].menuId}`
        route['meta']['iframeUrl'] = menuList[i].url
      } else {
        try {
          route['component'] = !(menuList[i].url == "#" || menuList[i].url == "") ? _import(`modules/${menuList[i].url}`) : _import('modules/404')
        } catch (e) { }
      }
      routes.push(route)
    }
  }
  if (temp.length >= 1) {
    fnAddDynamicMenuRoutes(temp, routes)
  } else {
    mainRoutes.name = 'main-dynamic'
    mainRoutes.children = routes
    router.$addRoutes(mainRoutes);
    store.commit("common/updateDynamicMenuRoutes", JSON.parse(JSON.stringify(mainRoutes.children)));
  }
}

router.$addRoutes = (params) => {
  router.matcher = new Router({
    mode: 'history',
    scrollBehavior: () => ({
      y: 0
    }),
    isAddDynamicMenuRoutes: false, // 是否已经添加动态(菜单)路由
    routes: globalRoutes.concat(newMainRoutes)
  }).matcher;
  router.addRoutes([
    params,
    {
      path: '*',
      redirect: {
        name: '404'
      }
    }
  ])
}
export default router
