import React, { Component } from 'react'
import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export default class AdminProjecrProgressBar extends Component {
    render() {
        return (
            <div>
                <div className="card-block" style={{backgroundColor: "#eee"}}>
                    <div className="card-body text-dark">
                        <h2 className="card-title">Projects Progress</h2>
                        <div className="text-center" v-if="projectSpinner">
                            <span>Loading...</span>
                        </div>
                        <div v-if="!projectSpinner" className="table-responsive">

                            <table id="classTable" className="table table-bordered">
                                <thead className="bg-secondary">
                                    <tr className="text-white">
                                        <th colSpan="1"><strong>#</strong></th>
                                        <th><strong>Project Name</strong></th>

                                        <th><strong>Progress</strong></th>
                                    </tr>
                                </thead>

                                <tbody id="myText">

                                    <tr v-for="row,index in projects">
                                    <td>1</td>
                                    <td>2</td>


                                    <td>
                                        <span className="float-right"></span>
                                        <div className="progress bg-secondary">
                                            <div
                                                className="progress-bar bg-primary"
                                                role="progressbar">
                                                <span className="font-weight-bold">
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>  
            </div >
        )
    }
}
