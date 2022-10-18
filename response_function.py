import json
import uuid

class response_function:
    def __init__(self, client, ui):
        super().__init__()
        self.client = client
        self.mainUi = ui
        self.G_elsa_status = False
        self.G_ev_status = False
        self.G_ev_now_floor = 1
        self.G_ev_now_door = "Close"
        self.G_ev_arrival_floor = 1
        self.G_robot_state = 0

    def sub_systemStatus(self, msg):
        # self.table_view(msg, 0)
        print("Sub topic:   system Status")
        sub_msg = json.loads(str(msg.payload.decode("utf-8")))
        elsa_status = sub_msg.get("enabled")
        elevator_info = sub_msg.get("elevators")
        elevator_id = ""
        elevator_enabled = False
        for list in elevator_info:
            elevator_id = list.get("id")
            elevator_enabled = list.get("enabled")
        print("Sub Message: status:" + str(elsa_status) + " /elevator_id: " + str(
            elevator_id) + " /elevator_enabled:" + str(
            elevator_enabled))
        # Data save
        self.G_elsa_status = elsa_status
        self.G_ev_status = elevator_enabled

    def sub_EVCall(self, msg):
        temp = msg.topic.split('/')
        if len(temp) > 8: # response
            # self.table_view(msg, 0)
            print("Pub topic:   EVCall_Response")
            sub_msg = json.loads(str(msg.payload.decode("utf-8")))
            sub_id = sub_msg.get("id")
            sub_result = sub_msg.get("result")
            print("Pub Message: pub_id:" + str(sub_id) + " /pub_result: " + str(sub_result))
        else:
            print("Sub topic: EVCall")
            # self.table_view(msg, 1)
            pub_msg = json.loads(str(msg.payload.decode("utf-8")))
            pub_id = pub_msg.get("id")
            pub_type = pub_msg.get("type")
            pub_origin = pub_msg.get("origin")
            pub_destination = pub_msg.get("destination")
            print("Sub Message: sub_id:" + str(pub_id) + " /sub_type: " + str(pub_type) + " /sub_origin: " + str(
                pub_origin) + " /sub_destination: " + str(pub_destination))
            self.pub_evCall_response(pub_id)

    def sub_RobotState(self, msg):
        temp = msg.topic.split('/')
        if len(temp) > 8:
            # self.table_view(msg, 0)
            print("Pub topic:   RobotState_Response")
            sub_msg = json.loads(str(msg.payload.decode("utf-8")))
            sub_id = sub_msg.get("id")
            sub_result = sub_msg.get("result")
            print("Pub Message: pub_id:" + str(sub_id) + " /pub_result: " + str(sub_result))
        else:
            # self.table_view(msg, 1)
            print("Sub topic:   RobotState")
            pub_msg = json.loads(str(msg.payload.decode("utf-8")))
            pub_id = pub_msg.get("id")
            pub_state = pub_msg.get("state")
            print("Sub Message: sub_id:" + str(pub_id) + " /sub_state: " + str(pub_state))
            self.pub_robotState_response(pub_id)
            self.G_robot_state = pub_state

    def sub_EVarrival(self, msg):
        # self.table_view(msg, 0)
        print("Pub topic:   EV arrival")
        sub_msg = json.loads(str(msg.payload.decode("utf-8")))
        ev_info = sub_msg.get("info")
        ev_floor = sub_msg.get("floor")
        print("Pub Message: info: " + str(ev_info) + "/ev_floor:" + str(ev_floor))
        # Data save
        self.G_ev_arrival_floor = ev_floor

    def sub_EVdoor(self, msg):
        # self.table_view(msg, 0)
        print("Pub topic:   EVdoor")
        sub_msg = json.loads(str(msg.payload.decode("utf-8")))
        ev_door = sub_msg.get("state")
        print("Pub Message: ev_door:" + str(ev_door))
        # Data save
        if ev_door == 0:
            self.G_ev_now_door = "open"
        elif ev_door == 1:
            self.G_ev_now_door = "opening"
        elif ev_door == 2:
            self.G_ev_now_door = "close"
        elif ev_door == 3:
            self.G_ev_now_door = "closing"

    def sub_EVfloor(self, msg):
        # self.table_view(msg, 0)
        print("Pub topic:   EVfloor")
        sub_msg = json.loads(str(msg.payload.decode("utf-8")))
        ev_floor = sub_msg.get("floor")
        print("Pub Message: ev_floor:" + str(ev_floor))
        # Data save
        self.G_ev_now_floor = ev_floor

    def pub_systemStatus(self):
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
        self.client.publish(topic, json.dumps({"enabled": elsa_status_sub,
                                          "elevators": [{
                                              "id": id,
                                              "enabled": ev_status_sub
                                          }]
                                          }))

    def pub_evCall_response(self, id):
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
        self.client.publish(topic, json.dumps({"id": id,
                                          "result": result}))

    def pub_robotState_response(self, id):
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

        self.client.publish(topic, json.dumps({"id": id,
                                          "result": result}))

    # -------------------------------------------