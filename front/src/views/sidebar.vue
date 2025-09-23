<template>
  <aside class="site-sidebar" :class="'site-sidebar--' + sidebarLayoutSkin">
    <div class="site-sidebar__inner">
      <el-menu :default-active="menuActiveName || 'home'" :collapse="sidebarFold" :collapseTransition="false"
        class="site-sidebar__menu">
        <div class="img">
          <img :src="imgAvator" onerror="javascript:this.src='/static/img/profile2.jpg'" />
          <div class="loginName" v-if="!sidebarFold">
            管理员
            <div class="sta">
              <div class="status online">
                <div></div>
                <span>在线</span>
              </div>
              <div class="status">
                <icon-svg name="reload" class="site-sidebar__menu-icon"></icon-svg>
                <span>注销</span>
              </div>
            </div>
          </div>
        </div>
        <template v-if="!isHorizontal">
          <!-- <el-menu-item index="home" @click="$router.push({ name: 'home' })">
            <icon-svg name="shouye" class="site-sidebar__menu-icon"></icon-svg>
            <span slot="title">首页</span>
          </el-menu-item> -->

          <sub-menu v-for="menu in menuList" :key="menu.menuId" :menu="menu" :dynamicMenuRoutes="dynamicMenuRoutes">
          </sub-menu>
        </template>
      </el-menu>
    </div>
  </aside>
</template>

<script>
import SubMenu from "./sidebar-sub-menu";
import { isURL } from "@/utils/validate";

import imgAvator from '@@/img/profile2.jpg'

export default {
  data() {
    return {
      dynamicMenuRoutes: [],
      imgAvator: imgAvator
    };
  },
  components: {
    SubMenu,
  },
  computed: {
    sidebarLayoutSkin: {
      get() {
        return this.$store.state.common.sidebarLayoutSkin;
      },
    },
    sidebarFold: {
      get() {
        return this.$store.state.common.sidebarFold;
      },
    },
    updateMenuList: {
      get() {
        return this.$store.state.common.menuList;
      },
    },
    menuActiveName: {
      get() {
        return this.$store.state.common.menuActiveName;
      },
      set(val) {
        this.$store.commit("common/updateMenuActiveName", val);
      },
    },
    mainTabs: {
      get() {
        return this.$store.state.common.mainTabs;
      },
      set(val) {
        this.$store.commit("common/updateMainTabs", val);
      },
    },
    mainTabsActiveName: {
      get() {
        return this.$store.state.common.mainTabsActiveName;
      },
      set(val) {
        this.$store.commit("common/updateMainTabsActiveName", val);
      },
    },

    isHorizontal: {
      get() {
        return this.$store.state.common.isHorizontal;
      },
    },

    avatar: {
      get() {
        return "../../static/img/profile.jpg";
      },
    },
    loginName: {
      get() {
        return this.$store.state.user.user.loginName;
      },
    },
  },
  watch: {
    $route: "routeHandle",
  },
  created() {
    this.menuList = this.updateMenuList;
    this.dynamicMenuRoutes = this.$store.state.common.dynamicMenuRoutes;
    this.routeHandle(this.$route);
  },
  methods: {
    // 路由操作
    routeHandle(route) {
      if (route.meta.isTab) {
        // tab选中, 不存在先添加
        var tab = this.mainTabs.filter((item) => item.name === route.name)[0];
        if (!tab) {
          if (route.meta.isDynamic) {
            route = this.dynamicMenuRoutes.filter((item) => item.name === route.name)[0];
            if (!route) {
              return console.error("未能找到可用标签页!");
            }
          }
          tab = {
            menuId: route.meta.menuId || route.name,
            name: route.name,
            title: route.meta.title,
            type: isURL(route.meta.iframeUrl) ? "iframe" : "module",
            iframeUrl: route.meta.iframeUrl || "",
            params: route.params,
            query: route.query,
          };
          this.mainTabs = this.mainTabs.concat(tab);
        }
        this.menuActiveName = tab.menuId + "";
        this.mainTabsActiveName = tab.name;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.img {
  display: flex;
  align-items: center;
  // width: 50px;
  // height: 50px;
  padding: 4px;

  img {
    width: 55px;
    height: 55px;
    border-radius: 50%;
  }

  .loginName {
    padding-left: 10px;

    .sta {
      display: flex;
      margin-top: 10px;

      .status {
        display: flex;
        align-items: center;
      }

      .online {
        margin-right: 10px;

        div {
          width: 10px;
          height: 10px;
          // background: #115895;
          background: #4ea9f8;
          border-radius: 50%;
          margin-right: 5px;
        }
      }

      .icon-svg {
        width: 12px;
        height: 12px;
      }
    }
  }
}
</style>
