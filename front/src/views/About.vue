<template>
    <div class="main-body" style="width: 100%;">
        <div class="main-list">
            技术交流加qq群: 386380284
        </div>
        <LoadEnd v-if="true"></LoadEnd>
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
</style>
