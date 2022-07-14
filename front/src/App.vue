<template>
  <div class="container">
    <Nav v-if="state.isShowNav" />
    <div class="showdemo">
        <el-carousel :interval="4000" type="card" height="300px">
            <el-carousel-item v-for="(item, index) in state.showimagelist" :key="index" style="height: 300px;">
                <el-image class="ad-image"  :src="item" fit="contain"></el-image>
            </el-carousel-item>
        </el-carousel>
    </div>
    <div class="layout">
      <div class="layout-body">
        <router-view />
        <CustomSlider v-if="state.isShowSlider"></CustomSlider>
      </div>  
      <Footer v-if="state.isShowNav"></Footer>
    </div>
    <!--<ArrowUp></ArrowUp>-->
    <!--<Footer v-if="state.isShowNav"></Footer>-->
  </div>
</template>

<script lang="ts">
import { defineComponent, defineAsyncComponent, reactive, onMounted } from "vue";
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router';
import { isMobileOrPc } from "./utils/utils";

// 移动端 rem 单位适配
if (isMobileOrPc()) {
  // width * 100 / 750 = width / 7.5
  // 1rem = 100px
  var width = window.screen.width;
  window.document.getElementsByTagName("html")[0].style.fontSize =
    width / 7.5 + "px";
}

export default defineComponent({
  name: "App",
  components: {
    Nav: defineAsyncComponent(() => import("./components/Nav.vue")),
    CustomSlider: defineAsyncComponent(
      () => import("./components/CustomSlider.vue")
    ),
    Footer: defineAsyncComponent(() => import("./components/Footer.vue")),
    ArrowUp: defineAsyncComponent(() => import("./components/Footer.vue")),
  },
  watch: {
    $route: function (val: any, oldVal: any) {
      this.routeChange(val, oldVal);
    },
  },
  setup() {
    const state = reactive({
      isShowNav: false,
      isShowSlider: false,
      showimagelist: [
        "../../public/img/static/5ea53e0ee5178018ccb5df95ec05affb_result.jpg",
        "../../public/img/static/5833d4171206d28bd37050011c8dc0be_result.jpg",
        "../../public/img/static/6a0a92a0872bb8ac4ccebb7b2121341d_result.jpg",
        "../../public/img/static/bb637ee9851ef88534a9d078b0d2150e_result.jpg"
    ]
    });

    // const router = useRouter();
    const route = useRoute();

    const routeChange = (val: any, oldVal: any): void => {
      const referrer: any = document.getElementById("referrer");
      
      if (val.path === "/") {
        state.isShowNav = false;
        referrer.setAttribute("content", "always");
      } else {
        state.isShowNav = true;
        referrer.setAttribute("content", "never");
      }
      const navs = [
        "/articles",
        // "/archive",
        // "/archive",
        // "/project",
        // "/timeline",
        "/message",
      ];
      if (navs.includes(val.path)) {
        state.isShowSlider = true;
      } else {
        state.isShowSlider = false;
      }
      if (isMobileOrPc()) {
        state.isShowSlider = false;
      }
    };

    onMounted(() => {
        routeChange(route, route);
    })

    return {
      state,
      routeChange,
    };
  },
});
</script>

<style lang="less">
@import url("./less/monokai_sublime.less");
@import url("./less/index.less");
@import url("./less/mobile.less");
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  // width: 1200px;
  padding-top: 61px;
}
img {
  vertical-align: bottom;
}
.showdemo {
    width: 100%;
    margin: 0px auto;
}
.el-carousel .el-carousel--horizontal .el-carousel--card {
    position: absolute;
    display: flex;
    width: 750px;
    height: 330px;
    margin: 0 auto;
}
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
  text-align: center;
}
.el-carousel__item  {
    //border: 1px solid #dedede;
    //border-radius:10px;
    overflow: hidden;
    &:not-child(2n+1) {
        //background-color: rgba(#fff, 0.0);
    }
}
.ad-image {
    width: 100%;
    height: 100%;
}
.el-image .el-image__error {
    min-width: 236px !important;
}
</style>
