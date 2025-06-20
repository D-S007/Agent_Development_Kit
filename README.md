# Agent_Development_Kit
adk run multi_tool_agent (inside parent_folder)

# Response
![alt text](image.png)

# Open-Meteo API
- The get_weather function in agent.py is now updated to retrieve weather data for any location using the Open-Meteo API. 
- It performs geocoding to get latitude and longitude for the city, then fetches the current weather.
- We can now use the agent to get weather information for any city, not just New York.