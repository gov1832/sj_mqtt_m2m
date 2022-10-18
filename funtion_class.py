import json
import os
import time
import uuid

import paho.mqtt.client as mqtt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from drawclass_file import drawclass
from response_function import response_function
from log import Log_function
from datetime import datetime


class funtion_class(QWidget):
    def __init__(self, ui=None):
        super().__init__()
        if ui is not None:
            self.mainUi = ui
            self.mainUi.btnInit.clicked.connect(self.btnInit_clicked)
            self.mainUi.btnUninit.clicked.connect(self.btnUninit_clicked)
            self.mainUi.btnSub.clicked.connect(self.btnSub_clicked)
            self.mainUi.btnPub.clicked.connect(self.btnPub_clicked)
            # 실제 통신 테스트----------------------------------------------
            self.mainUi.btnSubT.clicked.connect(self.btnSubTest_clicked)
            # -----------------------------------------------------------
            self.setup_UI()
            self.btnState(False)
            self.table_counter = 0
            self.timer = QTimer(self)
            self.timer.setInterval(300)
            self.timer.timeout.connect(self.dataLabel_view)

            self.dc = drawclass()
            self.log = Log_function()
            # region Log
            exe_path = os.path.abspath(".")
            log_folder = "Log"
            folder_path = os.path.join(exe_path, log_folder)
            self.log.make_directory(folder_path=folder_path)
            # endregion
            global client

    def setup_UI(self):
        # self.mainUi.hostEdit.setText("211.250.184.225")
        # self.mainUi.portEdit.setText("5555")
        self.mainUi.hostEdit.setText("220.76.90.180")
        self.mainUi.portEdit.setText("1884")
        # self.mainUi.userEdit.setText("hbrain")
        # self.mainUi.pwEdit.setText("0372")
        self.mainUi.topicEdit.setText("/elsa/#")
        self.mainUi.floor_start.setValue(1)
        self.mainUi.floor_start.setMinimum(1)
        self.mainUi.floor_start.setMaximum(15)
        self.mainUi.floor_stop.setValue(1)
        self.mainUi.floor_stop.setMinimum(1)
        self.mainUi.floor_stop.setMaximum(15)
        self.mainUi.robotState_value.addItem("0: 대기")
        self.mainUi.robotState_value.addItem("1: 탑승완료")
        self.mainUi.robotState_value.addItem("2: 탑승취소")
        self.mainUi.robotState_value.addItem("3: 하차대기")
        self.mainUi.robotState_value.addItem("4: 하차완료")
        self.mainUi.robotState_value.addItem("5: 하차취소")
        # Subscribe Test Ui
        # call
        self.mainUi.sub_call.setEnabled(False)
        self.mainUi.call_result.addItem("00: 정상")
        self.mainUi.call_result.addItem("91: 등록X 로봇")
        self.mainUi.call_result.addItem("92: 등록X EV")
        self.mainUi.call_result.addItem("10: 호출 불가")
        # robot
        self.mainUi.sub_robot.setEnabled(False)
        self.mainUi.robot_result.addItem("00: 정상")
        self.mainUi.robot_result.addItem("91: 등록X 로봇")
        self.mainUi.robot_result.addItem("92: 등록X EV")
        # door
        self.mainUi.door_state.addItem("0: 열림")
        self.mainUi.door_state.addItem("1: 열림 중")
        self.mainUi.door_state.addItem("2: 닫힘")
        self.mainUi.door_state.addItem("3: 닫힘 중")
        # floor
        self.mainUi.floor_state.setValue(1)
        self.mainUi.floor_state.setMinimum(1)
        self.mainUi.floor_state.setMaximum(15)
        # arrival
        self.mainUi.arrival_state.setValue(1)
        self.mainUi.arrival_state.setMinimum(1)
        self.mainUi.arrival_state.setMaximum(15)
        self.mainUi.arrival_info.setValue(1)
        self.mainUi.arrival_info.setMinimum(1)
        self.mainUi.arrival_info.setMaximum(2)

    def btnState(self, b):
        self.mainUi.btnInit.setEnabled(not b)
        self.mainUi.btnUninit.setEnabled(b)
        self.mainUi.btnSub.setEnabled(b)
        self.mainUi.btnSubT.setEnabled(b)
        self.mainUi.btnPub.setEnabled(b)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("connected error")

    def on_disconnect(self, client, userdata, flags, rc=0):
        print(str(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("subscribe OK")

    def on_message(self, client, userdata, msg):
        self.subMsg_parsing(msg)

    def btnInit_clicked(self):
        host = self.mainUi.hostEdit.toPlainText()
        port = int(self.mainUi.portEdit.toPlainText())
        user = self.mainUi.userEdit.toPlainText()
        pswd = self.mainUi.pwEdit.text()

        global client
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        # client.username_pw_set(username=user, password=pswd)
        client.connect(host, port)
        client.loop_start()

        self.rf = response_function(client=client, ui=self.mainUi)
        self.btnState(True)

        self.timer.start()

    def btnUninit_clicked(self):
        client.loop_stop()
        self.timer.stop()

        self.btnState(False)

    def btnSub_clicked(self):
        topic = self.mainUi.topicEdit.toPlainText()
        client.subscribe(topic, 1)

    def btnPub_clicked(self):
        if self.mainUi.ev_call_check.isChecked():
            self.pub_evCall()
        if self.mainUi.robot_check.isChecked():
            self.pub_robotState()

    # def pub_evCall(self):
    #     print("----ev_call----")
    #     id = str(uuid.uuid1())
    #     elsa_id = "elsa-1"
    #     elevator_id = "elevator-1"
    #     robot_id = "robot-1"
    #     floor_start = int(self.mainUi.floor_start.value())
    #     floor_stop = int(self.mainUi.floor_stop.value())
    #     topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/call"
    #     client.publish(topic, json.dumps({"id": id,
    #                                       "type": 0,
    #                                       "origin": floor_start,
    #                                       "destination": floor_stop
    #                                       }))
    #
    # def pub_robotState(self):
    #     print("----robot_state----")
    #     id = str(uuid.uuid1())
    #     elsa_id = "elsa-1"
    #     elevator_id = "elevator-1"
    #     robot_id = "robot-1"
    #     state = int(self.mainUi.robotState_value.currentIndex())
    #     topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/state"
    #     client.publish(topic, json.dumps({"id": id, "state": state}))

    # EV 관제 시스템 Publish ---------------------
    def btnSubTest_clicked(self):
        try:
            req_id = uuid.uuid1()
            if self.mainUi.sub_status.isChecked():
                self.pub_systemStatus()
            elif self.mainUi.sub_call.isChecked():
                self.pub_evCall_response(req_id)
            elif self.mainUi.sub_robot.isChecked():
                self.pub_robotState_response(req_id)
            elif self.mainUi.sub_door.isChecked():
                self.pub_doorState()
            elif self.mainUi.sub_floor.isChecked():
                self.pub_evFloor()
            elif self.mainUi.sub_arrival.isChecked():
                self.pub_evArrival()
        except Exception as e:
            print("btnSubTest_clicked error: ", e)

    def pub_systemStatus(self):
        try:
            print("----system_status----")
            elsa_id = "elsa-1"
            topic = "/elsa/" + elsa_id +"/system/status"
            id = str(uuid.uuid1())
            elsa_status_sub = False
            ev_status_sub = False
            if self.mainUi.elsa_status.isChecked():
                elsa_status_sub = True
            if self.mainUi.EV_status.isChecked():
                ev_status_sub = True
            client.publish(topic, json.dumps({"enabled": elsa_status_sub,
                                              "elevators": [{
                                                  "id": id,
                                                  "enabled": ev_status_sub
                                              }]
                                              }))
        except Exception as e:
            print("pub_systemStatus error: ", e)

    def pub_evCall_response(self, id):
        try:
            print("----ev_call----")
            elsa_id = "elsa-1"
            elevator_id = "ev-204-1"
            robot_id = "wmr001"
            topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/call/response"
            result = 0
            if self.mainUi.call_result.currentIndex() == 0:
                result = 0
            elif self.mainUi.call_result.currentIndex() == 1:
                result = 91
            elif self.mainUi.call_result.currentIndex() == 2:
                result = 92
            elif self.mainUi.call_result.currentIndex() == 3:
                result = 10
            client.publish(topic, json.dumps({"id": id,
                                              "result": result}))
        except Exception as e:
            print("pub_evCall_response error: ", e)

    def pub_robotState_response(self, id):
        try:
            print("----robot_State----")
            elsa_id = "elsa-1"
            elevator_id = "ev-204-1"
            robot_id = "wmr001"
            topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/state/response"
            result = 0
            if self.mainUi.robot_result.currentIndex() == 0:
                result = 0
            elif self.mainUi.robot_result.currentIndex() == 1:
                result = 91
            elif self.mainUi.robot_result.currentIndex() == 2:
                result = 92

            client.publish(topic, json.dumps({"id": id,
                                              "result": result}))
        except Exception as e:
            print("pub_robotState_response error: ", e)

    def pub_doorState(self):
        try:
            print("----door----")
            elsa_id = "elsa-1"
            elevator_id = "ev-204-1"
            robot_id = "wmr001"
            topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/door/state"
            result = self.mainUi.door_state.currentIndex()
            client.publish(topic, json.dumps({"state": result}))
        except Exception as e:
            print("pub_doorState error: ", e)

    def pub_evFloor(self):
        try:
            print("----ev_floor----")
            elsa_id = "elsa-1"
            elevator_id = "ev-204-1"
            robot_id = "wmr001"
            topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/floor"
            floor = int(self.mainUi.floor_state.value())
            client.publish(topic, json.dumps({"floor": floor}))
        except Exception as e:
            print("pub_evFloor error: ", e)

    def pub_evArrival(self):
        try:
            print("----ev_arrival----")
            elsa_id = "elsa-1"
            elevator_id = "ev-204-1"
            robot_id = "wmr001"
            topic = "/elsa/" + elsa_id + "/elevator/" + elevator_id + "/robot/" + robot_id + "/arrival"
            info = int(self.mainUi.arrival_info.value())
            floor = int(self.mainUi.arrival_state.value())
            client.publish(topic, json.dumps({"info": info,
                                                   "floor": floor}))
        except Exception as e:
            print("pub_evArrival error: ", e)
    # -------------------------------------------

    def subMsg_parsing(self, msg):
        temp = msg.topic.split('/')
        log_list = ["", "", "", ""]
        log_list[0] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_list[1] = "PUB"
        log_list[2] = msg.topic
        log_list[3] = msg.payload

        elsa_id = temp[2]
        if temp[3] == 'system':
            self.rf.sub_systemStatus(msg)
        elif temp[3] == 'elevator':
            if temp[5] == 'robot':
                if temp[7] == 'call':
                    self.rf.sub_EVCall(msg)
                    if len(temp) < 9:
                        log_list[1] = "SUB"
                elif temp[7] == 'state':
                    self.rf.sub_RobotState(msg)
                    if len(temp) < 9:
                        log_list[1] = "SUB"
                elif temp[7] == 'arrival':
                    self.rf.sub_EVarrival(msg)
                elif temp[7] == 'door':
                    self.rf.sub_EVdoor(msg)
                elif temp[7] == 'floor':
                    self.rf.sub_EVfloor(msg)
        self.log.log_save(log_list)
        self.table_view(log_list)

    def table_view(self, msg_list):
        self.mainUi.dataList_m2m.setRowCount(self.mainUi.dataList_m2m.rowCount() + 1)
        for i in range(4):
            if i == 0:
                self.table_item = str(msg_list[0])
            elif i == 1:
                self.table_item = str(msg_list[1])
            elif i == 2:
                self.table_item = str(msg_list[2])
            elif i == 3:
                self.table_item = str(msg_list[3])
            self.mainUi.dataList_m2m.setItem(self.table_counter, i, QTableWidgetItem(self.table_item))
        self.table_counter += 1
        self.mainUi.dataList_m2m.scrollToBottom()
        self.mainUi.dataList_m2m.resizeColumnsToContents()

    def dataLabel_view(self):
        self.mainUi.systemStatus_label.setText(str(self.rf.G_elsa_status))
        self.mainUi.EVStatus_label.setText(str(self.rf.G_ev_status))
        self.mainUi.EV_now_floor.setText(str(self.rf.G_ev_now_floor))
        self.mainUi.EV_now_door.setText(str(self.rf.G_ev_now_door))
        self.mainUi.EV_arrival_floor.setText(str(self.rf.G_ev_arrival_floor))
        if self.rf.G_robot_state == 0:
            self.mainUi.robot_state.setText("탑승 대기")
        elif self.rf.G_robot_state == 1:
            self.mainUi.robot_state.setText("탑승 완료")
        elif self.rf.G_robot_state == 2:
            self.mainUi.robot_state.setText("탑승 취소")
        elif self.rf.G_robot_state == 3:
            self.mainUi.robot_state.setText("하차 대기")
        elif self.rf.G_robot_state == 4:
            self.mainUi.robot_state.setText("하차 완료")
        elif self.rf.G_robot_state == 5:
            self.mainUi.robot_state.setText("하차 취소")

        self.dc.get_EVData(self.rf.G_ev_now_floor, self.rf.G_ev_now_door, self.rf.G_ev_arrival_floor)
        self.dc.get_RobotData(self.rf.G_robot_state, self.rf.G_ev_now_floor)
