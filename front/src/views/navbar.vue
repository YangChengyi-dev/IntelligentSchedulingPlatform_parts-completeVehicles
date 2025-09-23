<template>
  <nav class="site-navbar" :class="'site-navbar--' + navbarLayoutType">
    <div class="site-navbar__header">
      <h1 class="site-navbar__brand" @click="$router.push({ name: 'home' })">
        <a
          class="site-navbar__brand-lg"
          style="font-size: 16px;"
          href="javascript:;"
        >
          <div
            style="position: absolute;height: 50px;
    width:220px;left:2%"
          >
            <p style="position: relative;left:0%;top:-20%;">
              基于多式联运的零件与整车
            </p>
            <p style="position: absolute;left:32%;top:25%;">
              智能调度平台
            </p>
          </div>
        </a>
        <a class="site-navbar__brand-mini" href="javascript:;">智能调度</a>
      </h1>
    </div>
    <div class="site-navbar__body clearfix">
      <!-- 折叠，横向菜单 -->
      <el-menu
        :default-active="menuActiveName || 'home'"
        class="site-navbar__menu "
        id="cjMenu"
        mode="horizontal"
        background-color="#113c38"
        text-color="#c5cbcf"
        active-text-color="#e8eaec"
      >
        <!-- 折叠-->
        <el-menu-item
          class="site-navbar__switch"
          index="0"
          @click="sidebarFold = !sidebarFold"
        >
          <icon-svg id="svgIcon" name="zhedie"></icon-svg>
        </el-menu-item>
        <!-- 横向菜单 -->
        <template v-if="isHorizontal">
          <el-menu-item
            index="home"
            @click="
              $router.push({ path: '/index/chargeOperation/overview/overview' })
            "
          >
            <icon-svg name="shouye" class="site-sidebar__menu-icon"></icon-svg>
            <span slot="title">总览</span>
          </el-menu-item>
          <template
            v-for="(menu, index) in menuList"
            v-if="
              index >= currentTabIndex &&
                currentTabIndex + showMenuCount > index
            "
          >
            <el-submenu
              v-if="menu.children && menu.children.length >= 1"
              :index="menu.menuId + ''"
            >
              <template slot="title">
                <i
                  :class="('fa', menu.icon)"
                  class="site-sidebar__menu-icon"
                ></i>
                <span :title="menu.menuName">{{ menu.menuName }}</span>
              </template>
              <sub-menu
                v-for="menus in menu.children"
                :key="menus.menuId"
                :menu="menus"
                :dynamicMenuRoutes="dynamicMenuRoutes"
              >
              </sub-menu>
            </el-submenu>
          </template>
          <div class="right">
            <el-button
              type="primary"
              size="mini"
              icon="el-icon-caret-left"
              :disabled="isLeftClick"
              @click="menuleft"
            ></el-button>

            <el-button
              type="primary"
              size="mini"
              icon="el-icon-caret-right"
              :disabled="isClick"
              @click="menuright"
            ></el-button>
          </div>
        </template>
      </el-menu>
      <!-- 全屏显示 个人中心 -->
      <el-menu
        class="site-navbar__menu site-navbar__menu--right"
        mode="horizontal"
      >
        <el-menu-item
          index="1"
          @click="$router.push({ name: 'theme' })"
          style="display: none"
        >
          <template slot="title">
            <el-badge>
              <icon-svg
                id="svgIcon"
                name="shezhi"
                class="el-icon-setting"
              ></icon-svg>
            </el-badge>
          </template>
        </el-menu-item>
        <el-menu-item index="1" @click="fullScreen">
          <template slot="title">
            <icon-svg
              id="svgIcon"
              name="fullpage"
              class="el-icon-setting"
            ></icon-svg>
            <span>全屏显示</span>
          </template>
        </el-menu-item>
        <el-menu-item class="site-navbar__avatar" index="3">
          <el-dropdown :show-timeout="0" placement="bottom">
            <span class="el-dropdown-link">
              <img
                :src="imgAvator"
                onerror="javascript:this.src='/static/img/profile2.jpg'"
                :alt="userName"
              />{{ userName }}
            </span>
            <el-dropdown-menu slot="dropdown" class="cjDropdown">
              <el-dropdown-item @click.native="updatePasswordHandle()">
                修改密码
              </el-dropdown-item>
              <el-dropdown-item @click.native="changeMenu()">
                切换菜单
              </el-dropdown-item>
              <el-dropdown-item @click.native="logoutHandle()"
                >退出</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </el-menu-item>
      </el-menu>
    </div>
    <!-- 弹窗, 修改密码 -->
    <update-password
      v-if="updatePassowrdVisible"
      ref="updatePassowrd"
    ></update-password>
  </nav>
</template>

<script>
import { mapMutations } from "vuex";
import UpdatePassword from "./navbar-update-password";
import SubMenu from "./sidebar-sub-menu";
import { clearLoginInfo } from "@/utils";
import { isURL } from "@/utils/validate";

import imgAvator from "@@/img/profile2.jpg";
export default {
  data() {
    return {
      updatePassowrdVisible: false,
      currentTabIndex: 0,
      showMenuCount: 5, //横向菜单显示个数
      isLeftClick: true, //左按钮是否禁止点击
      isClick: false, //右按钮是否禁止点击

      imgAvator: imgAvator
    };
  },
  components: {
    UpdatePassword,
    SubMenu
  },
  watch: {
    $route: "routeHandle"
  },
  computed: {
    navbarLayoutType: {
      get() {
        return this.$store.state.common.navbarLayoutType;
      }
    },
    sidebarFold: {
      get() {
        return this.$store.state.common.sidebarFold;
      },
      set(val) {
        this.$store.commit("common/updateSidebarFold", val);
      }
    },
    mainTabs: {
      get() {
        return this.$store.state.common.mainTabs;
      },
      set(val) {
        this.$store.commit("common/updateMainTabs", val);
      }
    },
    userName: {
      get() {
        return this.$store.state.user.user.userName;
      }
    },
    avatar: {
      get() {
        return "../../static/img/profile.jpg";
      }
    },
    isHorizontal: {
      get() {
        return this.$store.state.common.isHorizontal;
      }
    },
    updateMenuList: {
      get() {
        return this.$store.state.common.menuList;
      }
    },
    menuActiveName: {
      get() {
        return this.$store.state.common.menuActiveName;
      },
      set(val) {
        this.$store.commit("common/updateMenuActiveName", val);
      }
    },
    mainTabs: {
      get() {
        return this.$store.state.common.mainTabs;
      },
      set(val) {
        this.$store.commit("common/updateMainTabs", val);
      }
    },
    mainTabsActiveName: {
      get() {
        return this.$store.state.common.mainTabsActiveName;
      },
      set(val) {
        this.$store.commit("common/updateMainTabsActiveName", val);
      }
    },
    sidebarLayoutSkin: {
      get() {
        return this.$store.state.common.sidebarLayoutSkin;
      }
    }
  },
  created() {
    this.menuList = this.updateMenuList;
    this.dynamicMenuRoutes = this.$store.state.common.dynamicMenuRoutes;
    this.routeHandle(this.$route);
  },
  methods: {
    // 修改密码
    updatePasswordHandle() {
      this.updatePassowrdVisible = true;
      this.$nextTick(() => {
        this.$refs.updatePassowrd.init();
      });
    },
    // 退出
    logoutHandle() {
      this.$confirm(`确定进行[退出]操作?`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          this.$router.replace({
            name: "login"
          });
        })
        .catch(() => {});
    },
    ...mapMutations({ updateIsHorizontal: "common/updateIsHorizontal" }),
    // 切换菜单
    changeMenu() {
      this.$confirm(`确定切换菜单?`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(res => {
          this.updateIsHorizontal(!this.isHorizontal);
        })
        .catch(err => {
          this.$message(err);
        });
    },

    // 全屏显示
    fullScreen() {
      var de = document.documentElement;
      if (de.requestFullscreen) {
        de.requestFullscreen();
      } else if (de.mozRequestFullScreen) {
        de.mozRequestFullScreen();
      } else if (de.webkitRequestFullScreen) {
        de.webkitRequestFullScreen();
      }
    },

    // 路由操作
    routeHandle(route) {
      if (route.meta.isTab) {
        // tab选中, 不存在先添加
        var tab = this.mainTabs.filter(item => item.name === route.name)[0];
        if (!tab) {
          if (route.meta.isDynamic) {
            route = this.dynamicMenuRoutes.filter(
              item => item.name === route.name
            )[0];
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
            query: route.query
          };
          this.mainTabs = this.mainTabs.concat(tab);
        }
        this.menuActiveName = tab.menuId + "";
        this.mainTabsActiveName = tab.name;
      }
    },

    menuleft() {
      if (this.currentTabIndex > 1) {
        this.isLeftClick = false;
      } else {
        this.isLeftClick = true;
      }
      this.isClick = false;
      this.currentTabIndex = this.currentTabIndex - 1;
    },
    menuright() {
      this.currentTabIndex = this.currentTabIndex + 1;
      if (
        this.menuList.length - this.showMenuCount <
        this.currentTabIndex + 1
      ) {
        this.isClick = true;
      } else {
        this.isClick = false;
      }
      this.isLeftClick = false;
    }
  }
};
</script>

<style lang="scss" scoped>
.text-wrapper {
  word-break: break-all;
  word-wrap: break-word;
  white-space: pre-wrap;
}
.el-dropdown-link {
  color: #fff;

  img {
    display: inline-block;
  }
}

.quanping {
  width: 1.5em;
  height: 1.5em;
}

.el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
  color: #fff;
}

.el-menu--horizontal > .el-menu-item,
.el-menu--horizontal > .el-menu-item.is-active {
  color: #d8dadd;
}

#cjMenu {
  width: 80%;
  position: relative;
  display: flex;
  flex-wrap: nowrap;
  align-items: center;

  .right {
    position: absolute;
    right: 0;
  }
}

.cjDropdown {
  background: rgb(10, 82, 65);
  border: 1px solid rgb(10, 82, 65);
  // background-color: #1f756c;
  // background: rgb(11, 214, 225);
  // border: 1px solid rgb(11, 214, 225);

  li {
    color: #fff;
  }
}
</style>
