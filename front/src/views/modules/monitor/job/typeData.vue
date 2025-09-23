<template>
    <div class="userContainer">
        <div class="recipientsApply">
            <!-- 表单 -->
            <div ref="formDiv">
                <el-form ref="form" class="unitForm" :model="form" id="form">
                    <el-form-item label="任务分组:" prop="jobGroup">
                        <el-select v-model="form.jobGroup" placeholder="请选择">
                            <el-option v-for="(item,index) in options" :key="index" :label="item.dictLabel"
                                :value="item.dictValue">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="执行状态:" prop="status">
                        <el-select v-model="form.status" placeholder="请选择">
                            <el-option v-for="(item,index) in statusArr" :key="index" :label="item.dictLabel"
                                :value="item.dictValue">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="操作时间:" prop="time">
                        <el-date-picker v-model="form.time" unlink-panels type="daterange" range-separator="-"
                            start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd">
                        </el-date-picker>
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
                        <el-button type="primary" size="mini" @click="deleteSelect(muticalSelectData)"> 删除 </el-button>
                        <el-button type="primary" size="mini" @click="clean"> 清空 </el-button>
                        <el-button type="primary" size="mini" @click="exportExcel"> 导出 </el-button>
                    </el-row>
                </div>
                <!-- 表格 -->
                <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table"
                    stripe style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }"
                    :height="TableHeight" @selection-change="handleSelectionChange">
                    <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
                    <el-table-column prop="jobLogId" label="日志编号" class-name="menuName" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="jobName" label="任务名称" align="center" min-width="14%">

                    </el-table-column>
                    <el-table-column prop="jobGroup" label="任务分组" align="center" min-width="14%">
                        <template slot-scope="scope">
                            <div v-for="(item,index) in options" :key="index">
                                <div v-if="scope.row.jobGroup==item.dictValue">
                                    <el-tag effect="dark" type="">{{item.dictLabel}}</el-tag>
                                </div>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="invokeTarget" label="调用目标字符串" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="jobMessage" label="日志信息" align="center" show-overflow-tooltip
                        min-width="12%">

                    </el-table-column>
                    <el-table-column prop="status" label="状态" sortable align="center" min-width="14%">
                        <template slot-scope="scope">
                            <div v-for="(item,index) in statusArr" :key="index">
                                <div v-if="scope.row.status==item.dictValue">
                                    <el-tag effect="dark" :type="scope.row.status==1?'danger':''">{{item.dictLabel}}
                                    </el-tag>
                                </div>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column prop="createTime" label="创建时间" sortable align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column label="操作" align="center" min-width="14%">
                        <template slot-scope="scope">
                            <div class="opr">
                                <el-button type="primary" icon="el-icon-edit" size="mini" @click="detailRow(scope.row)">
                                    详细
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
                <tableFirst :title="title" width="40%" :isDetail="isDetail" v-if="openDialog" ref="testDialog">
                </tableFirst>
            </div>
        </div>
    </div>
</template>
  
<script>
import FileSaver from 'file-saver';
import * as XLSX from 'xlsx';
import tableFirst from "./log";
export default {
    name: "unitManagement",
    components: { tableFirst },
    data() {
        return {
            form: {
                jobGroup: "",
                status: "",
                time: '',
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
            isDetail: false,
            openDialog: false,
            muticalSelectData: [],

            options: [],
            statusArr: [],
            title: '',
        };
    },
    created() {
        this.rowData = this.$route.params.data;
        this.getData();
        this.statusFun();
        this.jobGroupFun();

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

            let formData = new FormData();
            formData.append("jobGroup", this.form.jobGroup);
            formData.append("status", this.form.status);
            formData.append("params[beginTime]", this.form.time[0] ? this.form.time[0] : "");
            formData.append("params[endTime]", this.form.time[1] ? this.form.time[1] : "");
            this.$http({
                url: this.$http.adornUrl("/monitor/jobLog/list"),
                method: "post",
                data: formData
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
        // 任务分组接口
        jobGroupFun() {
            this.$http({
                url: this.$http.adornUrl("/tool/dict/getType"),
                method: "get",
                params: this.$http.adornParams({
                    type: "sys_job_group"
                }),
            }).then((res) => {
                if (res.status == 200) {
                    const data = res.data;
                    this.options = data;

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
                        "type": "sys_common_status"
                    }
                ),
            }).then((res) => {
                if (res.data.length) {
                    const data = res.data;
                    this.statusArr = data;
                }
            });
        },

        // 删除复选框选中的数据
        deleteSelect(data) {
            if (data) {
                let length = data.length;
                var ids = [];
                for (const key of data) {
                    ids.push(key.jobLogId)
                }

                this.$confirm("确认删除" + length + "行数据?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning",
                })
                    .then(() => {
                        this.$http({
                            url: this.$http.adornUrl(`/monitor/jobLog/remove`),
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
        // 清空
        clean() {
            this.$confirm("确认清空所有调度日志?", "提示", {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
            })
                .then(() => {
                    this.$http({
                        url: this.$http.adornUrl(`/monitor/jobLog/clean`),
                        method: "POST",
                        params: this.$http.adornParams({})
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
        // 详情
        detailRow(data) {
            this.openDialog = true;
            this.isDetail = true;
            this.title = "调度日志详情";
            this.$nextTick(() => {
                this.$refs.testDialog.editFun(data, 'detail');
            });
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
  