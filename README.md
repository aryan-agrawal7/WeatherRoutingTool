# Weather Routing Tool  

## Task: Create a New Ship Class  

The task was to create a new ship class in the `ship.py` file with the following specific requirements:  

1. **Inherit from the existing `Boat` base class**  
2. **Implement the `get_ship_parameters` method**  
3. **Create a function that calculates a "synthetic" fuel rate**  
    - The fuel rate should depend on at least one environmental parameter (e.g., wave height).  
    - Ensure fuel rates are within a reasonable range.  
4. **Consider how ship characteristics (size, type, speed) affect fuel consumption**  

## Implementation Details  

Currently, the relationship between environmental parameters and fuel consumption is not clearly defined. Since there are multiple ways to approach this, I have implemented the simplest solution: a mathematical relation between fuel consumption and environmental factors.  

I asked ChatGPT for an approximate mathematical formula that relates wind speed and wave height to fuel consumption. It suggested the following formula:  
\[ \Delta F = k_1 \cdot w^3 + k_2 \cdot H^2 \]  
Here, \( k_1 \) and \( k_2 \) are constants that depend on the ship type. The formula indicates that fuel consumption is influenced by wind speed (\( w \)) cubically and wave height (\( H \)) quadratically.  

Using this formula, I created random values for \( k_1 \) and \( k_2 \) for each ship type and implemented a basic function. This function takes wave height and wind speed as arguments and returns the calculated fuel consumption.  

### Code Location  

The implementation of the new ship class can be found in the file:  
`WeatherRoutingTool/ship/customship_task.py`

### Future Improvements  

This approach can be significantly improved with the availability of data. Using a predictive model based on historical data would be more accurate, as nature is highly variable. A mathematical formula alone cannot capture this variability effectively. Transitioning to a data-driven model would allow for better predictions and adaptability.  