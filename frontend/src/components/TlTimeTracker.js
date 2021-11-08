import React, { Component } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import moment from 'moment/moment.js';
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const options = JSON.parse(taskStatusListAccess)



//const taskStatusTimerViewAccess = JSON.parse(taskStatusTimerViewAccess)



export default class TlTimeTracker extends React.Component {
    constructor(props) {
        super(props)
        this.state = {

            timerOn: false,
            timerStart: 0,
            timerTime: 0,

            options: options,
            time: "00:00:00.000",
            dirty_form: false,
            baseUrl: null,
            baseSegment: null,
            todayDate: "0000-00-00",
            started: false,
            seconds: 0,
            minutes: 0,
            hours: 0,
            timeBegan: null,
            timeStopped: null,
            stoppedDuration: 0,
            started: null,
            running: false,
            taskSpinner: false,
            task: null,
            todayTakenDuration: null,
            subTaskSpinner: false,
            subTask: [],
            taskLogsSpinner: true,
            taskLogs: [],
            taskLog: {},
            taskStatusSpinner: true,
            checkProcessStatusViewAccess:false,
            submitSpinner: false,
            taskStatus: [],
            value: '',
            form: {
                status: '',
                note: '',
            },


        }


        this.formSubmit = this.formSubmit.bind(this);
    }


    handleStatusChange = (val) => {
        this.setState({ form: { ...this.state.form, status: val.target.value } }, () => {

        })
    }
    handleNoteChange = (val) => {
        this.setState({ form: { ...this.state.form, note: val.target.value } }, () => {

        })
    }

    componentDidMount = () => {
       
        this.checkProcessStatusViewAccess()
        
        this.task = task

        setInterval(() => {

        }, 5000);
        this.getAjaxTask()


    }

    componentWillUnmount() {
        //clearInterval(this.state.started)
    }
    updateIntervalTime() {

    }
    checkProcessStatusViewAccess = (task,subTask) => {
       
       
        if (!task) return false;
        
        let processStatus = taskStatusTimerViewAccess;
       
        if(task.parent_id){
            return false;
        }
        else{
            if(task.status == "active" &&
            processStatus.indexOf(task.process_status) != -1) {return true}
            else return false;
        }
        
      }

    startTimer = () => {

        this.state.dirty_form = true;
        this.state.running = true;
        
        this.setState({
            timerOn: true,
            timerTime: this.state.timerTime,
            timerStart: Date.now() - this.state.timerTime
        });
        this.timer = setInterval(() => {
            this.setState({
                timerTime: Date.now() - this.state.timerStart
            });
        }, 10);
        this.storeTaskTime();

    };

    stopTimer = () => {
        this.setState({ timerOn: false });
        this.timeStopped = new Date();
        
        clearInterval(this.timer);
        this.updateTaskTime();
        this.state.dirty_form = false;
        
    };

    resetTimer = () => {
        this.setState({
            timerStart: 0,
            timerTime: 0
        });
    };



    formSubmit() {
        this.state.submitSpinner = true
        if (!this.state.form.status) {
            alert("Please select status");
            return false
        } else {
          
            let postForm = this.state.form
            console.log("postForm-->",postForm)
            axios.post(baseSegment + '/updateStatus/' + tasksId, postForm)  
                .then(response => {

                    setTimeout(() => {
                            //window.location.reload();
                    this.getAjaxTask();

                    }, 1000);
                        let td = response
                       

                }
                )   
                .catch(errors => { this.submitSpinner = false; console.log(errors) })
        }
    }
     storeTaskTime = () => {
        
         this.state.taskSpinner = true;

         axios.get(baseSegment + '/storeTime/' + tasksId)  
             .then(response => {
               
                 this.getAjaxTask();
             })
             .catch(err => { console.log("Error: " + err) })
     }

     updateTaskTime = () => {     
     this.state.taskSpinner = true;
     this.state.taskLogsSpinner = true;
   
     axios.get(baseSegment + '/updateTime/' + tasksId) 
             .then(response => {
            //console.log("update task time--->",response) 
            this.getAjaxTask();
                
            this.setState({
                 taskSpinner : false,
             });
             })
             .catch(err => { console.log("Error: " + err) })

     }


    getAjaxTask = () => {
      
            this.state.subTaskSpinner = true;
            this.subTask = [];
        axios.get(baseSegment + '/getAjaxTask/' + tasksId) // 1
            .then(response => {
                console.log("TL tasks")
                this.subTaskSpinner = true;
                this.subTask = [];

                let sbtsk = response.data;
                this.subTask = sbtsk.subTask

                let tld = response.data;         
                this.data = tld.task;
                this.setState({

                    task: this.data
                   
                });
                task = this.state.task[0].fields
                setTimeout(() => {
                        this.state.form.status = task.process_status;
                        this.setState({
                        subTask:this.subTask,
                        subTaskSpinner:false,
                        todayDate : response.data.todayDate,
                        });  
                    // subTask  = this.state.subTask            
                     this.getAjaxTaskLogs();
                     this.getAjaxTaskStatus();
                    }, 2000);
                })
                .catch(err => { console.log("Error: " + err) })

        }

     getAjaxTaskLogs = () => {
         this.state.taskLogsSpinner = true;

         axios.get(baseSegment + '/getAjaxTaskLog/' + tasksId)  
             .then(response => {             
                                  
                 let tld = response.data;
                 this.data = tld.task;
                 this.ttd = tld.todayduration;

                 this.setState({
                     submitSpinner: false,
                     taskLogs: this.data,
                     taskLogsSpinner: false,
                     todayTakenDuration:this.ttd,
                 });
             })
             .catch(err => { console.log("Error: " + err) })



    }

     getAjaxTaskStatus = () => {
        
         this.state.taskStatusSpinner = true;
       
         axios.get(baseSegment + '/getAjaxTaskStatus/' + tasksId)  
             .then(response => {                               
                 
                 let tld = response.data;
                 this.data = tld.taskStatus;

                 this.setState({
                     taskStatus: this.data,
                    //  user: tld.user,

                     taskStatusSpinner: false

                 });
             })
             .catch(err => { console.log("Error: " + err) })

     }

    zeroPrefix(num, digit) {
        var zero = "";
        for (var i = 0; i < digit; i++) {
          zero += "0";
        }
        return (zero + num).slice(-digit);
      }
   
    render() {
      
        const { timerTime } = this.state;
        let centiseconds = ("0" + (Math.floor(timerTime / 10) % 100)).slice(-2);
        let seconds = ("0" + (Math.floor(timerTime / 1000) % 60)).slice(-2);
        let minutes = ("0" + (Math.floor(timerTime / 60000) % 60)).slice(-2);
        let hours = ("0" + Math.floor(timerTime / 3600000)).slice(-2);
    
        this.time =
        this.zeroPrefix(hours, 2) +
        ":" +
        this.zeroPrefix(minutes, 2) +
        ":" +
        this.zeroPrefix(seconds, 2) +
        "." +
        this.zeroPrefix(centiseconds, 3);

       
        return (

            <div><br />

                <div id="task_tracker" className="container0">
                   
                    <div className="justify-content-center">
                      
                    {this.checkProcessStatusViewAccess(task,this.state.subTask) ? 
                        <div className="row p-2 text-white" style={{
                            WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                            MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                            boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#014047"
                        }}>
                            <div className="col-md-2 mb-2 text-center">
                                <div>
                                    <strong>Today Date:</strong> <br />
                                    {this.state.todayDate?this.state.todayDate:'Not Available'}
                                </div>
                                <div>
                                    <strong>Today Duration:</strong> <br />
                                    {this.state.todayTakenDuration ? this.state.todayTakenDuration + " min":'00:00:00:00'}
                                </div>
                                
                            </div>
                            <div className="col-md-4 mb-2 text-center border border-5px rounded" style={{
                                WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#01434a"
                            }}>
                                <div className="Stopwatch">

                                    <div className="Stopwatch-display">
                                       <span className="display-6 font-weight-normal"> {hours}:{minutes}:{seconds}:{centiseconds}</span>
                                    </div>
                                    <div className="mt-3">
                                    {this.state.timerOn === false && this.state.timerTime === 0 && (
                                        <button onClick={this.startTimer} className="btn btn-primary"><i className="fas fa-play-circle fa-sm"></i>Start</button>
                                    )}
                                    {this.state.timerOn === true && (
                                        <button onClick={this.stopTimer} className="btn btn-warning"><i className="fas fa-pause-circle fa-sm"></i>Stop</button>
                                    )}
                                    {this.state.timerOn === false && this.state.timerTime > 0 && (
                                        <button onClick={this.startTimer} className="btn btn-success mx-1" ><i className="fas fa-play-circle fa-sm"></i>Resume</button>
                                    )}
                                    {this.state.timerOn === false && this.state.timerTime > 0 && (
                                        <button onClick={this.resetTimer} className="btn btn-danger"><i className="fas fa-undo fa-xs"></i>Reset</button>
                                    )}
                                    </div>
                                </div>
                                {
                                    this.taskSpinner === true ? <div>
                                        <i className="fas fa-spinner fa-spin"></i>
                                    </div> : ''

                                }

                            </div>
                            <div className="col-md-3">
                                <div className="form-group" >
                                    <textarea value={this.state.form.note} onChange={this.handleNoteChange} className="form-control" style={{ backgroundColor: "#eee" }} rows="4" placeholder="Note"></textarea>
                                </div>
                            </div>
                            <div className="col-md-3 mb-2 text-center">
                                <div className="input-group" >
                                    <div className="input-group-prepend">
                                        <div className="input-group-text">Status</div>
                                    </div>
                                    <select disabled={this.state.taskLogs.length <= 0} value={this.state.form.status} onChange={this.handleStatusChange} className="form-control" >
                                        <option value="">Select</option>
                                        {options.map((ab, index) => <option className="form-control" key={index} value={Object.keys(ab)} >{Object.values(ab)}</option>)}
                                    </select>
                                </div>
                                <div className="form-group mt-3">
                                   
                                    <button disabled={this.state.submitSpinner || this.state.taskLogs.length <= 0} type="button" className="btn btn-primary" onClick={this.formSubmit}>
                                        Update
                                        {this.state.submitSpinner ?
                                            <span><i className="fas fa-spinner fa-spin"></i></span>
                                            : ''}
                                    </button>
                                </div>
                            </div>
                            
                        </div>
                        
                        : ''}

                        {this.checkProcessStatusViewAccess(task,this.state.subTask) ? 
                        <div style={{ borderBottom: "3px solid #02c72d" }}></div>
                        : ''}
                        <br/>
                        {task ?
                            <div className="row border p-2 text-white" style={{
                                WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#014047"
                            }}>
                                <div className="col-md-3">
                                    <div>
                                        <strong>Total Time:</strong><br />
                                        {task.work_duration} min.
                                    </div>
                                    <div>
                                        <strong>Work started at: </strong><br />
                                        {task.work_started_at ? moment(task.work_started_at).format('YYYY-MM-DD hh:mm:ss A'):'Not Available'}
                                    </div>
                                    <div>
                                        <strong>Work ended at: </strong><br />
                                        {task.work_started_at ? moment(task.work_ended_at).format('YYYY-MM-DD hh:mm:ss A'):'Not Available'}
                                    </div>
                                    <div>
                                        <strong>Total duration:</strong><br />
                                        {task.task_duration} | {task.work_duration} min.
                                    </div>

                                </div>

                                <div className="col-md-2 ">

                                    <div>
                                        <strong>Is Sub-Task ?:</strong>
                                        <span className={`badge badge-pill ${task.parent_id == 0 ? 'badge-success':'badge-warning'}`}>
                                         {task.parent_id ? "YES" : "NO"} | {task.parent_id}
                                        </span>
                                        <span className="{'badge badge-pill badge-success': task.parent_id == 0,'badge badge-pill badge-warning': task.parent_id > 0}">
                                           </span>

                                    </div>

                                    <div>
                                        <strong>Status</strong>:<br />
                                        <span className={`badge badge-pill ${task.status == 'active' ? 'badge-success':'badge-warning'}`}>
                                            {task.status}</span>
                                    </div>

                                    <div>
                                        <strong> Process Status: </strong><br />
                                        <span className="badge badge-pill badge-secondary">{task.process_status}</span>
                                    </div>
                                </div>

                                <div className="col-md-6">
                                    <div>
                                        <strong>TaskID</strong> :
                                        {task.taskid ? task.taskid : "-"}
                                    </div>
                                    <div>
                                        <strong>Task name</strong><br />
                                        {task.name ? task.name : "-"}
                                    </div>
                                    <div>
                                        <strong>Description</strong><br />
                                        {task.description ? task.description : "-"}
                                    </div>
                                    <div>
                                        <strong>Priority : </strong><br />
                                                    {task.priority == 'extreme high' ? 
                                                    <span className="badge badge-pill badge text-white extreme_high_task" style={{backgroundColor: "#8C370D"}}>{task.priority}</span> 
                                                    :''} 

                                                    {task.priority == 'high' ? 
                                                    <span className="badge badge-pill badge-danger">{ task.priority }</span> 
                                                    :''}

                                                    {task.priority == 'medium' ? 
                                                    <span className="badge badge-pill badge-warning">{ task.priority }</span>
                                                    :''}

                                                    {task.priority == 'low' ? 
                                                    <span className="badge badge-pill badge-primary">{task.priority}</span>
                                                    :''}

                                                    {task.priority == null ?
                                                    <span className="badge badge-pill badge-secondary">Not Available</span>
                                                    :''}
                                    </div>
                                    
                                </div>

                            </div>

                            : ''
                        }
                        <br />
                        {task ? 
                        <div className="row">
                            
                            {task.parent_id == 0 && this.state.subTask.length > 0 ? 
                            <div className="col-md-12">
                                <div><strong>Sub-Tasks</strong></div>
                                <div className="table-responsive">
                                    <table className="table table-sm table-hover">
                                        <thead className="text-white" style={{
                                            WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#014047", borderBottom: "3px solid #02b2ed"
                                        }}>
                                            <tr>
                                            <th width="5%">#</th>
                                            <th width="5%">ID</th>
                                            <th width="10%">Name</th>
                                            <th width="10%">Description</th>
                                            <th width="10%">Started At</th>
                                            <th width="10%">Ended At</th>
                                            <th width="10%">Duration</th>
                                            <th width="10%">Status</th>
                                            <th width="10%">P. Status</th>
                                            <th width="10%">Created By</th>
                                            <th width="10%">Priority</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {this.state.subTaskSpinner ?
                                            <tr v-if="subTaskSpinner">
                                            <td colSpan="10" align="center">
                                                <i className="fas fa-spinner fa-spin"></i> loading...
                                            </td>
                                            </tr>
                                            :<tr></tr>}
                                            {!this.state.subTaskSpinner && this.state.subTask.length == 0 ?
                                            <tr>
                                            <td colSpan="10" align="center">No data found.</td>
                                            </tr>
                                            :<tr></tr>}
                                            
                                            {this.state.subTask.length > 0 && this.state.subTaskSpinner == false ? this.state.subTask.map((row, index) => (
                                            <tr key={index}>  
                                                
                                                <td width="5%">{ index + 1 }.</td>
                                                <td width="5%">{ row.pk }</td>
                                                
                                                <td width="10%">{ row.fields.name }</td>
                                                <td width="10%">{ row.fields.description }</td>
                                                <td width="10%">{ moment(row.fields.work_started_at).format('DD-MM-YYYY') }</td>
                                                <td width="10%">{ moment(row.fields.work_ended_at).format('DD-MM-YYYY') }</td>
                                                <td width="10%">{ row.fields.work_duration ? row.fields.work_duration : "-" }</td>
                                                <td width="10%">{ row.fields.status }</td>
                                                <td width="10%">{row.fields.process_status }</td>
                                                <td width="10%">
                                                    {moment(row.fields.created_at).format('DD-MM-YYYY') }
                                                </td>
                                                <td width="10%">
                                                    {row.fields.priority == 'extreme high' ? 
                                                    <span className="badge badge-pill badge text-white extreme_high_task" style={{backgroundColor: "#8C370D"}}>{row.fields.priority}</span> 
                                                    :''} 

                                                    {row.fields.priority == 'high' ? 
                                                    <span className="badge badge-pill badge-danger">{ row.fields.priority }</span> 
                                                    :''}

                                                    {row.fields.priority == 'medium' ? 
                                                    <span className="badge badge-pill badge-warning">{ row.fields.priority }</span>
                                                    :''}

                                                    {row.fields.priority == 'low' ? 
                                                    <span className="badge badge-pill badge-primary">{row.fields.priority}</span>
                                                    :''}

                                                    {row.fields.priority == null ?
                                                    <span className="badge badge-pill badge-secondary">Not Available</span>
                                                    :''}
                                                </td>
                                            
                                            </tr>
                                            
                                            ))
                                            : <tr></tr>}
                                        </tbody>    
                                    </table>    
                                </div>    
                            </div>
                            :''}
                        </div>
                        :''}
                        <div className="row" >
                            <div className="col-md-6" >
                                <div>
                                    <strong>Task Time Logs</strong>  min.
                                </div>

                                <div className="table-responsive">
                                    <table className="table table-sm table-hover">
                                        <thead className="text-white" style={{
                                            WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#014047", borderBottom: "3px solid #02b2ed"
                                        }}>
                                            <tr >
                                                <th width="5%">#</th>
                                                <th width="10%">ID</th>
                                                <th width="20%">Start At</th>
                                                <th width="20%">End At</th>
                                                <th width="15%">Duration</th>
                                                <th width="20%">Created At</th>

                                            </tr>
                                        </thead>

                                        <tbody>

                                            {this.state.taskLogsSpinner ?
                                                <tr>
                                                    <td colSpan="7" align="center">
                                                        <i className="fas fa-spinner fa-spin"></i> loading...
                                                    </td>
                                                </tr>
                                                : <tr></tr>}

                                            {this.state.taskLogs.length == 0 && !this.state.taskLogsSpinner ?
                                                <tr>
                                                    <td colSpan="7" align="center">No data found.</td>
                                                </tr>
                                                : <tr></tr>}
                                            {this.state.taskLogs.length > 0 && this.state.taskLogsSpinner == false ? this.state.taskLogs.map((task, index) => (

                                                <tr key={index}>

                                                    <td width="5%">{index + 1}</td>
                                                    <td width="10%">{task.pk}</td>
                                                    <td width="20%">{moment(task.fields.work_started_at).format('hh:mm:ss A')}</td>
                                                    <td width="20%">{task.fields.work_ended_at ? moment(task.fields.work_ended_at).format('hh:mm:ss A'):'-'}</td>
                                                    <td width="15%">{task.fields.work_duration} min.</td>
                                                    <td width="20%">{moment(task.fields.created_at).format('DD-MM-YYYY')}
                                                        <br /><span
                                                            className="timesmall">
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))

                                                : <tr></tr>}


                                        </tbody>

                                    </table>
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div><strong>Task Process Status</strong></div>
                                <div className="table-responsive">
                                    <table className="table table-sm table-hover">
                                        <thead className="text-white" style={{
                                            WebkitBoxshadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            MozBoxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)",
                                            boxShadow: "0px 0px 4px 0px rgba(50, 50, 50, 0.79)", backgroundColor: "#014047", borderBottom: "3px solid #02b2ed"
                                        }}>

                                            <tr>
                                                <th width="5%">#</th>
                                                <th width="10%">ID</th>
                                                <th width="20%">Status</th>
                                                <th width="30%">Note</th>
                                                <th width="20%">Status By</th>
                                                <th width="20%">Created At</th>
                                            </tr>

                                        </thead>
                                        <tbody>
                                            {this.state.taskStatusSpinner ?
                                                <tr>
                                                    <td colSpan="7" align="center">
                                                        <i className="fas fa-spinner fa-spin"></i> loading...
                                                    </td>
                                                </tr>
                                                : <tr></tr>}

                                            {this.state.taskStatus.length == 0 && !this.state.taskStatusSpinner ?
                                                <tr>
                                                    <td colSpan="7" align="center">No data found.</td>
                                                </tr>
                                                : <tr></tr>}

                                            {this.state.taskStatus.length > 0 && this.state.taskStatusSpinner == false ? this.state.taskStatus.map((taskStatus, index) => (
                                                <tr key={index}>
                                                    <td width="5%">{index + 1}</td>
                                                    <td width="10%">{taskStatus.id}</td>
                                                    
                                                    <td width="20%"><span
                                                    className={`badge badge pill ${taskStatus.status == 'forwarded_to_tl' || taskStatus.status == 'forwarded_to_qc'? 'badge-secondary' : (taskStatus.status=='active'? 'badge-success':(taskStatus.status=='qc_rejected' || taskStatus.status=='tl_rejected'? 'badge-danger':(taskStatus.status == 'completed' ? 'badge-success':'text-dark')))}`}
                                                    >{taskStatus.status}</span></td>
                                                    <td width="30%">{taskStatus.note ? taskStatus.note : '-'}</td>
                                                    <td width="20%">{taskStatus.user_id ? taskStatus.user_id : '-'}</td>
                                                    <td width="20%">{moment(taskStatus.created_at).format('DD-MM-YYYY')}</td>
                                                </tr>
                                            ))
                                                : <tr></tr>}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );

    }

}