<template>
    <div class="main-body" style="width: 100%;">
        <div class="main-list">
            3455
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
