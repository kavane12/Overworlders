# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

import MalmoPython
import os
import random
import sys
import time
import json
import math
import uuid

from World import getWorldXML, agentName
from CombatAI import AI

# Create one agent host for parsing:
agent_hosts = [MalmoPython.AgentHost()]

# Parse the command-line options:
agent_hosts[0].addOptionalFlag( "debug,d", "Display debug information.")
agent_hosts[0].addOptionalIntArgument("agents,n", "Number of agents to use, including observer.", 3)

try:
    agent_hosts[0].parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_hosts[0].getUsage())
    exit(1)
if agent_hosts[0].receivedArgument("help"):
    print(agent_hosts[0].getUsage())
    exit(0)

DEBUG = agent_hosts[0].receivedArgument("debug")
INTEGRATION_TEST_MODE = agent_hosts[0].receivedArgument("test")
agents_requested = agent_hosts[0].getIntArgument("agents")
NUM_AGENTS = max(2, agents_requested - 1) # Will be NUM_AGENTS robots running around, plus one static observer.

# Create the rest of the agent hosts - one for each robot, plus one to give a bird's-eye view:
agent_hosts += [MalmoPython.AgentHost() for x in range(1, NUM_AGENTS + 1) ]

# Create AI objects:
ais = [AI(agentName(i), 'basic' if i == 0 else 'passive') for i in range(NUM_AGENTS)]

# Set up debug output:
for ah in agent_hosts:
    ah.setDebugOutput(DEBUG)    # Turn client-pool connection messages on/off.

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)



def safeStartMission(agent_host, my_mission, my_client_pool, my_mission_record, role, expId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            # Attempt start:
            agent_host.startMission(my_mission, my_client_pool, my_mission_record, role, expId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow a two minute timeout.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    if time.time() - start_time >= time_out:
        print("Timed out while waiting for mission to start - bailing.")
        exit(1)
    print()
    print("Mission has started.")


# Set up a client pool.
# IMPORTANT: If ANY of the clients will be on a different machine, then you MUST
# make sure that any client which can be the server has an IP address that is
# reachable from other machines - ie DO NOT SIMPLY USE 127.0.0.1!!!!
# The IP address used in the client pool will be broadcast to other agents who
# are attempting to find the server - so this will fail for any agents on a
# different machine.
client_pool = MalmoPython.ClientPool()
for x in range(10000, 10000 + NUM_AGENTS + 1):
    client_pool.add( MalmoPython.ClientInfo('127.0.0.1', x) )


num_missions = 1
for mission_no in range(1, num_missions+1):
    print("Running mission #" + str(mission_no))

    # Create mission xml - use forcereset if this is the first mission.
    my_mission = MalmoPython.MissionSpec(getWorldXML("true" if mission_no == 1 else "false", NUM_AGENTS), True)
    # Generate an experiment ID for this mission.
    # This is used to make sure the right clients join the right servers -
    # if the experiment IDs don't match, the startMission request will be rejected.
    # In practice, if the client pool is only being used by one researcher, there
    # should be little danger of clients joining the wrong experiments, so a static
    # ID would probably suffice, though changing the ID on each mission also catches
    # potential problems with clients and servers getting out of step.

    # Note that, in this sample, the same process is responsible for all calls to startMission,
    # so passing the experiment ID like this is a simple matter. If the agentHosts are distributed
    # across different threads, processes, or machines, a different approach will be required.
    # (Eg generate the IDs procedurally, in a way that is guaranteed to produce the same results
    # for each agentHost independently.)
    experimentID = str(uuid.uuid4())
    for i in range(len(agent_hosts)):
        safeStartMission(agent_hosts[i], my_mission, client_pool, MalmoPython.MissionRecordSpec(), i, experimentID)

    safeWaitForStart(agent_hosts)

    time.sleep(1)




    print("MISSION START")

    # AIs will make actions, return false if dead 
    q = False
    while not q:
        for i in range(NUM_AGENTS):
            if not ais[i].act(agent_hosts[i]):
                q = True


    print("MISSION END")




    print("Waiting for mission to end ", end=' ')
    # Mission should have ended already, but we want to wait until all the various agent hosts
    # have had a chance to respond to their mission ended message.
    hasEnded = False
    while not hasEnded:
        hasEnded = True # assume all good
        print(".", end=' ')
        time.sleep(0.1)
        for ah in agent_hosts:
            world_state = ah.getWorldState()
            if world_state.is_mission_running:
                hasEnded = False # all not good
