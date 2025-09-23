<template>
    <div class="userContainer">
        <div class="recipientsApply">
            <!-- 表单 -->
            <div ref="formDiv">
                <el-form ref="form" class="unitForm" :model="form" id="form">
                    <el-form-item label="用户名称:" prop="roleName">
                        <el-input placeholder="请输入" v-model="form.roleName" :disabled="true"> </el-input>
                    </el-form-item>
                    <el-form-item label="登录账号:" prop="phone">
                        <el-input placeholder="请输入" v-model="form.phone" :disabled="true"> </el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div class="table">
                <!-- 表格 -->
                <el-table :data="searchTableData.slice((currentPage - 1) * pagesize, currentPage * pagesize)" id="table"
                    stripe style="width: 100%" :header-row-style="{ height: '35px' }" :row-style="{ height: '35px' }"
                    :height="TableHeight">
                    <el-table-column type="selection"  align="center" min-width="4%"> </el-table-column>
                    <el-table-column prop="roleId" label="角色编号" class-name="menuName" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="roleName" label="角色名称" align="center" min-width="14%">
                    </el-table-column>
                    <el-table-column prop="roleKey" label="权限字符" sortable align="center" min-width="14%">
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
</template>
  
<script>
export default {
    name: "unitManagement",
    components: {},
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
        this.rowData = this.$route.params.userId;
        this.getData();
    },
    mounted() {
        //动态计算表格高度
        let windowHeight = document.documentElement.clientHeight || document.bodyclientHeight;
        this.$nextTick(() => {
            this.TableHeight = windowHeight - this.$refs.formDiv.offsetHeight - 175; //数值"140"根据需要调整
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
       
        // 获取数据
        getData() {

            this.$http({
                url: this.$http.adornUrl("/system/user/authRole/" + this.rowData),
                method: "GET",
                params: this.$http.adornParams({}),
            }).then((res) => {
                if (res.status==200) {
                    const data = res.data.roles;
                    this.searchTableData = data;
                    this.total = data.length;
                    this.form.roleName = res.data.user.userName;
                    this.form.phone = res.data.user.loginName;
                }
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
  