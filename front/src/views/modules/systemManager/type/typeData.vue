<template>
    <div class="userContainer">
        <div class="recipientsApply">
            <!-- 表单 -->
            <div ref="formDiv">
                <el-form ref="form" class="unitForm" :model="form" id="form">
                    <el-form-item label="字典名称:" prop="dictType">
                        <el-select v-model="form.dictType" placeholder="请选择">
                            <el-option v-for="(item,index) in options" :key="index" :label="item.dictName"
                                :value="item.dictType">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="字典标签:" prop="dictLabel">
                        <el-input placeholder="请输入" v-model="form.dictLabel" clearable> </el-input>
                    </el-form-item>
                    <el-form-item label="数据状态:" prop="status">
                        <el-select v-model="form.status" placeholder="请选择">
                            <el-option v-for="(item,index) in statusArr" :key="index" :label="item.dictLabel"
                                :value="item.dictValue">
                            </el-option>
                        </el-select>
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
                        <el-button type="primary" size="mini" @click="addRow(null)">新增</el-button>
                        <el-button type="primary" size="mini" @click="editSelect(muticalSelectData)"> 修改 </el-button>
                        <el-button type="primary" size="mini" @click="deleteSelect(muticalSelectData)"> 删除 </el-button>
                        <el-button type="primary" size="mini" @click="exportExcel"> 导出 </el-button>
                    </el-row>
                </div>
                <!-- 表格 -->
                <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table"
                    stripe style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }"
                    :height="TableHeight" @selection-change="handleSelectionChange">
                    <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
                    <el-table-column prop="dictCode" label="字典编码" class-name="menuName" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="dictLabel" label="字典标签" align="center" min-width="14%">
                        <template slot-scope="scope">
                            <el-tag type="">{{scope.row.dictLabel}}</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="dictValue" label="字典键值" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="dictSort" label="字典排序" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="status" label="状态" align="center" min-width="12%">
                        <template slot-scope="scope">
                            <div v-if="scope.row.status == '0'">
                                <el-tag type="">正常</el-tag>
                            </div>
                            <div v-if="scope.row.status == '1'">
                                <el-tag type="danger" effect="dark">异常</el-tag>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="remark" label="备注" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="createTime" label="创建时间" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column label="操作" align="center" min-width="14%">
                        <template slot-scope="scope">
                            <div class="opr">
                                <el-button type="primary" icon="el-icon-edit" size="small" @click="editRow(scope.row)">
                                    编辑
                                </el-button>
                                <el-button type="primary" icon="el-icon-delete" size="small"
                                    @click="deleteRow(scope.row)">
                                    删除
                                </el-button>
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
                <tableFirst :title="title" width="70%" v-if="openDialog" ref="testDialog"></tableFirst>
            </div>
        </div>
    </div>
</template>
  
<script>
import FileSaver from 'file-saver';
import * as XLSX from 'xlsx';
import tableFirst from "./addUser";
export default {
    name: "unitManagement",
    components: { tableFirst },
    data() {
        return {
            form: {
                dictType: "",
                dictLabel: "",
                status: "",
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

            options: [],
            statusArr: [],
            title: '',
        };
    },
    created() {
        this.rowData = this.$route.params.data;
        this.statusFun();
        this.dictTypeFun();

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
        getData(dictType) {
            let params = {
                dictType: dictType ? dictType : this.form.dictType,
                dictLabel: this.form.dictLabel,
                status: this.form.status,
            }
            this.$http({
                url: this.$http.adornUrl("/system/dict/data/list"),
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
            this.getData();
        },


        // 重置
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },

        // 复选框选中的数组
        handleSelectionChange(val) {
            this.muticalSelectData = val;
        },
        // 字典名称接口
        dictTypeFun() {
            this.$http({
                url: this.$http.adornUrl("/system/dict/detail/" + this.rowData.dictId),
                method: "get",
                params: this.$http.adornParams({}),
            }).then((res) => {
                if (res.status == 200) {
                    const data = res.data.dictList;
                    this.options = data;

                    this.form.dictType = res.data.dict.dictType;
                    this.getData(res.data.dict.dictType);

                }
            });
        },
        // 用户状态接口
        statusFun() {
            this.$http({
                url: this.$http.adornUrl("/tool/dict/getType"),
                method: "get",
                params: this.$http.adornParams(
                    {
                        "type": "sys_normal_disable"
                    }
                ),
            }).then((res) => {
                if (res.data.length) {
                    const data = res.data;
                    this.statusArr = data;
                }
            });
        },

        // 新增
        addRow(data) {
            this.openDialog = true;
            this.isDetail = false;
            this.title = "添加数据";
            this.$nextTick(() => {
                this.$refs.testDialog.addFun(this.form.dictType, 'add');
            });
        },
        // 编辑多选数据
        editSelect(data) {
            var that = this;
            if (data.length == 1) {
                that.openDialog = true;
                that.isDetail = false;
                that.title = "修改数据";
                that.$nextTick(() => {
                    that.$refs.testDialog.editFun(data[0], 'edit');
                });
            } else {
                this.$message({
                    message: '请选择一条数据',
                    type: 'warning'
                })
            }
        },
        // 删除复选框选中的数据
        deleteSelect(data) {
            if (data) {
                let length = data.length;
                var ids = [];
                for (const key of data) {
                    ids.push(key.dictCode)
                }

                this.$confirm("确认删除" + length + "行数据?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                })
                    .then(() => {
                        this.$http({
                            url: this.$http.adornUrl(`/system/dict/data/remove`),
                            method: "POST",
                            params: this.$http.adornParams({
                                "ids": ids.join(',')
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
                            } else {
                                this.$message({
                                    message: res.data.msg,
                                    type: "error"
                                })
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
        // 导出
        exportExcel() {
            const loading = this.$loading({
                lock: true,
                text: "导出中...",
                spinner: "el-icon-loading",
                background: "rgba(0, 0, 0, 0.7)",
            });
            setTimeout(() => {
                loading.close();
                /* generate workbook object from table */
                var xlsxParam = { raw: true };
                var wb = XLSX.utils.table_to_book(document.querySelector("#table"), xlsxParam);
                /* get binary string as output */
                var wbout = XLSX.write(wb, { bookType: "xlsx", bookSST: true, type: "array" });
                try {
                    FileSaver.saveAs(
                        new Blob([wbout], { type: "application/octet-stream" }),
                        this.$route.meta.title + ".xlsx"
                    );
                } catch (e) {
                    if (typeof console !== "undefined") console.log(e, wbout);
                }
                return wbout;
            }, 2000);
        },
        // 编辑
        editRow(data) {
            this.openDialog = true;
            this.isDetail = false;
            this.title = "修改岗位";
            this.$nextTick(() => {
                this.$refs.testDialog.editFun(data, 'edit');
            });
        },
        // 删除
        deleteRow(data) {
            if (data) {
                this.$confirm("确认删除该行数据?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                })
                    .then(() => {
                        this.$http({
                            url: this.$http.adornUrl(`/system/dict/data/remove`),
                            method: "POST",
                            params: this.$http.adornParams({
                                "ids": data.dictCode
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
  