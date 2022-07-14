<template>
    <div class="main-body" style="width: 100%;">
        <div class="main-list">
            <div class="h2">技术交流加qq群: 386380284</div>
            <div class="h2">广告投放，软文推广加QQ：250316792</div>
        </div>
        <!--<LoadEnd v-if="true"></LoadEnd>-->
    </div>
</template>

<script>
import LoadEnd from "../components/LoadEnd.vue";
export default {
    components: {
    LoadEnd,
  },
}
</script>

<style lang="less">
.main-list {
    min-height:calc(100% - 54px) !important;
}
.h2 {
    border-bottom-color: rgb(238, 238, 238);
    border-bottom-style: solid;
    border-bottom-width: 1px;
    box-sizing: border-box;
    color: rgb(51, 51, 51);
    display: block;
    font-family: "Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif;
    font-size: 28px;
    font-weight: 700;
    line-height: 34.3px;
    margin-block-end: 15px;
    margin-block-start: 15px;
    margin-bottom: 15px;
    margin-inline-end: 0px;
    margin-inline-start: 0px;
    margin-top: 15px;
    overflow-wrap: break-word;
    padding-bottom: 8.4px;
    text-align: left;
    text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
}
</style>
