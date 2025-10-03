<template>
  <div
    class="site-wrapper"
    :class="{ 'site-sidebar--fold': sidebarFold }"
    v-loading.fullscreen.lock="loading"
    element-loading-text="拼命加载中"
  >
    <template v-if="!loading">
      <main-navbar />
      <main-sidebar />
      <div
        class="site-content__wrapper"
        :style="{ 'min-height': documentClientHeight + 'px' }"
      >
        <main-content v-if="!$store.state.common.contentIsNeedRefresh" />
      </div>
    </template>
  </div>
</template>

<script>
import { mapMutations } from "vuex";
import MainNavbar from "./navbar";
import MainSidebar from "./sidebar";
import MainContent from "./content";
export default {
  provide() {
    return {
      // 刷新
      refresh: this.refresh
    };
  },
  data() {
    return {
      loading: true
    };
  },
  components: {
    MainNavbar,
    MainSidebar,
    MainContent
  },
  computed: {
    documentClientHeight: {
      get() {
        return this.$store.state.common.documentClientHeight;
      },
      set(val) {
        this.$store.commit("common/updateDocumentClientHeight", val);
      }
    },
    sidebarFold: {
      get() {
        return this.$store.state.common.sidebarFold;
      }
    }
  },
  created() {
    this.getUserInfo();
  },
  mounted() {
    this.resetDocumentClientHeight();
  },
  methods: {
    refresh() {
      this.getUserInfo();
      this.$store.commit("common/updateContentIsNeedRefresh", true);
      this.$nextTick(() => {
        this.$store.commit("common/updateContentIsNeedRefresh", false);
      });
    },
    // 重置窗口可视高度
    resetDocumentClientHeight() {
      this.documentClientHeight = document.documentElement["clientHeight"];
      window.onresize = () => {
        this.documentClientHeight = document.documentElement["clientHeight"];
      };
    },
    ...mapMutations({
      getUser: "user/updateUser"
    }),
    // 获取当前管理员信息
    getUserInfo() {
      // 由于API调用被注释，直接设置loading为false以显示页面内容
      this.loading = false;
      
      // 注释掉的API调用部分
      // this.$http({
      //   url: this.$http.adornUrl(`/index`),
      //   method: "get",
      //   params: this.$http.adornParams({
      //   }),
      // }).then((res) => {
      //   this.loading = false;
      //   if (res.data.user) {
      //     this.getUser(res.data.user);
      //   } else {
      //     this.$router.replace({
      //       name: 'login'
      //     })
      //   }
      // }).catch(err => {
      //   this.$router.replace({
      //     name: 'login'
      //   })
      // });
      this.loading = false;
    }
  }
};
</script>
