# coding=UTF-8
from __future__ import division
import socket
import numpy as np

SIZE = 1024 * 1024*2
import json
import random
import re
import os


# EP_MAX = 100000
# EP_LEN = 4500
# N_WORKER = 1  # parallel workers
# frams = 6

class Env():
    def __init__(self, IP, port):
        self._ip = IP
        self._port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SIZE)
        self.client.connect((self._ip, self._port))

    # def _recv(self):
    #     try:
    #         data = self.client.recv(SIZE)
    #         data = data.decode(encoding="utf-8")
    #         return data
    #     except:
    #         print("socket error,Nothing received")

    def _recv(self):
        result = self.client.recv(SIZE)
        result = result.decode(encoding="utf-8")
        while 1:
            num_lcount = result.count('{')
            num_rcount = result.count('}')
            if num_lcount == num_rcount:
                break
            result1 = self.client.recv(SIZE)
            result1 = result1.decode(encoding="utf-8")
            result = result + result1

        # 粘包处理
        if result.count("}{") != 0:
            pos = result.rfind("}{")
            result = result[pos + 1:]
        dataBuffer = list()
        for i in range(result.count("}{")):
            pos = result.find("}{")
            dataStr = result[0:pos + 1]
            result = result[pos + 1:]
            dataBuffer.append(dataStr)
        dataBuffer.append(result)
        # tail = tail.decode(encoding="utf-8")
        return dataBuffer[0]
    def _send(self, message):
        try:
            # print("send", message)
            self.client.send(str(message).encode('utf-8'))
            result = self._recv()
            # print("recv", result);
            return result
        except:
            print("socket error,{} not send".format(str(message)))

    def Step(self, Action=None):
        command = {"CMD": "Step"}
        if Action != None:
            command.update(Action)
        command = json.dumps(command)
        result = self._send(command)
        return result

    def Reset(self):
        command = {"CMD": "Reset"}
        command = json.dumps(command)
        result = self._send(command)
        return result

    def Save(self):
        command = {"CMD": "Save"}
        command = json.dumps(command)
        self._send(command)

    def Load(self, filename=None):
        command = {"CMD": "Load"}
        if filename != None:
            command.update({"filename": filename})
        command = json.dumps(command)
        self._send(command)

    def GetCurrentStatus(self):
        command = {"CMD": "GetCurrentStatus"}
        command = json.dumps(command)
        statusinfo = self._send(command)
        return statusinfo

    def GetWeaponInfo(self):
        command = {"CMD": "GetWeaponInfo"}
        command = json.dumps(command)
        weaponinfo = self._send(command)
        print("GetWeaponInfo OK")
        return weaponinfo

    def SetSimInterval(self, timestep):
        command = {"CMD": "SetSimInterval"}
        SetSimInterval = {"siminterval": timestep}
        command.update(SetSimInterval)
        command = json.dumps(command)
        self._send(command)
        # print("SetSimInterval OK")

    def SetRender(self, render=True):
        command = {"CMD": "SetRender"}
        command.update({"render": render})
        command = json.dumps(command)
        self._send(command)

    def GetCurrentResult(self):
        command = {"CMD": "GetCurrentResult"}
        command = json.dumps(command)
        result = self._send(command)
        # print("GetCurrentResult OK")
        return result

    def GetPisResult(self):
        command = {"CMD": "GetPisResult"}
        command = json.dumps(command)
        result = self._send(command)
        # print("GetPisResult OK")
        return result

    def statusparser(self, result):
        if "status" not in json.loads(result).keys():
            return None
        if result.find('status') < 0:
            return None
        if json.loads(result)["status"] == "":
            return None
        status = json.loads(json.loads(result)["status"])
        redState = status["redState"]
        blueState = status["blueState"]
        # whiteState = status["whiteState"]
        # redScore = whiteState["redScore"]
        # blueScore = whiteState["blueScore"]
        return redState, blueState

    def GetLandForm(self,lon,lat):
        command = {"CMD": "GetCurrentPlatform"}
        command.update({"lon": lon,"lat":lat})
        command = json.dumps(command)
        result = self._send(command)
        # print("GetLandForm OK")
        return result

    def resultparser(self, result):
        if "status" not in json.loads(result).keys():
            return None
        if result.find('status') < 0:
            return None
        if json.loads(result)["status"] == "":
            return None
        status = json.loads(json.loads(result)["status"])
        redState = status["redState"]
        blueState = status["blueState"]
        # whiteState = status["whiteState"]
        # redScore = whiteState["redScore"]
        # blueScore = whiteState["blueScore"]
        return redState, blueState

    def reward(self):
        result = self.GetCurrentStatus()
        if json.loads(result)["status"] == "":
            return None
        status = json.loads(json.loads(result)["status"])
        return status

    def Terminal(self):
        command = {"CMD": "Terminal"}
        command = json.dumps(command)
        result = self._send(command)
        if json.loads(result) == "":
            return None
        result = json.loads(result)
        return result