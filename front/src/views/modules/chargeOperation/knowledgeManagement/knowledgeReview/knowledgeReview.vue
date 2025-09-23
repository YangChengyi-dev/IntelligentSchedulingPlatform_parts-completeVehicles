<!--  -->
<template>
  <div id="app">
      <div ref="formDiv">
      <el-form ref="form" class="unitForm" :model="form" id="form" >
        <el-form-item label="知识类型:">
          <el-select v-model="form.knowledge_type" placeholder="请选择" clearable="true" >
            <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态:">
          <el-select v-model="form.status"  placeholder="请选择" clearable="true">
            <el-option
            v-for="item in option_status"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="严重等级:">
          <el-select v-model="form.severity_level"  placeholder="请选择" clearable="true">
            <el-option
            v-for="item in option_severity_level"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="录入人:">
          <el-select v-model="form.entry_person"  placeholder="请选择" clearable="true">
            <el-option
            v-for="item in option_audit_person"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" size="small" @click="onSearch"
            >查询</el-button
          >
          <el-button type="primary" icon="el-icon-add" size="small" @click.native="dialogVisible = true"
            >添加</el-button
          >
        </el-form-item>
      </el-form>
      </div>

      <el-dialog :visible.sync="dialogVisible"  custom-class="menu-dialog-height">
        <el-form :v-model="add_form" :inline="true" :label-position="left">
          <el-form-item label="知识类型:">
          <el-select v-model="add_form.knowledge_type" placeholder="请选择" clearable="true">
            <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="审核人：">
          <el-select v-model="add_form.entry_person"  placeholder="请选择" clearable="true">
            <el-option
            v-for="item in option_audit_person"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="严重等级:">
          <el-select v-model="add_form.severity_level"  placeholder="请选择" clearable="true">
            <el-option
            v-for="item in option_severity_level"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="录入人：">
          <el-select v-model="add_form.audit_person"  placeholder="请选择" clearable="true">
            <el-option
            :label="userName"
            :value="userName">
            </el-option>
          </el-select>
        </el-form-item>
        <el-col :span="18">
          <el-form-item label="故障描述:" class="text_description">
          <el-input v-model="add_form.description" 
          type="textarea"
          maxlength="30"
          style="width: 465px;"
          show-word-limit
          autosize="{ minRows: 2, maxRows: 6 }"
          :rows="6"
          >
          </el-input>
        </el-form-item>
        </el-col>
        <el-form-item class="dialog-bottom-button">
                    <el-button @click="submitForm(add_form)">提交</el-button>
                    <el-button @click="resetForm(add_form)">重置</el-button>
                </el-form-item>
        </el-form>
      </el-dialog>
      
    <!-- 表格 -->
      <el-table
        :data="
          searchTableData.slice((queryInfo.page - 1)*queryInfo.pageSize, queryInfo.page*queryInfo.pageSize)
        "
        id="table"
        stripe
        style="width: 100%"
        :header-row-style="{ height: '35px' }"
        :row-style="{ height: '35px' }"
        :height="TableHeight"
        :default-sort="{prop:'audit_time', order:'descending'}"
      >
        <el-table-column label="" align="center" min-width="3%">
          <template slot-scope="scope">
            <el-radio v-model="tableRadio" :label="scope.row"><i></i></el-radio>
          </template>
        </el-table-column>
        <el-table-column type="index" label="序号" align="center" min-width="4%">
        </el-table-column>
        <el-table-column
          prop="knowledge_type"
          label="知识类型"
          align="center"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column
          prop="severity_level"
          label="严重等级"
          align="center"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column
          prop="description"
          label="故障描述"
          align="center"
          min-width="13%"
        >
        </el-table-column>
        <el-table-column
          prop="entry_time"
          label="录入时间"
          align="center"
          min-width="10%"
        >
        </el-table-column>
        <el-table-column
          prop="entry_person"
          label="录入人"
          align="center"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column
          prop="status"
          label="审核状态"
          align="center"
          min-width="4%"
        >
        </el-table-column>
        <el-table-column
          prop="audit_person"
          label="审核人"
          align="center"
          min-width="5%"
        >
        </el-table-column>
        <el-table-column
          prop="audit_time"
          label="审核时间"
          align="center"
          min-width="10%"
        >
        </el-table-column>
      </el-table>
      <!-- 分页 -->
      <el-pagination
        background
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="pagesizes"
        :page-size="pagesize"
        layout=" prev, pager, next, jumper, sizes,total"
        :total="searchTableData.length"
      >
      </el-pagination>
  </div>
</template>

<script>
//这里可以导入其他文件（比如：组件，工具js，第三方插件js，json文件，图片文件等等）
//例如：import 《组件名称》 from '《组件路径》';
import axios from 'axios'
import knowledgeGraphVue from '../knowledgeGraph/knowledgeGraph.vue';
axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8";
export default {
  //import引入的组件需要注入到对象中才能使用
  components: {  },
  data() {
    return {
      form: {
        entry_person:null,
        knowledge_type:null,
        status:null,
        severity_level:null,
      },
      queryInfo: {
					name: '',
					type: '',
					page: 1,
					pageSize: 10
				},
      add_form:{
        knowledge_type:"",
        severity_level:"",
        description:"",
        entry_person:"",
        audit_person:""
      },
      dialogVisible: false,
      searchDataParams:{
        knowledge_type:null,
        status:null,
        severity_level:null,
        audit_person:null
      },
      tableData: [],
      searchTableData: [],
      TableHeight: 0,
      tableRadio: {},
      currentPage: 1,
      pagesize: 10,
      pagesizes: [5, 10, 20, 50, 100],
      total: 0,
      isopenDialog: "false",
      title: "",
      option_status:[{
        value:'通过',
        label:'通过'
      },{
        value:'未通过',
        label:'未通过'
      }],
      option_audit_person:[{
        value:"李工",
        label:"李工"
      },{
        value:"吴工",
        label:"吴工"
      },{
        value:"张工",
        label:"张工"
      }],
      option_severity_level:[{
        value:"告警",
        label:"告警"
      },{
        value:"提示",
        label:"提示"
      },{
        value:"紧急故障",
        label:"紧急故障"
      },{
        value:"轻微故障",
        label:"轻微故障"
      },{
        value:"一般故障",
        label:"一般故障"
      }],
      options: [{
          value: '电气元件',
          label: '电气元件'
        }, {
          value: '充电模块',
          label: '充电模块'
        }, {
          value: '内部环境',
          label: '内部环境'
        }, {
          value: '车桩交互',
          label: '车桩交互'
        }, {
          value: '逻辑类',
          label: '逻辑类'
        },{
          value: '通讯类',
          label: '通讯类'
        }],
    };
  },
  //监听属性 类似于data概念
  computed: {
    userName: {
      get() {
        return this.$store.state.user.user.userName;
      },
    },
  },
  //监控data中的数据变化
  watch: {},
  //方法集合
  methods: {
      getData() {
        axios.get("http://10.160.24.112:7000/KnowledgeAudit/init",).then(result => {
					this.searchTableData = result.data.data;
          this.searchTableData.sort(function(a,b){
            return a.entry_time < b.entry_time ? 1 : -1;
          })
				})
    },
    // 表单查询
    onSearch() {
      if(this.form.knowledge_type=="")
        this.form.knowledge_type=null;
      if(this.form.status=="")
        this.form.status=null;
      if(this.form.severity_level=="")
        this.form.severity_level=null;
      if(this.form.entry_person=="")
        this.form.entry_person=null;
      if(this.form.knowledge_type==null && this.form.status==null && this.form.severity_level==null && this.form.entry_person==null){
        this.getData();
      }
      else{
        const params = {...this.searchDataParams};
        params.knowledge_type = this.form.knowledge_type;
        params.status = this.form.status;
        params.severity_level = this.form.severity_level;
        params.entry_person = this.form.entry_person;
        axios.post("http://10.160.24.112:7000/KnowledgeAudit/search",params).then(result =>{
						this.searchTableData = result.data.data;
						this.$message.success("查询成功");
					})
      }
    },
    tableRes(searchData, table, array) {
      const search = searchData;
      return table.filter((data) => {
        return Object.keys(data).some((key) => {
          if (array) {
            if (array.indexOf(key) == -1) {
              return String(data[key]).toLowerCase().indexOf(search) > -1;
            }
          } else {
            return String(data[key]).toLowerCase().indexOf(search) > -1;
          }
        });
      });
      return table;
    },
    // 表格选择当前显示行数
    handleCurrentChange(page) {
				this.queryInfo.page = page;
			},
			handleSizeChange(size) {
				this.queryInfo.pageSize = size;
			},
    resetForm(add_form) {
				add_form.knowledge_type = "";
        add_form.severity_level = "";
        add_form.entry_person = "";
        add_form.audit_person = "";
        add_form.description = "";
			},
    submitForm(add_form){
      if(add_form.knowledge_type=="" || add_form.severity_level=="" || add_form.entry_person=="" || add_form.audit_person=="" || add_form.description==""){
        this.$message.error("添加失败，必须字段均不能为空");
      }
      else{
        axios.get("http://10.160.24.112:7000/KnowledgeAudit/create",{
						params:{
              knowledge_type:add_form.knowledge_type,
              severity_level:add_form.severity_level,
              entry_person:add_form.entry_person,
              audit_person:add_form.audit_person,
              description:add_form.description
						}
					}).then((res) => {
            this.$message.success("插入成功");
            this.dialogVisible = false;
            this.getData();
					})
      }
    }

  },
  //生命周期 - 创建完成（可以访问当前this实例）
  created() {
       this.getData();
  },
  //生命周期 - 挂载完成（可以访问DOM元素）
  mounted() {
    
      //动态计算表格高度
    let windowHeight = document.documentElement.clientHeight || document.bodyclientHeight;
    this.$nextTick(() => {
      this.TableHeight =
        windowHeight -
        this.$refs.formDiv.offsetHeight -
        175; //数值"140"根据需要调整
    });
    
  },
  beforeCreate() {}, //生命周期 - 创建之前
  beforeMount() {}, //生命周期 - 挂载之前
  beforeUpdate() {}, //生命周期 - 更新之前
  updated() {}, //生命周期 - 更新之后
  beforeDestroy() {}, //生命周期 - 销毁之前
  destroyed() {}, //生命周期 - 销毁完成
  activated() {}, //如果页面有keep-alive缓存功能，这个函数会触发
};
</script>
<style lang="scss" scoped>
.unitForm {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  .el-form-item {
    width: 24%;
    .el-form-item__label {
      width: 40%;
      // width: 150px;
    }
    .el-form-item__content {
      margin-left: 10px !important;
      .el-date-editor {
        width: 100%;
        // width: 202px;
        .el-input__icon {
          color: #15a193;
        }
      }
    }
  }
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 15px;

  .btnGroup {
    width: 35%;
  }
}
.dialog-bottom-button {
        margin-left: 75%;
    }
.text_description {
  width: 100%;
}

</style>


