<template>
  <el-submenu style="color: rgb(125, 180, 173);" v-if="menu.children && menu.children.length >= 1"
    :index="menu.menuId + ''" :popper-class="'site-sidebar--' + sidebarLayoutSkin + '-popper'">
    <template slot="title">
      <i style="color: rgb(125, 180, 173);" :class="('fa', menu.icon)" class="site-sidebar__menu-icon"></i>
      <span style="color: rgb(125, 180, 173);" :title="menu.menuName">{{ menu.menuName }}</span>
    </template>
    <sub-menu v-for="item in menu.children" :key="item.menuId" :menu="item" :dynamicMenuRoutes="dynamicMenuRoutes">
    </sub-menu>
  </el-submenu>
  <el-menu-item style="color: rgb(125, 180, 173);" v-else :index="menu.menuId + ''" @click="gotoRouteHandle(menu)">
    <i :class="('fa', menu.icon)" class="site-sidebar__menu-icon"></i>
    <span :title="menu.menuName">{{ menu.menuName }}</span>
  </el-menu-item>
</template>

<script>
import SubMenu from "./sidebar-sub-menu";
export default {
  name: "sub-menu",
  props: {
    menu: {
      type: Object,
      required: true,
    },
    dynamicMenuRoutes: {
      type: Array,
      required: true,
    },
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
  },
  methods: {
    // 通过menuId与动态(菜单)路由进行匹配跳转至指定路由
    gotoRouteHandle(menu) {
      var route = this.dynamicMenuRoutes.filter(
        (item) => item.meta.menuId === menu.menuId
      );
      // debugger;
      if (route.length >= 1) {
        var that = this;
        this.$router.push({ name: route[0].name });
        setTimeout(function () {
          that.$store.commit("common/updateContentIsNeedRefresh", true);
          that.$nextTick(() => {
            that.$store.commit("common/updateContentIsNeedRefresh", false);
          });
        }, 200);
      }
    },
  },
};
</script>
