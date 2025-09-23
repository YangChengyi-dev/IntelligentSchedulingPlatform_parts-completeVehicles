<!--  -->
<template>
    <div class="dialogDiv">
        <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
            append-to-body :lock-scroll="false" @destroy-on-close="true">
            <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
                <el-form-item class="form-item" label="日志序号:" prop="detailTitle">
                    <el-input v-model="form.detailTitle" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="任务名称:" prop="detailOperName">
                    <el-input v-model="form.detailOperName" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="任务分组:" prop="detailOperUrl">
                    <el-input v-model="form.detailOperUrl" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="调用目标字符串:" prop="detailRequestMethod">
                    <el-input v-model="form.detailRequestMethod" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="执行表达式:" prop="operParam">
                    <el-input v-model="form.operParam" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="下次执行时间:" prop="jsonResult">
                    <el-input v-model="form.jsonResult" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="执行策略:" prop="detailMethod">
                    <el-input v-model="form.detailMethod" :disabled="true"></el-input>
                </el-form-item>

                <el-form-item class="form-item" label="并发执行:" prop="status">
                    <el-tag effect="dark" type="">{{form.statusTag}}</el-tag>
                </el-form-item>
                <el-form-item class="form-item" label="执行状态:" prop="errorMsg" v-show="form.statusTag=='异常'">
                    <el-input type="input" v-model="form.errorMsg" :disabled="true"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer" v-if="!isDetail">
                <el-button class="" @click="open = false">取消</el-button>
                <el-button class="" type="primary" @click="submitForm('form')">保存</el-button>
            </div>
        </el-dialog>
    </div>
</template>
  
<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';

export default {
    //import引入的组件需要注入到对象中才能使用
    components: {},
    props: ["title", "width", "isDetail"],
    data() {
        //这里存放数据
        return {
            // 是否显示弹出层
            open: false,
            form: {
                jobId: "",
                detailTitle: "",
                detailOperName: "",
                detailRequestMethod: "",
                detailMethod: "",
                operParam: "",
                detailOperUrl: "",
                jsonResult: "",
                statusTag: '正常',
                errorMsg: '',
            },
            rules: {
                detailTitle: [{ required: true, message: "操作模块不能为空", trigger: "blur" }],
                detailOperName: [
                    { required: true, message: "登录信息不能为空", trigger: "blur" },
                ],
                detailOperUrl: [{ required: true, message: "请求地址不能为空", trigger: "blur" }],
            },

            status: '',
            rowData: {},
        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
        // 修改
        editFun(data, status) {
            this.open = true;
            this.status = status;
            this.rowData = data;
            this.$nextTick(() => {
                // 表单重置
                this.$refs["form"].resetFields();

                if (data) {
                    this.$http({
                        url: this.$http.adornUrl(`/monitor/job/detail/${data.jobLogId?data.jobLogId:data.jobId}`),
                        method: "get",
                        params: this.$http.adornParams({})
                    }).then((res) => {
                        if (res.data) {
                            let operLog = res.data.job,
                                form = this.form;
                            form.jobId = operLog.jobId;
                            form.detailTitle = operLog.jobId;

                            form.detailOperName = `${operLog.jobName}`,
                                form.detailOperUrl = operLog.jobGroup,
                                form.detailRequestMethod = operLog.invokeTarget,
                                form.operParam = operLog.cronExpression,
                                form.jsonResult = operLog.nextValidTime,

                                form.statusTag = (operLog.concurrent == 0 ? '允许' : '禁止'),
                                form.errorMsg = operLog.status == '0' ? '正常' : '暂停'
                            switch (operLog.misfirePolicy) {
                                case "0":
                                    form.detailMethod = "默认策略";
                                    break;
                                case "1":
                                    form.detailMethod = "立即执行";
                                    break;
                                case "2":
                                    form.detailMethod = "执行一次";
                                    break;
                                case "3":
                                    form.detailMethod = "放弃执行";
                                    break;
                            }
                        }
                    });
                }
            });
        },
    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() { },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() { },
    beforeCreate() { }, //生命周期 - 创建之前
    beforeMount() { }, //生命周期 - 挂载之前
    beforeUpdate() { }, //生命周期 - 更新之前
    updated() { }, //生命周期 - 更新之后
    beforeDestroy() { }, //生命周期 - 销毁之前
    destroyed() { }, //生命周期 - 销毁完成
    activated() { }, //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
<style scoped>
/* @import url(); 引入公共css类 */
/* .dialog >>> .el-dialog {
          height: v-bind(height) !important;
        } */
.dialog>>>.el-dialog {
    max-height: 77%;
}

#form {
    padding: 0 70px;
}

#form>>>.el-form-item__label {
    width: 30% !important;
}

.el-form-item {
    width: 100%;
    align-items: flex-start !important;
}

#form>>>.el-form-item__content {
    margin-left: 10px !important;
    width: 90% !important;
}
</style>
  