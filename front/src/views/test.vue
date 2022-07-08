<template>
    <div class="demo-body">
        <div class="showdemo">
            <el-carousel :interval="4000" type="card" height="300px">
                <el-carousel-item v-for="item in 6" :key="item">
                    <h3 text="2xl" justify="center"></h3>
                </el-carousel-item>
            </el-carousel>
        </div>
        <div class = "StyleTransfer">
            <div v-for="i in state.styletransfertype.length" :key="i" class="upload-content">
                <div class="h2">{{state.styletransfertype[i-1].name}}</div>
                <div class="content">{{state.styletransfertype[i-1].desc}}</div>
                <div style="display: flex;">
                    <el-upload
                        class="upload-demo"
                        drag
                        accept=".jpeg,.jpg,.png"
                        :before-upload="beforeUpload"
                        :action="`${state.service.defaults.baseURL}${state.urls.uploadfile}`"
                        :on-success="
                            (response, file, fileList) => {
                            return handleSuccess(response, file, fileList, i-1, 'sourceimgurl');
                            }
                        "
                        :show-file-list="false"
                    >
                        <div v-if="state.styletransfertype[i-1].params.sourceimgurl" class="el-upload-image">
                           <el-image  :src="state.styletransfertype[i-1].params.sourceimgurl" fit="contain" ></el-image>
                           <span class="close" @click.prevent.stop="state.styletransfertype[i-1].params.sourceimgurl=null">X</span>
                        </div>
                       
                        <div v-else class="el-upload_empty-views">
                            <div class="el-upload__text">
                                Drop file here or <em>click to upload</em>
                            </div>
                            
                            <div class="el-upload__tip">
                                jpeg/jpg/png files with a size less than 500kb
                            </div>
                        </div>
                        
                    </el-upload>
                    <el-image style="height : 90px;" src="../../public/img/add.svg" fit="contain" />
                    <el-upload
                        class="upload-demo"
                        drag
                        accept=".jpeg,.jpg,.png"
                        :before-upload="beforeUpload"
                        :action="`${state.service.defaults.baseURL}${state.urls.uploadfile}`"
                        :on-success="
                            (response, file, fileList) => {
                            return handleSuccess(response, file, fileList, i-1, 'styleimgurl');
                            }
                        "
                        :show-file-list="false"
                    >
                        <div v-if="state.styletransfertype[i-1].params.styleimgurl" class="el-upload-image">
                           <el-image  :src="state.styletransfertype[i-1].params.styleimgurl" fit="contain" ></el-image>
                           <span class="close" @click.prevent.stop="state.styletransfertype[i-1].params.styleimgurl=null">X</span>
                        </div>
                       
                        <div v-else class="el-upload_empty-views">
                            <div class="el-upload__text">
                                Drop file here or <em>click to upload</em>
                            </div>
                            
                            <div class="el-upload__tip">
                                jpeg/jpg/png files with a size less than 500kb
                            </div>
                        </div>
                    </el-upload>
                </div>
                <div style="height : 200px;">
                    <el-image style="cursor : pointer;" @mousedown="handleMouseDown(i-1)" @mouseup="handleMouseUp(i-1)" @mouseleave="handleMouseLeave(i-1)" :src="state.styletransfertype[i-1].downarrow" fit="contain"/>
                </div>
                <div style="margin-bottom:30px;"><el-image :src="state.styletransfertype[i-1].resulturl" :preview-src-list="srcList" :initial-index="0" fit="contain" /></div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, reactive} from "vue";
import { ElMessage } from "element-plus";
import service from "../utils/https";
import urls from "../utils/urls";
const srcList = [
  'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg']
export default defineComponent({
    name: 'test',
    setup(props, context) {
        const state = reactive({
            service: service,
            urls: urls,
            styletransfertype: [
            {
                downarrow: "../../public/img/downarrow.svg",
                name: "styletransfer1标题",
                desc: "styletransfer1简单介绍",
                params:{functionname:"StyleTransfer_WCT", 
                        alpha:1,
                        sourceimgurl:"http://124.223.100.95:9999/img/aae6f4fbacd61507c11794cb3d3215c2.jpg",
                        styleimgurl:"http://124.223.100.95:9999/img/c9aefd196664b49e25c90a57724d8f7f.jpg"},
                resulturl:"http://124.223.100.95:9999/img/6b9ed12ddd1cb45f2c7e39d4ff13ff85_result.jpg",
            },
            {
                downarrow: "../../public/img/downarrow.svg",
                name: "styletransfer2标题",
                desc: "styletransfer2简单介绍",
                params:{functionname:"StyleTransfer_AdaIN",
                        alpha:1,
                        sourceimgurl:"",
                        styleimgurl:""},
                resulturl:"",
            }
            ]
        })
        const handleSuccess = (response, file, fileList, index, key) => {
            state.styletransfertype[index].params[key] = response.data
            // state.styletransfertype[index].params = {
            //     ...state.styletransfertype[index].params,
            //     [key]: response.data
            // }
        }

        const beforeUpload = (file) => {
            const isLt2M = file.size / 1024 / 1024 < 2
            if (!isLt2M) {
                ElMessage.error('上传图片大小不能超过2M!可使用画图工具重新调整图片大小')
                return false;
            }
        };

        const handleMouseDown = (index) => {
            state.styletransfertype[index].downarrow = "../../public/img/smalldownarrow.svg"
        };

        const handleMouseUp = async (index) => {
            if(!state.styletransfertype[index].params.styleimgurl || !state.styletransfertype[index].params.sourceimgurl) {
                ElMessage.error("请上传原始图片和风格图片")
                return
            }
            state.styletransfertype[index].downarrow = "../../public/img/downarrow.svg"
            state.styletransfertype[index].resulturl= "../../public/img/loading2.gif"
            service.post(urls.styletransfer, state.styletransfertype[index].params).then(response =>{
                state.styletransfertype[index].resulturl = response
            });
        };

        const handleMouseLeave = async (index) => {
            state.styletransfertype[index].downarrow = "../../public/img/downarrow.svg"
        };

        return {
            state,
            handleSuccess,
            beforeUpload,
            handleMouseDown,
            handleMouseUp,
            handleMouseLeave
        };
    }
})
</script>

<style scoped lang="less">
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

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
.demo-body {
    width: 100%;
}
.showdemo {
    width: 100%;
    margin: 0px auto;
}
.StyleTransfer {
    .upload-content {
        // display: flex;
        height: fit-content;
    }
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
.content{
    box-sizing: border-box;
    color: rgb(51, 51, 51);
    display: block;
    font-family: "Helvetica Neue", Helvetica, "Segoe UI", Arial, freesans, sans-serif;
    font-size: 16px;
    line-height: 25.6px;
    margin-block-end: 16px;
    margin-block-start: 0px;
    margin-bottom: 16px;
    margin-inline-end: 0px;
    margin-inline-start: 0px;
    margin-top: 0px;
    overflow-wrap: break-word;
    text-align: left;
    text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
}

.el-upload-list__item-custom:not-child(1) {
    float: right;
}
.el-upload_empty-views {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    height: 180px;
    .el-upload__tip {
        margin-top: 15px;
        color: #90939a;
    }
}
.el-upload-image {
    position: relative;
    .el-image {
        height: 180px;
    }
    .close{
        display: inline-block;
        width: 30px;
        height: 30px;
        text-align:center;
        line-height:30px;
        border-radius: 15px;
        font-size: 16px;
        position: absolute;
        right: 5px;
        top: 5px;
        color: white;
        background-color: rgba( #dedede, 0.5);
    }
}
</style>
