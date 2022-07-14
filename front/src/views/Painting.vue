<template>
    <div class="demo-body">
        <div class = "StyleTransfer">
            <div style="margin:30px;" v-for="i in state.styletransfertype.length" :key="i" class="upload-content">
                <div v-html="state.styletransfertype[i-1].desc"></div>
                <div style="display: flex; align-items: center;">
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
                                jpeg/jpg/png files with a size less than 2M
                            </div>
                        </div>
                        
                    </el-upload>
                    <el-image class="add-image" src="../../public/img/static/add.svg" fit="contain" />
                    <div>
                        <el-upload 
                            v-if="state.styletransfertype[i-1].name != 'StyleTransfer_Fast'"
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
                                    jpeg/jpg/png files with a size less than 2M
                                </div>
                            </div>
                        </el-upload>
                        
                        <div v-else style="width:360px; height: 180px; border: 1px dashed #d9d9d9;">
                            <div v-if="!state.styletransfertype[i-1].styleimgurl" class="flex">
                                <select @change="changeimage" v-model="state.styletransfertype[i-1].selectimage">
                                    <option 
                                        v-for="(item, index) in state.styletransfertype[i-1].faststyles"
                                        :value="index">{{item.label}}</option>
                                </select>
                            </div>
                            <div v-else class="el-upload-image flex">
                                <el-image :src="state.styletransfertype[i-1].styleimgurl" :preview-src-list="[state.styletransfertype[i-1].styleimgurl]" fit="contain" ></el-image>
                                <span class="close" @click.prevent.stop="state.styletransfertype[i-1].styleimgurl=''">X</span>
                            </div>
                            
                        </div>
                    </div>
                    <div class="generate-image">
                        <el-image @click="handleMouseClick(i-1)" src="../../public/img/static/equal.svg" fit="contain"/>
                    </div>
                    <div>
                        <el-image style="cursor : pointer; height : 180px;width: 236px;" :src="state.styletransfertype[i-1].resulturl" :preview-src-list="[state.styletransfertype[i-1].resulturl]" fit="contain" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, reactive} from "vue";
import { ElMessage } from "element-plus";
import service from "../utils/https";
import urls from "../utils/urls";
declare let document: Document | any;

export default defineComponent({
    setup(props, context) {
        document.title = "AI Painting";
        document.querySelector("#keywords").setAttribute("content", "风格迁移,A Neural Algorithm of Artistic Style,Universal Style Transfer via Feature Transforms,\
        Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization,Perceptual Losses for Real-Time Style Transfer and Super-Resolution");
        document.querySelector("#description").setAttribute("content", "使用特定模型实现快速风格迁移，使用WCT和Adain方法实现快速风格迁移");
        const state = reactive({
            service: service,
            urls: urls,
            styletransfertype: [
            {
                name: "StyleTransfer_WCT",
                desc: "<div class=\"h2\">StyleTransfer_WCT</div>\
                        <div class=\"content\"><a href=\"https://arxiv.org/abs/1508.06576\">《A Neural Algorithm of Artistic Style》</a>是基于协方差和Gram矩阵的方法能很好的提取视觉风格特征，但缺点是处理时间长。\
                            而<a href=\"https://arxiv.org/abs/1705.08086\">《Universal Style Transfer via Feature Transforms》</a>则通过白化原始图像，再对白化后的图像彩化并循环多次实现快速风格迁移效果。\
                        </div>",
                params:{functionname:"StyleTransfer_WCT", 
                        alpha:1,
                        sourceimgurl:"http://124.223.100.95:9999/img/20220710/bde12f4656700699769080539eb4a37a.jpg",
                        styleimgurl:"http://124.223.100.95:9999/img/20220710/0634a86fb0899a32168c12ffd5eff811.jpg"},
                resulturl:"http://124.223.100.95:9999/img/20220710/db46073544fa2563c66047e0b67d5da2_result.jpg",
            },
            {
                name: "StyleTransfer_AdaIN",
                desc: "<div class=\"h2\">StyleTransfer_AdaIN</div>\
                        <div class=\"content\"><a href=\"https://arxiv.org/abs/1703.06868\">《Arbitrary Style Transfer in Real-time with Adaptive Instance Normalization》<\a>\
                            提出使用风格照片特征空间的均值和方差对原始照片特征空间进行转换，当两者的特征空间对齐时则认为风格相似。\
                        </div>",
                params:{functionname:"StyleTransfer_AdaIN",
                        alpha:1,
                        sourceimgurl:"http://124.223.100.95:9999/img/20220710/22cbb859c931c7e3b109278ee04005df.jpg",
                        styleimgurl:"http://124.223.100.95:9999/img/20220710/3aae758bab2f44a087b4de590e4d1755.jpg"},
                resulturl:"http://124.223.100.95:9999/img/20220710/818fc5ba7817a1f2743b76f2a1798d87_result.jpg",
            },
            {
                name: "StyleTransfer_Fast",
                desc: "<div class=\"h2\">StyleTransfer_Fast</div>\
                        <div class=\"content\"><a href=\"https://arxiv.org/abs/1603.08155\">《Perceptual Losses for Real-Time Style Transfer and Super-Resolution》<\a>\
                            提出使用TransformerNet转换原始图片，转换后的图片通过vgg16提取特征，如果特征与风格图片的特征空间相似，则认为风格相同。因为TransformerNet是预训练网络，所以使用该方法进行风格转换较快。\
                        </div>",
                params:{functionname:"StyleTransfer_Fast",
                        sourceimgurl:"http://124.223.100.95:9999/img/20220710/20f336afe77cd89351a54541080950dd.jpg",
                        faststyle:"faststyle3"},
                resulturl:"http://124.223.100.95:9999/img/20220710/18b0cb426dc304c163d56ab31467c5af_result.jpg",
                faststyles:[
                    {"label":"faststyle1","value":"../../public/img/static/1.jpg"},
                    {"label":"faststyle2","value":"../../public/img/static/2.jpg"},
                    {"label":"faststyle3","value":"../../public/img/static/3.jpeg"},
                    {"label":"faststyle4","value":"../../public/img/static/4.jpg"},
                    {"label":"faststyle5","value":"../../public/img/static/5.jpg"},
                ],
                selectimage: '2',
                styleimgurl: 'http://124.223.100.95:9999/img/20220710/18b0cb426dc304c163d56ab31467c5af_result.jpg',
            }
            ]
        })
        const handleSuccess = (response, file, fileList, index, key) => {
            state.styletransfertype[index].params[key] = response.data
        }

        const beforeUpload = (file) => {
            const isLt2M = file.size / 1024 / 1024 < 2
            if (!isLt2M) {
                ElMessage.error('上传图片大小不能超过2M!可使用画图工具重新调整图片大小')
                return false;
            }
        };

        const handleMouseClick = async (index) => {
            if(state.styletransfertype[index].name !="StyleTransfer_Fast")
            {
                if(!state.styletransfertype[index].params.sourceimgurl || !state.styletransfertype[index].params.styleimgurl) {
                    ElMessage.error("请上传原始图片和风格图片")
                    return
                }
            }
            else
            {
                if(!state.styletransfertype[index].params.sourceimgurl || !state.styletransfertype[index].params.faststyle) {
                    console.log(state.styletransfertype[index])
                    ElMessage.error("请上传原始图片和风格图片")
                    return
                }
            }
            state.styletransfertype[index].resulturl= "../../public/img/static/loading2.gif"
            service.post(urls.styletransfer, state.styletransfertype[index].params).then(response =>{
                state.styletransfertype[index].resulturl = response
            });
        };

        const changeimage = (val) => {
            let index = state.styletransfertype[2].selectimage
            let faststyle = state.styletransfertype[2].faststyles[index].label
            let image = state.styletransfertype[2].faststyles[index].value

            state.styletransfertype[2].styleimgurl = image
            state.styletransfertype[2].params.faststyle = faststyle
        }

        return {
            state,
            handleSuccess,
            beforeUpload,
            handleMouseClick,
            changeimage
        };
    }
})
</script>

<style lang="less">
.demo-body {
    width: 100%;
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
        cursor: pointer;
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
.generate-image {
    cursor: pointer;
    width: 80px;
    text-align: center;
    &:hover .el-image {
        height: 80px;
    }

}
.el-image .el-image__error {
    min-width: 236px !important;
}
.flex {
    display: flex;
    justify-content:center;
    align-items: center;
    height:100%;
    select {
        width: 40%;
        height:36px;
        line-height: 36px;
        color: #303133;
    }
}
</style>
