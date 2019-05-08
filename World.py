SUMMARY = "Combat AI"

def getMissionXML(agent_id):
    ''' Build an XML mission string '''

    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>''' + SUMMARY + '''</Summary>
            <Description>Test01</Description>
        </About>

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
                <FlatWorldGenerator generatorString="3;5*minecraft:air;2;" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="100" z1="-50" x2="50" y2="100" z2="50" type="grass" />
                    <DrawCuboid x1="-51" y1="102" z1="-51" x2="50" y2="102" z2="-51" type="wooden_slab" />
                    <DrawCuboid x1="51" y1="102" z1="-51" x2="51" y2="102" z2="50" type="wooden_slab" />
                    <DrawCuboid x1="51" y1="102" z1="51" x2="-50" y2="102" z2="51" type="wooden_slab" />
                    <DrawCuboid x1="-51" y1="102" z1="51" x2="-51" y2="102" z2="-50" type="wooden_slab" />
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Player''' + str(agent_id) + '''</Name>
            <AgentStart>
                <Placement x="-25.5" y="101.0" z="0.5"/>
                <Inventory>
                    <InventoryItem slot="0" type="stone_sword" />
                    <InventoryItem slot="1" type="stone_axe" />
                    <InventoryItem slot="2" type="bow" />
                    <InventoryItem slot="9" type="arrow" quantity="64" />
                    <InventoryItem slot="3" type="shield" />
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromHotBar/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''
