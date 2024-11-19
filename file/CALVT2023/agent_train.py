# coding=UTF-8
import sys, os
sys.path.append(os.getcwd())

import argparse
from Env import Env
import json
import time

from AI.red_agent import RedAgent
from AI.blue_agent import BlueAgent
import sys

def get_states(env):
    result = env.GetCurrentStatus()
    while (env.statusparser(result) == None):
        env.Step()
        result = env.GetCurrentStatus()
    redState, blueState = env.statusparser(result)
    return redState, blueState

def train(red_agent: RedAgent, blue_agent: BlueAgent, args, seed=1234):
    env = Env(args.ip, args.port)
    for epoch in range(args.epochs):
        print(f"================ {epoch + 1} th =============")
        ### Reset ###
        shipIDlist = env.Reset()
        shipIDlist = json.loads(shipIDlist)
        red_agent.reset()
        blue_agent.reset()

        ### Deploy ###
        act = (
            red_agent.deploy(shipIDlist['RedShipID'])
            + blue_agent.deploy(shipIDlist['BlueShipID'])
        )
        env.Step(Action={'Action': act})

        # print('landform:')
        # print(env.GetLandForm(2.59, 39.72))
        # print(env.GetLandForm(2.58875, 39.71979))
        for step in range(1, args.max_episode_len+1):
            print(f"================ {step} steps =============")
            env.SetRender(True)
            red_state, blue_state = get_states(env)
            # if 'DespoilControlPos0' in red_state.keys():
            #     print("Red Controling!!!")
            #     print(red_state['DespoilControlPos0'])
            # if 'DespoilControlPos0' in blue_state.keys():
            #     print("Blue Controling!!!")
            #     print(blue_state.keys())
            #     print(blue_state['DespoilControlPos0'])
            act = red_agent.step(red_state) + blue_agent.step(blue_state)
            env.Step(Action={'Action': act})
            # print(act)

            cur_result = json.loads(env.GetCurrentResult())
            print(cur_result)
            # print("blueScore: ", cur_result["blueScore"])
            # print("redScore: ", cur_result["redScore"])
            # time.sleep(0.05)
            # if step == 20: break
            # if step == 3000: break
            # if step == 500: break
            # if step == 3000: break

        # cur_result = json.loads(env.GetCurrentResult())
        # print("blueScore: ", cur_result["blueScore"])
        # print("redScore: ", cur_result["redScore"])
        result = env.Terminal()
        print(result)
        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Provide arguments for agent.')
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Ip to connect")
    parser.add_argument("--port", type=str, default=20001, help="port to connect")
    parser.add_argument("--epochs", type=int, default=200, help="Number of training epochs to run")  # 设置训练轮次数
    parser.add_argument("--max-episode-len", type=int, default=3000, help="maximum episode length")
    args = parser.parse_args()

    ### Build red/blue Agent ###
    redAgent = RedAgent()
    blueAgent = BlueAgent()

    ### Train ###
    train(redAgent, blueAgent, args, seed=1234)
