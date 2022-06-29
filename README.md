# **Capstone I Camelot**

# Project Overview:
 
Create a fully automated ecosystem of NPCs using Reinforcement Learning. With the aid of reinforcement learning, create multiple agents or models for each NPCs to automatically conduct various tasks and create settings similar to human behaviors like satisfying basic needs like hunger, thirst, and energy. These agents will be trained on simulations of states and actions which will allow the NPCs to act on their own will. The goal is to create agents or models that allow the NPCs to act on their own without any written instructions and ultimately creating an ecosystem with no outside guides. 

Once an ecosystem is established with fully automated NPCs, multiple layers can be introduced such as a trading system, distribution of wealth, each of the NPCs happiness, establishing supply and demand, different skills and traits for the NPCs, and etc. When different layers are introduced, a study can be done to see the effects of each event to the ecosystem. 

**Sample events can and may include the following:**


-	Introducing special skills or traits that will allow the NPCs to better collect more resources than what they need while spending less energy. Ultimately, having the AI decide the occupation of the NPCs.
-	A trading system can then be introduced so that the NPCs can trade or sell extra resources which in the end increases wealth and happiness.
-	A market can be created so that the NPCs can buy and trade to satisfy basic needs. 
-	Trader NPCs will be able to simulate supply and demand like the real world. If the traders are not able to sell particular items, they must lower the price to be able to sell the items. If the supply is low and demand high, these NPC will increase the prices. At the end having the AI decide the price of resources based on the supply and demand.

**Sample studies can and may include the following:**

-	Study the distribution of wealth, equality, productivity, and happiness on a step basis.
-	Introduce environmental variability such as a tax system, drought, or any hardships to see its effects on the economy.
-   Create societal conflict like struggle for power or crime.
 
 
 

# Agile Development Deliverables                                                                                                                                 

<details><summary>Goals for Deliverable #1 (Due March 4th): Developing the Ecosystem</summary>
<br/>
<details><summary>Sprint 1 - Creating the World & NPCs (Feb 4th - Feb 18th)</summary>

1.	Creating a place or environment
-   Create an array (2D or 3D) where events will take place
-	Randomize resource and NPC placements
-	Replicate Camelot coordinates

2.	Class for generating NPCs
-   Class __init__ should include NPC’s name, body type, hair style, outfit info
-   Class should include state info (hunger info, thirst info and energy info).
-   Class should include skills:
--       Neutral: collecting, trading, fishing, farming
--        Positive: give, receive
--        Negative: stealing, fighting

3.	Class for generating items
-	Class __init__ should include item name, item type, effect info
-	Class should set item placement
</details>

<details><summary>Sprint 2 - Create reinforcement learning models to automate NPCs (Feb 18th - Mar 4th)</summary>

1.	Create a measurement or value for the RL model to improve on.
-	Ex. Happiness which is a measure of hunger, thirst, and energy
-	Expandable to future layers such as addition of wealth, free time, etc

2.	Automate NPC movements
-	Create initial state, idle state, and action states for the NPCs

3.	Create NPC actions and states
-	Collecting, moving towards objects, eating, drinking, sleeping.
-	Future layers can include selling, buying, trading.

4.	Introduce rules and measures for actions and states
-	Cost for movements, actions, and events
-	Create limits per step/day

5.	Deliverable 1 Presentation
-	Create presentation
-	Create demo  
</details>    
</details>	
<br/>
<details><summary>Goals for Deliverable #2 (Due April 1st): Application of Reinforcement Learning</summary>
<br/>
<details><summary>Sprint 3 - Adding layers to the agents (Mar 4th - Mar 18th)</summary>
                                                                                                                                      
1.	Introduce skills or traits that affects actions and states for the NPCs
-	Skills or traits would allow NPCs to complete certain tasks much effectively
-	Forces the AI to make NPCs to do a certain task (introduction of occupations)
-	Allows opportunity to add additional layers and complexity

2.	Add more complex layers
-	Ex. Trading system, supply and demand, taxes
</details> 

<details><summary>Sprint 4 - Improving layers and adding events (Mar 18th - Apr 1st)</summary>

1.	Create layers that encourages changes in the ecosystem
-	Environmental variability such as a tax system, drought, or any hardships
2.	Study changes in the ecosystem
-	Make visual representations such as graphs
3.	Deliverable 2 Presentation
-	Create presentation
-	Create demo 
</details>
</details> 
 
<br/>                                                                                                                                        
<details><summary>Goals for Deliverable #3 (Due April 29th): Introduction and Study of  Events to the Ecosystem</summary>
<br/>
<details><summary>Sprint 5 - Visualization in Camelot and paying technical debt (Apr 1st - Apr 15th)</summary>
1.	Integrate python to camelot and create visualizations
2.	Catch up on technical debt
3.	Try more scenarios if possible
</details>

<details><summary>Sprint 6 - Project finalization (Apr 15th - Apr 29th)</summary>
1.	Generate visualizations and graphical plots to show studies
2.	Create HTML page for visualization
3.	Host visualization to use for HTML
4.	Deliverable 3 Presentation
-	Create final presentation
-	Show demos
</details>
</details>
