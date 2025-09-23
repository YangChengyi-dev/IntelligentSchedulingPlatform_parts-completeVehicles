<template>
	<div class="goodsindex">
		<el-button type="text" @click.native="dialogVisible = true">
            上传文件
        </el-button>
        <!--上传文件通知框-->
        <el-dialog :visible.sync="dialogVisible" :before-close="handleClose" custom-class="menu-dialog-height" :close="resetFromOther">
            <el-form :v-model="form">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="项目名称" >
                            <el-input v-model="form.name" style="width:180x"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item>
                    <el-upload
						ref="upload"
                        class="upload-demo"
                        drag
                        :action="actionURL"
                        multiple
						accept=".xlsx"
						:before-upload="beforeUpload"
                        >
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">只能上传excel文件，且不超过500kb</div>
                    </el-upload>
                </el-form-item>
                <el-form-item class="dialog-bottom-button">
                    <el-button @click="submitForm(form)">提交</el-button>
                    <el-button @click="resetForm(form)">重置</el-button>
                </el-form-item>
            </el-form>

           
            
        </el-dialog>
		<!-- 搜索条件 -->
		<el-row :gutter="20" class="goodsindex-queryInfo">
			<!-- 商品名称搜索 -->
			<el-col :xs="8" :sm="6" :md="6" :lg="4" :xl="4">
				<el-input class="goodsindex-queryInfo-li-one" v-model="queryInfo.name" clearable size="small"
					placeholder="请输入项目名称"></el-input>
			</el-col>
			<el-col :xs="6" :sm="4" :md="3" :lg="2" :xl="2">
				<el-button type="primary" class="goodsindex-queryInfo-li-two" size="small" @click="search(queryInfo.name)">搜索</el-button>
			</el-col>
			<el-col :xs="6" :sm="4" :md="3" :lg="2" :xl="2">
				<el-button type="primary" class="goodsindex-queryInfo-li-three" size="small" @click="reset">重置</el-button>
			</el-col>

		</el-row>
		<!-- 检索结果 -->
		<el-row :gutter="20">
			<el-col :span="24">
				<el-table :data="tableData.slice((queryInfo.page - 1)*queryInfo.pageSize, queryInfo.page*queryInfo.pageSize)" size='small' style="width: 100%" :default-sort="{prop:'create_time', order:'descending'}">

					<el-table-column prop="file_name" label="名称" width="250" align="center">
					</el-table-column>
					<!-- <el-table-column prop="task_id" label="任务" width="150">
					</el-table-column> -->
					<!-- <el-table-column prop="simulate_network" label="仿真网络结构" width="250" align="center">
					</el-table-column>
					<el-table-column prop="electrical_distance" label="电气距离" width="250" align="center">
					</el-table-column> -->
					<el-table-column prop="create_time" label="创建时间" width="260" :sortable="true" align="center">
					</el-table-column>
					<el-table-column prop="address" label="操作" align="center">
						<template slot-scope="scope">
							<el-button size="small" :plain="true" @click="sendRequest(scope.row.task_id)">开始诊断</el-button>
							<el-button size="small" :plain="true" type="success" @click="checkResult(scope.row.simulate_network,scope.row.electrical_distance,scope.row.task_id)">查看结果</el-button>
							<el-button size="small" :plain="true" type="primary" @click="downloadFile(scope.row.task_id)">下载文件</el-button>
							<el-button size="small" :plain="true" type="danger" @click="deleteTaskId(scope.row.task_id, scope.row)">删除任务</el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-col>
		</el-row>
		<!--结果展示-->
		<el-dialog :visible.sync="resultShow" customClass="customWidth" class="result-dialog" >
			<el-row :gutter="20" class="result-list">
				<el-col :span="24">
					<el-table 
                    :data="resultTable"
                    size='small' 
                    style="width: 100%"
					:cell-style="cellStyle">
                    <el-table-column type="index" label="序号" align="center" min-width="5%"></el-table-column>
                    <el-table-column prop="serial_number" label="充电桩编号" min-width="15%" align="center"></el-table-column>
                    <el-table-column prop="date" label="日期" min-width="10%" align="center"></el-table-column>
                    <el-table-column prop="is_fault" label="是否故障" min-width="5%" align="center"></el-table-column>
                    <el-table-column prop="type" label="故障类别" min-width="10%" align="center"></el-table-column>
                    <el-table-column prop="health" label="健康度" min-width="15%" align="center"></el-table-column>
                    <el-table-column prop="level" label="预警级别" min-width="5%" align="center"></el-table-column>
                    </el-table>
				</el-col>
			</el-row>
		</el-dialog>
		<!-- 分页 -->
		<el-row :gutter="20" class="goodsindex-list">
			<el-col :span="24" class="goodsindex-page-box">
				<el-pagination @size-change="handleSizeChange"
					@current-change="handleCurrentChange" :current-page="queryInfo.page" :page-sizes="[10, 20, 50, 100]"
					:page-size="queryInfo.pageSize" layout="total, sizes, prev, pager, next, jumper" :total="tableData.length">
				</el-pagination>
			</el-col>
		</el-row>
	</div>
</template>

<script>
	import axios from 'axios'
	axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8";

	export default {
		data() {
			return {
				queryInfo: {
					name: '',
					type: '',
					page: 1,
					pageSize: 10
				},
                dialogVisible: false,
				fileList:[],
                resultTable:[],
				is_upload:false,
				fd:{},
				headers: {
         		 "content-type": "multipart/form-data"
        		},
				
                form: {
                    name: '',
                    file:'',
                    date1: '',
                    date2: '',
                    delivery: false,
                    type: [],
                    resource: '',
                    desc: '',
                },
				searchParam:{
					file_name:null
				},
				si_id:"1",
				sle_id:"1",
				si_url:'',
				ele_url:"",
                formLabelWidth: '120px',
				tableData: [],
				actionURL:"",
				tempTableData:{
					task_id:null,
					file_path:null,
					file_name:null,
					create_time:null
				},
				deleteTaskIdParams:{
					task_id:null,
					task_type:null
				},
				resultShowParams: {
					task_id: null,
					batch_size: null,
					batch_num: null
				},
				sendRequestParams: {
					task_id: null,
				},
				keyCodeShow: false,
				resultShow: false,
				keyCodeForm: {
					name: '',
					remarks: ''
				},
				keyCodeRules: {
					name: [{
							required: true,
							message: '请输入文件名称',
							trigger: 'blur'
						},
						{
							min: 1,
							max: 5,
							message: '长度在 1 到 5 个字符',
							trigger: 'blur'
						}
					]
				},
				keyCodeWidth: '120px',
			}
		},
		created() {
			this.getTask();
		},
		methods: {
            handleClose(done) {
            this.$confirm('确认关闭？')
                .then(_ => {
                done();
            })
            .catch(_ => {});
        },
			// 发送抽取请求
			sendRequest(task_id) {
				axios.get("http://10.160.24.112:7000/FaultDiagnosis/status",{
					params:{
						task_id:task_id,
					}
				}).then(res => {
					let status  = res.data.data;
					if(status == 0){
						const params = {...this.sendRequestParams};
						params.task_id = task_id;
						axios.post("http://10.160.24.112:7000/FaultDiagnosis/begin", params).then(result => {
							this.$message('请求已发送');
						})
					} else if(status == 2){
						this.$message.success("诊断已完成");
					} else if(status == 1){
						this.$message("诊断进行中");
					} else{
						this.$message.error("诊断失败");
					}
				})
				
			},
			// 查看抽取结果
			checkResult(si_id,ele_id,task_id) {
				axios.get("http://10.160.24.112:7000/FaultDiagnosis/status",{
					params:{
						task_id:task_id,
					}
				}).then(res => {
					let status  = res.data.data;
					if(status == 2){
						axios.get("http://10.160.24.112:7000/FaultDiagnosis/result",{
					        params:{
						        task_id:task_id,
					        }
				        }).then(res => {
                            this.resultTable = res.data.data;
                            this.resultShow = true;
							for(var i = 0;i < this.resultTable.length;i++){
								if(this.resultTable[i].level == '无')
									this.resultTable[i].level = ""
								
							}
                            console.log(this.resultTable);
                        })
					} else if(status == 0){
						this.$message("请先开始诊断");
					} else if(status == 1){
						this.$message("诊断进行中");
					} else{
						this.$message.error("诊断失败");
					}
				})
				
			},
			//下载文件
			downloadFile(task_id) {
				axios.get("http://10.160.24.112:7000/FaultDiagnosis/status",{
					params:{
						task_id:task_id,
					},
				}).then(res => {
					let status  = res.data.data;
					if(status == 2){
						const params = {...this.sendRequestParams};
						params.task_id = task_id;
						axios.post("http://10.160.24.112:7000/FaultDiagnosis/download",params,{responseType: 'blob'}).then((res) => {
							console.log(res.data);
							let link = document.createElement('a')
							link.href = window.URL.createObjectURL(new Blob([res.data]))
							link.target = '_blank'
							let filename = `任务${task_id}推断结果.txt`
							link.download = decodeURI(filename) // 下载的文件名称
							document.body.appendChild(link) // 添加创建的 a 标签 dom节点
							link.click() // 下载
							document.body.removeChild(link) // 移除节点
						})
					} else if(status == 0){
						this.$message("请先开始诊断");
					} else if(status == 1){
						this.$message("诊断进行中");
					} else if(status == 3){
						this.$message.error("诊断失败");
					}
				})
				
			},
			// getFile(file, fileList) {
        	// 	this.fileList = fileList;
        	// 	// console.log(this.fileList)
        	// 	const fd = new FormData() // FormData 对象
			// 	fd.append("file",file);
			// 	console.log(file);
        	// 	this.fd = fd;
      		// },
			onSuccess(response, file, fileList) {
			},
			// 删除任务
			deleteTaskId(task_id, item) {
				axios.get("http://10.160.24.112:7000/FaultDiagnosis/status",{
					params:{
						task_id:task_id,
					}
				}).then(res => {
					let status  = res.data.data;
					if(status == 1){
						this.$message.error("诊断中无法删除");
					} else {
						this.tableData = this.tableData.filter(o => o.task_id != item.task_id);
						axios.get("http://10.160.24.112:7000/FaultDiagnosis/delete", {
							params:{
								task_id:task_id
							}
						}).then(result => {
							console.log(result.data.message);
						})
						this.$message({
							message:"任务删除成功",
							type:'success'
						})
							}
						})
				
			},
			// 分页
			handleCurrentChange(page) {
				this.queryInfo.page = page;
			},
			handleSizeChange(size) {
				this.queryInfo.pageSize = size;
			},
			reset(){
				this.queryInfo.name="";
				this.getTask();
			},
			// 获取任务
			getTask() {
				axios.get("http://10.160.24.112:7000/FaultDiagnosis/init",).then(result => {
					this.tableData = result.data.data;
				})

			},
			// beforeUpload (file) {
			// 	return new Promise((resolve, reject) => {
			// 		let id = Math.random().toString(36).slice(-8);
			// 		let name = form.name;
			// 		let time = new Date(+new Date() + 8 * 3600 * 1000).toISOString().replace(/T/g, ' ').replace(/\.[\d]{3}Z/, '');
			// 		const tempData = {...this.tempTableData};
			// 		this.actionURL = "http://10.160.24.112:7000/Inference/upload" + "?task_id="+id + "&file_name="+name+"&create_time="+time;
			// 		console.log(this.actionURL);
			// 		tempData.task_id = id;
			// 		tempData.file_name = name;
			// 		tempData.create_time = time;
			// 		this.tableData.push(tempData);
			// 		this.$nextTick(() => resolve());
					
			// 	})
				
			// },
			// submitUpload() {
			// 	this.$refs.upload.submit();
			// },
			beforeUpload (file) {
				return new Promise((resolve,reject) => {
					this.is_upload = false;
					console.log(file);
					var id = Math.random().toString(36).slice(-8);
					console.log(id);
					var time = new Date(+new Date() + 8 * 3600 * 1000).toISOString().replace(/T/g, ' ').replace(/\.[\d]{3}Z/, '');
					console.log(time);
					var name = this.form.name;
					if(name == "")
						this.message.error("名称不能为空");
					else{
						console.log(name);
						const tempData = {...this.tempTableData};
						this.actionURL = "http://10.160.24.112:7000/FaultDiagnosis/upload" + "?task_id="+id + "&file_name="+name+"&create_time="+time;
						console.log(this.actionURL);
						tempData.task_id = id;
						tempData.file_name = name;
						tempData.create_time = time;
						this.tableData.push(tempData);
						this.is_upload = true;
						this.$nextTick(() => resolve());
					}
					
				})
			},
			submitUpload(){
				this.$refs.upload.submit();
			},
            submitForm(formName) {
				this.$message.success("提交成功");
				this.dialogVisible = false;
				this.resetFromOther();
            },
            addToForm(event, file, fileList){
                console.log(file);
                console.log(fileList);
            },
			resetForm(form) {
				form.name = "";
				form.simulate_network = "";
				form.electrical_distance = "";
				console.log(this.is_upload);
				if(this.is_upload) {
					var task_id = this.tableData[this.tableData.length-1].task_id;
					axios.get("http://10.160.24.112:7000/FaultDiagnosis/delete", {
							params:{
								task_id:task_id
							}
						}).then(result => {
							console.log(result.data.message);
						})
					this.tableData.pop();
					this.is_upload = false;
				}
			},
			cellStyle({ row, column, rowIndex, columnIndex }) {
               if(column.property === 'level') {
                switch(row.level){
                    case '一级':
                    return {
                        color: '#cc0000',
                    }
                    break;
                    case '二级':
                    return {
                        color: '#ff8000',
                    }
                    break;
					case '三级':
                    return {
                        color: '#ffff00',
                    }
                    break;
                }
               }
            },
			resetFromOther() {
				this.form.name = "";
				this.form.simulate_network = "";
				this.form.electrical_distance = "";
			},
			search(name) {
				if(name == ""){
					this.$message.error("搜索名称不能为空");
				}
				else {
					const params = {...this.searchParam};
					params.file_name = name;
					axios.post("http://10.160.24.112:7000/FaultDiagnosis/search",params).then(result =>{
						this.tableData = result.data.data;
						this.$message.success("查询成功");
					})
				}
			}
		}
	}
</script>

<style scoped>

   
	.goodsindex {
		width: 100%;
		min-height: 100%;
		padding: 15px;
		box-sizing: border-box;
	}

	/* 搜索 */
	.goodsindex-queryInfo {
		margin-bottom: 20px;
		margin-left: 50%;
	}

	.goodsindex-queryInfo-li-one {
		width: 100%;
		height: auto;
		margin-left: 200%;

	}

	.goodsindex-queryInfo-li-two {
		width: 100%;
		height: auto;
		margin-left: 470%;
	}
	.goodsindex-queryInfo-li-three {
		width: 100%;
		height: auto;
		margin-left: 470%;
	}

	/* 列表 */
	.goodsindex-list {
		width: 100%;
		height: auto;
		margin-bottom: 20px;
		
	}

	/* 分页 */
	.goodsindex-page-box {
		width: 100%;
		height: auto;
		display: flex;
		justify-content: flex-end;
		margin-top: 20px;
	}

	.keycode-Info {
		width: 100%;
		margin-bottom: 15px;
	}

	.keycode-Info-li {
		margin-left: 1290%;
		margin-top: 15px;
	}

	.upload-demo {
		/* float: right; */
        margin-left:25% ;
	}
    .dialog-bottom-button {
        margin-left: 75%;
    }
	.result-list > div:nth-child(1) > img:nth-child(1) {
		width: 49%;
		display: inline;
	}
	.result-list > div:nth-child(1) > img:nth-child(2){
		width: 49%;
		display: inline;
	}
    .result-dialog /deep/ .el-dialog{
        background: #042224;
    }
</style>
<style>
	.el-popover {
		font-size: 10px;
		min-width: 50%;
		background: #303133;
  		color: #fff;
		max-width:30%;
    	padding-bottom: 5px!important;
    	display: -webkit-box;
    	overflow: hidden;
    	text-overflow: ellipsis;
    	-webkit-line-clamp: 30;
    	-webkit-box-orient: vertical;
		overflow-y:scroll;
		overflow-x:hidden;

	}
	.customWidth{
    	width:80%;
	}
     /* dialog */
     .menu-dialog-height {
        height: 65%;
    }
    .el-form-item__content{
        float: left;
        margin-left:5%;
    }
	 div.el-row:nth-child(1) {
		padding-left: 5%;
	}
</style>
