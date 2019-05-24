import random

# Inventory slots
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
    <InventoryItem slot="8" type="shield" />

    <InventoryItem slot="36" type="iron_boots" />
    <InventoryItem slot="37" type="iron_leggings" />
    <InventoryItem slot="38" type="iron_chestplate" />
    <InventoryItem slot="39" type="iron_helmet" />
</Inventory>
'''

def agentName(i):
    return "Player_" + str(i + 1)

def agentXML(num_agents):
	if num_agents == 2:
		return '''
        <AgentSection mode="Survival">
            <Name>Player_1</Name>
            <AgentStart>
                <Placement x="-15.5" y="204.0" z="0.5"/>
				''' + INVENTORY + '''
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <ChatCommands/>
                <MissionQuitCommands quitDescription="Player_1 has won"/>
                <InventoryCommands/>
                <ObservationFromHotBar/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>
            </AgentHandlers>
        </AgentSection>

        <AgentSection mode="Survival">
            <Name>Player_2</Name>
            <AgentStart>
                <Placement x="15.5" y="204.0" z="0.5"/>
                ''' + INVENTORY + '''
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <ChatCommands/>
                <MissionQuitCommands quitDescription="Player_2 has won"/>
                <InventoryCommands/>
                <ObservationFromHotBar/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullStats/>
            </AgentHandlers>
        </AgentSection>
		'''
	else:
		agXML = ""
		for i in range(num_agents):
			agXML += '''
			<AgentSection mode="Survival">
	            <Name>Player_''' + agentName(i) + '''</Name>
	            <AgentStart>
	                <Placement x="''' + str(random.randint(-18,18)) + '''" y="204.0" z="''' + str(random.randint(-18,18)) + '''"/>
	               	''' + INVENTORY + '''
	            </AgentStart>
	            <AgentHandlers>
	                <ContinuousMovementCommands turnSpeedDegs="480"/>
                    <ChatCommands/>
	                <AbsoluteMovementCommands/>
	                <MissionQuitCommands quitDescription="Player_2 has won"/>
	                <InventoryCommands/>
	                <ObservationFromHotBar/>
	                <ObservationFromNearbyEntities>
	                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
	                </ObservationFromNearbyEntities>
	            </AgentHandlers>
        	</AgentSection>
			'''
		return agXML

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
                    <DrawCuboid x1="-20" y1="199" z1="-20" x2="20" y2="227" z2="20" type="sandstone"/>
                    <DrawCuboid x1="-19" y1="200" z1="-19" x2="19" y2="200" z2="19" type="grass"/>
                    <DrawCuboid x1="-19" y1="201" z1="-19" x2="18" y2="247" z2="18" type="air"/>
                    <DrawBlock x="0" y="226" z="0" type="fence"/>
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="1000000"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>
    '''

    # Add players
	xml += agentXML(num_agents)

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
          	<VideoProducer>
            	<Width>640</Width>
           	 <Height>640</Height>
          	</VideoProducer>
        </AgentHandlers>
    </AgentSection>
    '''

	xml += '</Mission>'
	print(xml)
	return xml
