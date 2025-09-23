<!--  -->
<template>
    <div class="dialogDiv">
        <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
            append-to-body :lock-scroll="false" @destroy-on-close="true">
            <el-form :model="form" :rules="rules" ref="form" class="demo-form" id="form">
                <el-form-item class="form-item" label="字典标签:" prop="dictLabel">
                    <el-input v-model="form.dictLabel"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="字典键值:" prop="dictValue">
                    <el-input v-model="form.dictValue"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="字典类型:" prop="dictType">
                    <el-input v-model="form.dictType" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="样式属性:" prop="cssClass">
                    <el-input v-model="form.cssClass"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="字典排序:" prop="dictSort">
                    <el-input v-model="form.dictSort"></el-input>
                </el-form-item>
                <el-form-item class="form-item" label="回显样式:" prop="listClass">
                    <el-select v-model="form.listClass" placeholder="请选择">
                        <el-option label="默认" value="default"> </el-option>
                        <el-option label="主要" value="primary"> </el-option>
                        <el-option label="成功" value="success"> </el-option>
                        <el-option label="信息" value="info"> </el-option>
                        <el-option label="警告" value="warning"> </el-option>
                        <el-option label="危险" value="danger"> </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item class="form-item" label="系统默认:" prop="isDefault">
                    <template>
                        <el-radio v-for="(item,index) in isDefaultArr" :key="index" v-model="form.isDefault"
                            :label="item.dictValue">{{item.dictLabel}}</el-radio>
                    </template>
                </el-form-item>
                <el-form-item class="form-item" label="状态:" prop="status">
                    <template>
                        <el-radio v-for="(item,index) in statusArr" :key="index" v-model="form.status"
                            :label="item.dictValue">
                            {{item.dictLabel}}</el-radio>
                    </template>
                </el-form-item>
                <el-form-item class="form-item" label="备注:" prop="remark">
                    <el-input type="textarea" v-model="form.remark"></el-input>
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
                dictCode: "",
                dictLabel: "",
                dictValue: "",
                dictType: "",
                cssClass: "",
                dictSort: "",
                listClass: "",
                isDefault: "Y",
                status: "0",
                remark: "",
            },
            rules: {
                dictLabel: [{ required: true, message: "字典标签不能为空", trigger: "blur" }],
                dictValue: [{ required: true, message: "字典键值不能为空", trigger: "blur" }],
                dictSort: [{ required: true, message: "字典排序不能为空", trigger: "blur" }],
            },

            status: '',

            isDefaultArr: [],
            statusArr: [],
        };
    },
    //监听属性 类似于data概念
    computed: {},
    //监控data中的数据变化
    watch: {},
    //方法集合
    methods: {
        // 窗口初始化方法，nextTick方法可以添加逻辑，如打开窗口时查询数据填充
        addFun(tableRadio, status) {
            this.open = true;
            this.status = status;
            this.form.dictType = tableRadio;
            this.$nextTick(() => {
                // 表单重置
                this.$refs["form"].resetFields();
            });
        },

        editFun(data, status) {
            this.open = true;
            this.status = status;
            this.$nextTick(() => {
                // 表单重置
                this.$refs["form"].resetFields();

                if (data) {
                    this.$http({
                        url: this.$http.adornUrl(`/system/dict/data/edit/${data.dictCode}`),
                        method: "get",
                        params: this.$http.adornParams({})
                    }).then((res) => {
                        if (res.data.dict) {
                            let menu = res.data.dict;
                            this.form.dictCode= menu.dictCode,
                            this.form.dictLabel= menu.dictLabel,
                            this.form.dictValue=menu.dictValue,
                            this.form.dictType=menu.dictType,
                            this.form.cssClass=menu.cssClass,
                            this.form.dictSort=menu.dictSort,
                            this.form.listClass=menu.listClass,
                            this.form.isDefault=menu.isDefault,
                            this.form.status=menu.status,
                            this.form.remark=menu.remark
                        }
                    });
                }
            });
        },
        // 保存
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    let params = {
                        dictLabel: this.form.dictLabel,
                        dictValue: this.form.dictValue,
                        dictType: this.form.dictType,
                        cssClass: this.form.cssClass,
                        dictSort: this.form.dictSort,
                        listClass: this.form.listClass,
                        isDefault: this.form.isDefault,
                        status: this.form.status,
                        remark: this.form.remark,
                    }
                    if (this.status == 'edit') {
                        params.dictCode = this.form.dictCode;
                    }
                    this.$http({
                        url: this.$http.adornUrl(`/system/dict/data/${this.status}`),
                        method: "post",
                        params: this.$http.adornParams(params)
                    }).then((res) => {
                        if (res.data.code == 0) {
                            this.$message({
                                message: res.data.msg,
                                type: "success"
                            })
                            setTimeout(() => {
                                this.open = false;
                                this.$parent.openDialog = false;
                                this.$parent.getData();
                            }, 1000);
                        } else {
                            this.$message({
                                message: res.data.msg,
                                type: "error"
                            })
                        }
                    });
                } else {
                    console.log("error submit!!");
                    return false;
                }
            });
        },

        isDefaultFun() {
            this.$http({
                url: this.$http.adornUrl("/tool/dict/getType"),
                method: "GET",
                params: this.$http.adornParams({
                    type: "sys_yes_no"
                }),
            }).then((res) => {
                this.isDefaultArr = res.data;
            });
        },
        statusFun() {
            this.$http({
                url: this.$http.adornUrl("/tool/dict/getType"),
                method: "GET",
                params: this.$http.adornParams({
                    type: "sys_normal_disable"
                }),
            }).then((res) => {
                this.statusArr = res.data;
            });
        },
    },
    //生命周期 - 创建完成（可以访问当前this实例）
    created() { },
    //生命周期 - 挂载完成（可以访问DOM元素）
    mounted() {
        this.isDefaultFun();
        this.statusFun();
    },
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
  