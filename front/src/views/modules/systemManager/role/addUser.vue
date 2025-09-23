<template>
    <div class="dialogDiv">
        <el-dialog class="dialog" :title="title" :visible.sync="open" :width="width" :close-on-click-modal="false"
            append-to-body :lock-scroll="false" @destroy-on-close="true">
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
                                <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch">查询
                                </el-button>
                                <el-button icon="el-icon-refresh-right" size="small" @click="resetForm('form')">重置
                                </el-button>
                            </el-form-item>
                        </el-form>
                    </div>
                    <div class="table">
                        <!-- 表格 -->
                        <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)"
                            id="table" stripe style="width: 100%" :header-row-style="{ height: '35px' }"
                            :row-style="{ height: '35px' }" :height="TableHeight"  @selection-change="handleSelectionChange">
                            <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
                            <el-table-column prop="loginName" label="登录名称" class-name="menuName" align="center"
                                min-width="14%">
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
                        </el-table>
                        <!-- 分页 -->
                        <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
                            :current-page="currentPage" :page-sizes="pagesizes" :page-size="pagesize"
                            layout=" prev, pager, next, jumper, sizes,total" :total="total">
                        </el-pagination>
                    </div>
                </div>
            </div>
            <div slot="footer" class="dialog-footer">
        <el-button class="" @click="cancel">取消</el-button>
        <el-button class="" type="primary" @click="submitForm(muticalSelectData)">保存</el-button>
      </div>
        </el-dialog>
    </div>

</template>
  
<script>

export default {
    name: "unitManagement",
    components: {},
    props: ["title", "width"],
    data() {
        return {
            open: false,
            form: {
                roleName: "",
                phone: "",
            },
            tableData: [],
            searchTableData: [],
            TableHeight: '40vh',
            tableRadio: "",
            currentPage: 1,
            pagesize: 10,
            pagesizes: [2, 5, 10, 20, 50, 100],
            total: 0,

            roleId: "",
            muticalSelectData:[],
        };
    },
    created() {

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

    },
    methods: {
        init(tableRadio) {
            this.open = true;
            var that = this;
            this.$nextTick(() => {
                // 表单重置
                that.$refs.form.resetFields();
                // 查看/修改
                if (tableRadio) {
                    this.roleId = tableRadio;
                    this.getData();

                } else {//新增
                }
            });
        },
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
        // 获取数据
        getData() {
            let params = {
                loginName: this.form.roleName,
                phonenumber: this.form.phone,
                roleId: this.roleId,
                orderByColumn: "createTime",
                isAsc: "desc"
            }
            this.$http({
                url: this.$http.adornUrl("/system/role/authUser/unallocatedList"),
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

         // 取消
    cancel() {
      this.open = false;
      this.$parent.openDialog = false;
      this.$parent.getData();
    },

     // 保存
     submitForm(data) {
        if(data.length>0){
            var userIds=[];
            for (const key of data) {
                userIds.push(key.userId);
            }
            var that = this;
            let params = {
              roleId: this.roleId,
              userIds: userIds.join(','),
            }
            this.$http({
              url: this.$http.adornUrl(`/system/role/authUser/selectAll`),
              method: "post",
              params: this.$http.adornParams(params)
            }).then((res) => {
              if (res.data.code == 0) {
                this.$message({
                  message: res.data.msg,
                  type: "success"
                })
                setTimeout(() => {
                  that.open = false;
                  that.$parent.openDialog = false;
                  that.$parent.getData();
                }, 1000);
              }
  
  
            });
        }
    },

    // 复选框选中的数组
    handleSelectionChange(val){
this.muticalSelectData=val;
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
</style>
  