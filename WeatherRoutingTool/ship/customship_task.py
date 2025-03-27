import numpy as np
import math
from astropy import units as u
import WeatherRoutingTool.utils.formatting as form
import logging
from WeatherRoutingTool.ship.shipparams import ShipParams

logger = logging.getLogger('WRT.ship')

class Boat:
    speed: float  # boat speed in m/s

    def __init__(self, config):
        self.speed = config.BOAT_SPEED * u.meter/u.second
        pass

    def get_ship_parameters(self, courses, lats, lons, time, speed=None, unique_coords=False):
        pass

    def get_boat_speed(self):
        return self.speed

    def print_init(self):
        pass

class SyntheticFuelBoat(Boat):
    """
    A boat class that calculates fuel rate based on environmental conditions.
    The fuel rate is modeled as a function of:
    1. Base fuel rate (depends on ship type and speed)
    2. Wave height (increased waves lead to higher fuel consumption)
    3. Wind speed (headwinds increase fuel consumption)
    """
    
    def __init__(self, config):
        """
        Args:
            config: Configuration object containing boat parameters
        """
        super().__init__(config)
        # Base parameters
        self.base_fuel_rate = config.CONSTANT_FUEL_RATE * u.kg/u.second  # kg/s baseline
        self.ship_type = getattr(config, 'SHIP_TYPE', 'generic_cargo')
        
        # Fuel rate multipliers based on ship type
        self.type_multipliers = {
            'container_ship': 1.2,
            'tanker': 1.0,
            'bulk_carrier': 1.1,
            'fishing_vessel': 0.8,
            'generic_cargo': 1.0
        }

    def print_init(self):
        logger.info(form.get_log_step(f'Boat speed: {self.speed}', 1))
        logger.info(form.get_log_step(f'Base fuel rate: {self.base_fuel_rate}', 1))
        logger.info(form.get_log_step(f'Ship type: {self.ship_type}', 1))

    def calculate_fuel_rate(self, wave_height, wind_speed):
        """
        Args:
            wave_height (float): Significant wave height in meters
            wind_speed (float): Wind speed in m/s
        
        Returns:
            float: Estimated fuel rate in kg/s
        """
        # Base type multiplier
        type_multiplier = self.type_multipliers.get(self.ship_type, 1.0)
        
        # Wave height impact: square increase in fuel consumption
        wave_factor = 1 + 0.5 * (wave_height / 1.0) ** 2
        
        # Wind speed impact: The excess fuel consumption can be approximated as a cubic function of wind speed,
        wind_factor = 1 + 0.2 * (wind_speed / 10.0)**3
        
        # Calculate total fuel rate
        total_fuel_rate = (
            self.base_fuel_rate * 
            type_multiplier * 
            wave_factor * 
            wind_factor
        )
        
        # Ensure fuel rate stays within a reasonable range (0.5 to 5 kg/s)
        return np.clip(total_fuel_rate, 0.5 * u.kg/u.second, 5.0 * u.kg/u.second)

    def get_ship_parameters(self, courses, lats, lons, time, speed=None, unique_coords=False):
        """
        Generate ship parameters with synthetic fuel rate calculation.
        
        Args:
            courses (array): Array of ship courses
            lats (array): Latitudes
            lons (array): Longitudes
            time (array): Timestamps
            speed (array, optional): Ship speeds
            unique_coords (bool, optional): Whether to use unique coordinates
        
        Returns:
            ShipParams: Synthetic ship parameters
        """
        debug = False
        n_requests = len(courses)

        # For this example, we'll use dummy environmental data
        # In a real scenario, these would come from environmental datasets
        wave_heights = np.random.uniform(0.5, 3.0, n_requests) * u.meter
        wind_speeds = np.random.uniform(0, 15, n_requests) * u.meter/u.second
        
        # Calculate fuel rates
        fuel_rates = np.array([
            self.calculate_fuel_rate(wave_heights[i], wind_speeds[i]) 
            for i in range(n_requests)
        ])
        
        # Create dummy arrays for other parameters
        dummy_array = np.full(n_requests, -99)
        speed_array = np.full(n_requests, self.speed) if speed is None else speed

        # Construct ShipParams object
        ship_params = ShipParams(
            fuel_rate=fuel_rates,
            power=dummy_array * u.Watt,
            rpm=dummy_array * u.Hz,
            speed=speed_array * u.meter/u.second,
            r_wind=dummy_array * u.N,
            r_calm=dummy_array * u.N,
            r_waves=dummy_array * u.N,
            r_shallow=dummy_array * u.N,
            r_roughness=dummy_array * u.N,
            wave_height=wave_heights,
            wave_direction=dummy_array * u.radian,
            wave_period=dummy_array * u.second,
            u_currents=dummy_array * u.meter/u.second,
            v_currents=dummy_array * u.meter/u.second,
            u_wind_speed=wind_speeds,
            v_wind_speed=dummy_array * u.meter/u.second,
            pressure=dummy_array * u.kg/u.meter/u.second**2,
            air_temperature=dummy_array * u.deg_C,
            salinity=dummy_array * u.dimensionless_unscaled,
            water_temperature=dummy_array * u.deg_C,
            status=dummy_array,
            message=np.full(n_requests, "")
        )

        if debug:
            logger.info("Fuel rates: " + str(fuel_rates))
        
        return ship_params