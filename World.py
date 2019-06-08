import random

# Inventory setup for each player
# Hotbar: 		0-9
# Inventory:	9-38
# Armor:		36-39
# Offhand:		???

def inventory(playerNum):
    return '''
    <Inventory>
        <InventoryItem slot="0" type="stone_sword" />
        <InventoryItem slot="1" type="stone_axe" />
        <InventoryItem slot="2" type="bow" />
        <InventoryItem slot="9" type="arrow" quantity="64" />
        <InventoryItem slot="36" type="iron_boots" />
        <InventoryItem slot="37" type="iron_leggings" />
        <InventoryItem slot="38" type="iron_chestplate" />
        <InventoryItem slot="39" type="''' + ("golden_helmet" if playerNum == 0 else "iron_helmet")  + '''"/>
    </Inventory>'''

# Starting positions when # of players = 2
DUELPOSITIONS = [
'x="-2.5" y="204.0" z="0.5"',
'x="2.5" y="204.0" z="0.5"'
]


# Determines the name of a given player
def playerName(i):
    return "Player_" + str(i + 1)

# Determines the starting position of a given player
def playerPlacement(i, num_agents):
    if num_agents == 2:
        return DUELPOSITIONS[i]
    else:
        return 'x="' + str(random.randint(-18,18)) + '" y="204.0" z="' + str(random.randint(-18,18)) + '"'

# Creates and returns the xml for all players
def playerXML(num_agents):
	playersXML = ""

	for i in range(num_agents):
		playersXML += '''
    		<AgentSection mode="Survival">
                <Name>''' + playerName(i) + '''</Name>
                <AgentStart>
                    <Placement ''' + playerPlacement(i, num_agents) + '''/>
                   	''' + inventory(i) + '''
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands turnSpeedDegs="480"/>
                    <ChatCommands/>
                    <MissionQuitCommands quitDescription="''' + playerName(i) + ''' has won"/>
                    <InventoryCommands/>
                    <ObservationFromHotBar/>
                    <ObservationFromNearbyEntities>
                        <Range name="entities" xrange="40" yrange="5" zrange="40"/>
                    </ObservationFromNearbyEntities>
                    <ObservationFromFullStats/>
                </AgentHandlers>
        	</AgentSection>
		'''

	return playersXML

def getWorldXML(reset, num_agents, arenaSize, speedMul):
	xml = '''
    	<?xml version="1.0" encoding="UTF-8" standalone="no" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com">
            <About>
                <Summary>Fight to the death!</Summary>
            </About>
            <ModSettings>
                <MsPerTick>''' + str(50 // speedMul) + '''</MsPerTick>
            </ModSettings>
            <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>6000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                    <AllowSpawning>false</AllowSpawning>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator forceReset="'''+ reset +'''" generatorString="3;5*minecraft:air;2;" />
                    <DrawingDecorator>
                        <DrawCuboid x1="-''' + str(arenaSize+2) + '''" y1="198" z1="-''' + str(arenaSize+2) + '''" x2="''' + str(arenaSize+2) + '''" y2="227" z2="''' + str(arenaSize+2) + '''" type="bedrock"/>
                        <DrawCuboid x1="-''' + str(arenaSize+1) + '''" y1="199" z1="-''' + str(arenaSize+1) + '''" x2="''' + str(arenaSize+1) + '''" y2="227" z2="''' + str(arenaSize+1) + '''" type="sandstone"/>
                        <DrawCuboid x1="-''' + str(arenaSize) + '''" y1="200" z1="-''' + str(arenaSize) + '''" x2="''' + str(arenaSize) + '''" y2="200" z2="''' + str(arenaSize) + '''" type="grass"/>
                        <DrawCuboid x1="-''' + str(arenaSize) + '''" y1="201" z1="-''' + str(arenaSize) + '''" x2="''' + str(arenaSize) + '''" y2="247" z2="''' + str(arenaSize) + '''" type="air"/>
                    </DrawingDecorator>
                    <ServerQuitFromTimeUp timeLimitMs="60000"/>
                    <ServerQuitWhenAnyAgentFinishes />
                </ServerHandlers>
            </ServerSection>
    '''

    # Add players
	xml += playerXML(num_agents)

    # Add the camera (player)
	xml += '''
        <AgentSection mode="Spectator">
            <Name>Observer</Name>
            <AgentStart>
              	<Placement x="0.5" y="''' + str(201.0+arenaSize) + '''" z="0.5" pitch="90"/>
            </AgentStart>
            <AgentHandlers>
              	<ContinuousMovementCommands turnSpeedDegs="360"/>
              	<MissionQuitCommands/>
              	<ChatCommands/>
            </AgentHandlers>
        </AgentSection>
    '''

	xml += '</Mission>'

	return xml
