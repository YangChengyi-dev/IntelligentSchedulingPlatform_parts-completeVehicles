<template>
    <div class="userContainer">
        <div class="recipientsApply">
            <!-- 表单 -->
            <div ref="formDiv">
                <el-form ref="form" class="unitForm" :model="form" id="form">
                    <el-form-item label="登录名称:" prop="roleName">
                        <el-input placeholder="请输入" v-model="form.roleName" clearable> </el-input>
                    </el-form-item>
                    <el-form-item label="手机号码:" prop="phone">
                        <el-input placeholder="请输入" v-model="form.phone" clearable> </el-input>
                    </el-form-item>

                    <el-form-item>
                        <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch">查询</el-button>
                        <el-button icon="el-icon-refresh-right" size="small" @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <div class="table">
                <!-- 工具栏 -->
                <div ref="toolbar" class="toolbar">
                    <el-row class="btnGroup">
                        <el-button type="primary" size="mini" @click="addUser">添加用户 </el-button>
                        <el-button type="primary" size="mini" @click="cancel(muticalSelectData)"> 批量取消授权 </el-button>
                    </el-row>
                </div>
                <!-- 表格 -->
                <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table"
                    stripe style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }"
                    :height="TableHeight" @selection-change="handleSelectionChange">
                    <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
                    <el-table-column prop="loginName" label="登录名称" class-name="menuName" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="userName" label="用户名称" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="email" label="邮箱" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="phonenumber" label="手机" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="status" label="用户状态" align="center" min-width="12%">
                        <template slot-scope="scope">
                            <div v-if="scope.row.status == '0'">
                                <el-tag type="">正常</el-tag>
                            </div>
                            <div v-if="scope.row.status == '1'">
                                <el-tag type="danger" effect="dark">异常</el-tag>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="createTime" label="创建时间" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column label="操作" align="center" min-width="14%">
                        <template slot-scope="scope">
                            <div class="opr">
                                <el-button type="primary" icon="el-icon-delete" size="mini"
                                    @click="cancelRow(scope.row)">取消授权</el-button>
                            </div>
                        </template>
                    </el-table-column>
                </el-table>
                <!-- 分页 -->
                <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                    :current-page="currentPage" :page-sizes="pagesizes" :page-size="pagesize"
                    layout=" prev, pager, next, jumper, sizes,total" :total="total">
                </el-pagination>
            </div>

            <!-- 添加用户 -->
            <div class="dialog">
                <tableFirst title="选择用户" width="70%" v-if="openDialog" ref="testDialog"></tableFirst>
            </div>
        </div>
    </div>
</template>
  
<script>
import tableFirst from "./addUser";
export default {
    name: "unitManagement",
    components: { tableFirst },
    data() {
        return {
            form: {
                roleName: "",
                phone: "",
            },
            tableData: [],
            searchTableData: [],
            TableHeight: 0,
            tableRadio: "",
            currentPage: 1,
            pagesize: 10,
            pagesizes: [2, 5, 10, 20, 50, 100],
            total: 0,

            rowData: {},

            openDialog: false,
            muticalSelectData: [],
        };
    },
    created() {
        this.rowData = this.$route.params.data;
        this.getData();

        var _this = this;
        document.onkeydown = function (e) {
            //按下回车提交
            let key = window.event.keyCode;
            //事件中keycode=13为回车事件
            if (key == 13) {
                _this.onSearch();
            }
        };
    },
    mounted() {
        //动态计算表格高度
        let windowHeight = document.documentElement.clientHeight || document.bodyclientHeight;
        this.$nextTick(() => {
            this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - this.$refs.toolbar.offsetHeight - 175; //数值"140"根据需要调整
        });
    },
    methods: {

        // 单选获取整行数据
        clickChange(item) {
            this.tableRadio = item;
        },

        // 表格选择当前显示行数
        handleSizeChange(val) {
            this.pagesize = val;
        },
        // 切换表格页面
        handleCurrentChange(val) {
            this.currentPage = val;
        },
        // 多选框选择数据
        handleSelectionChange(val) {
            this.selectionData = val;
        },
        // 获取数据
        getData() {
            let params = {
                loginName: this.form.roleName,
                phonenumber: this.form.phone,
                roleId: this.rowData.roleId,
                orderByColumn: "createTime",
                isAsc: "desc"
            }
            this.$http({
                url: this.$http.adornUrl("/system/role/authUser/allocatedList"),
                method: "post",
                params: this.$http.adornParams(params),
            }).then((res) => {
                if (res.data.code == 0) {
                    const data = res.data.rows;
                    this.searchTableData = data;
                    this.total = data.length;

                }
            });
        },

        // 表单查询
        onSearch() {
            let params = {
                loginName: this.form.roleName,
                phonenumber: this.form.phone,
                roleId: this.rowData.roleId,
                orderByColumn: "createTime",
                isAsc: "desc"
            }
            this.$http({
                url: this.$http.adornUrl("/system/role/authUser/allocatedList"),
                method: "post",
                params: this.$http.adornParams(params),
            }).then((res) => {
                const data = res.data.rows;
                this.searchTableData = data;
            });
        },


        // 重置
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },
        // 添加用户
        addUser() {
            this.openDialog = true;
            this.$nextTick(() => {
                this.$refs.testDialog.init(this.rowData.roleId);
            });
        },
        // 复选框选中的数组
        handleSelectionChange(val) {
            this.muticalSelectData = val;
        },
        // 批量取消授权
        cancel(data) {
            if (data) {
                let length = data.length;
                var ids = [];
                for (const key of data) {
                    ids.push(key.userId)
                }

                this.$confirm("确认删除" + length + "行数据?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                })
                    .then(() => {
                        this.$http({
                            url: this.$http.adornUrl(`/system/role/authUser/cancelAll`),
                            method: "POST",
                            params: this.$http.adornParams({
                                "roleId":this.rowData.roleId,
                                "userIds": ids.join(',')
                            })
                        }).then(res => {
                            if (res.data.code == 0) {
                                this.$message({
                                    type: "success",
                                    message: res.data.msg,
                                });
                                setTimeout(() => {
                                    this.getData();
                                }, 1000);
                            }
                        }).catch(err => {

                        })

                    })
                    .catch(() => { });
            } else {
                this.$message({
                    message: "请选择行！",
                    type: "warning",
                });
            }
        },
        // 取消授权
        cancelRow(data){
                this.$confirm("确认删除该行数据?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                })
                    .then(() => {
                        this.$http({
                            url: this.$http.adornUrl(`/system/role/authUser/cancelAll`),
                            method: "POST",
                            params: this.$http.adornParams({
                                "roleId":this.rowData.roleId,
                                "userIds": data.userId
                            })
                        }).then(res => {
                            if (res.data.code == 0) {
                                this.$message({
                                    type: "success",
                                    message: res.data.msg,
                                });
                                setTimeout(() => {
                                    this.getData();
                                }, 1000);
                            }
                        }).catch(err => {

                        })

                    })
                    .catch(() => { });
        }
    },
};
</script>
<style lang="scss">
.el-form-item__label {
    // width: auto !important;
}
</style>
<style lang="scss" scoped>
.userContainer {
    display: flex;
    justify-content: space-between;

    .recipientsApply {
        width: 100%;

        .unitForm {
            display: flex;
            // justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;

            .el-form-item {
                width: 25%;
            }
        }
    }
}

.toolbar {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    padding-bottom: 15px;

    .btnGroup {
        width: 100%;
    }
}

.opr {
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    .operate {
        color: #1ba799;
        cursor: pointer;
    }
}
</style>
  