import random

# Inventory setup for each player
# Hotbar: 		0-9
# Inventory:	9-38
# Armor:		36-39
# Offhand:		???
INVENTORY = '''
    <Inventory>
        <InventoryItem slot="0" type="stone_sword" />
        <InventoryItem slot="1" type="stone_axe" />
        <InventoryItem slot="2" type="bow" />
        <InventoryItem slot="9" type="arrow" quantity="64" />

        <InventoryItem slot="36" type="iron_boots" />
        <InventoryItem slot="37" type="iron_leggings" />
        <InventoryItem slot="38" type="iron_chestplate" />
        <InventoryItem slot="39" type="iron_helmet" />
    </Inventory>
'''

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
                   	''' + INVENTORY + '''
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

def getWorldXML(reset, num_agents):
	xml = '''
    	<?xml version="1.0" encoding="UTF-8" standalone="no" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com">
            <About>
                <Summary>Fight to the death!</Summary>
            </About>
            <ModSettings>
                <MsPerTick>50</MsPerTick>
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
                        <DrawCuboid x1="-5" y1="198" z1="-5" x2="5" y2="227" z2="5" type="bedrock"/>
                        <DrawCuboid x1="-4" y1="199" z1="-4" x2="4" y2="227" z2="4" type="sandstone"/>
                        <DrawCuboid x1="-3" y1="200" z1="-3" x2="3" y2="200" z2="3" type="grass"/>
                        <DrawCuboid x1="-3" y1="201" z1="-3" x2="3" y2="247" z2="3" type="air"/>
                        <DrawBlock x="0" y="226" z="0" type="fence"/>
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
        <AgentSection mode="Creative">
            <Name>Observer</Name>
            <AgentStart>
              	<Placement x="0.5" y="228" z="0.5" pitch="90"/>
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
