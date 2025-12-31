#!/usr/bin/env python3
"""
Hybrid Energy Balancing System
Bakhmach Business Hub - Advanced Energy Management

Strategies:
1. GRID_PRIORITY: Use mains power (cheapest), battery as buffer
2. RENEWABLE_FIRST: Solar/wind first, fallback to mains, battery peak leveling
3. OFF_GRID: Battery primary, renewable secondary, mains emergency only
"""

import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('HybridBalancer')


@dataclass
class EnergySource:
    """Energy source with availability & cost metrics"""
    name: str
    power_available_w: float  # Current available power (W)
    power_capacity_w: float   # Max output (W)
    cost_per_kwh: float       # Price UAH/kWh
    response_time_ms: int     # How fast it can react (ms)
    is_available: bool = True
    uptime_percent: float = 99.5


@dataclass
class EnergyDemand:
    """Current load configuration"""
    monitoring_system_w: float = 150   # Prometheus, logger, dashboards
    connectivity_w: float = 80         # Router, modem, WiFi
    iot_devices_w: float = 200         # Sensors, ESP32, controllers
    safety_margin_w: float = 50        # Reserve for spikes
    total_w: float = 480               # Sum of above


class HybridBalancer:
    """Intelligent multi-source energy balancing engine"""

    STRATEGIES = ['GRID_PRIORITY', 'RENEWABLE_FIRST', 'OFF_GRID']

    def __init__(self, strategy='RENEWABLE_FIRST', log_interval=60):
        self.strategy = strategy
        self.log_interval = log_interval
        self.last_log = time.time()
        self.energy_log = []  # Time-series data for analytics
        
        # Energy sources (example values)
        self.sources = {
            'grid': EnergySource(
                name='Main Grid (Kyivstar)',
                power_available_w=2500,
                power_capacity_w=3000,
                cost_per_kwh=3.5,  # ~3.5 UAH/kWh (2025)
                response_time_ms=0,
                uptime_percent=95.2
            ),
            'solar': EnergySource(
                name='Solar Panels (30W est.)',
                power_available_w=0,  # Varies by time
                power_capacity_w=600,
                cost_per_kwh=0,
                response_time_ms=100,
                is_available=False
            ),
            'wind': EnergySource(
                name='Wind Turbine (5W est.)',
                power_available_w=0,
                power_capacity_w=100,
                cost_per_kwh=0,
                response_time_ms=200,
                is_available=False
            ),
            'battery': EnergySource(
                name='LiFePO4 Battery (50Wh)',
                power_available_w=150,  # Can discharge at max
                power_capacity_w=200,
                cost_per_kwh=0.05,  # Cycling cost estimate
                response_time_ms=50,
                uptime_percent=99.9
            )
        }

    def estimate_solar_power(self, hour: int = None) -> float:
        """Estimate solar generation based on time of day"""
        if hour is None:
            hour = datetime.now().hour
        
        # Simple cosine model: peak at 12:00 (noon)
        if hour < 6 or hour > 18:
            return 0
        
        # Power peaks at 12:00, is 0 at sunrise (6) and sunset (18)
        import math
        normalized_hour = (hour - 6) / 12  # 0 to 1 over 6-18
        solar_power = 600 * math.cos((normalized_hour - 0.5) * math.pi)**2
        return max(0, solar_power)

    def estimate_wind_power(self) -> float:
        """Estimate wind generation (simplified)"""
        # Assume wind is relatively constant in Ukraine (avg 4-5 m/s)
        # Can add time-series real data from NOAA/IMERG later
        import random
        return random.gauss(50, 15)  # 50W avg, 15W std dev

    def allocate_grid_priority(self, demand: EnergyDemand) -> Dict:
        """Strategy 1: Maximize mains usage (cheapest, most reliable)"""
        sources_used = {}
        remaining_demand = demand.total_w + demand.safety_margin_w

        # Step 1: Use mains first (cheapest)
        grid = self.sources['grid']
        if grid.is_available and remaining_demand > 0:
            grid_usage = min(remaining_demand, grid.power_available_w)
            sources_used['grid'] = grid_usage
            remaining_demand -= grid_usage

        # Step 2: Use battery if grid insufficient
        if remaining_demand > 0:
            battery = self.sources['battery']
            battery_usage = min(remaining_demand, battery.power_available_w)
            sources_used['battery'] = battery_usage
            remaining_demand -= battery_usage

        # Step 3: Emergency renewable if still short
        if remaining_demand > 0:
            solar_power = self.estimate_solar_power()
            wind_power = self.estimate_wind_power()
            sources_used['solar'] = min(remaining_demand * 0.7, solar_power)
            sources_used['wind'] = min(remaining_demand * 0.3, wind_power)

        return {
            'strategy': 'GRID_PRIORITY',
            'sources': sources_used,
            'deficit_w': max(0, remaining_demand),
            'cost_estimate_uah_per_hour': sources_used.get('grid', 0) / 1000 * 3.5
        }

    def allocate_renewable_first(self, demand: EnergyDemand) -> Dict:
        """Strategy 2: Prefer renewable, use grid as backup"""
        sources_used = {}
        remaining_demand = demand.total_w + demand.safety_margin_w

        solar_power = self.estimate_solar_power()
        wind_power = self.estimate_wind_power()

        # Step 1: Use renewable sources
        sources_used['solar'] = min(remaining_demand * 0.8, solar_power)
        remaining_demand -= sources_used['solar']

        sources_used['wind'] = min(remaining_demand * 0.8, wind_power)
        remaining_demand -= sources_used['wind']

        # Step 2: Use battery to level peaks
        battery = self.sources['battery']
        battery_usage = min(remaining_demand, battery.power_available_w)
        sources_used['battery'] = battery_usage
        remaining_demand -= battery_usage

        # Step 3: Fall back to grid
        grid = self.sources['grid']
        grid_usage = min(remaining_demand, grid.power_available_w)
        sources_used['grid'] = grid_usage
        remaining_demand -= grid_usage

        return {
            'strategy': 'RENEWABLE_FIRST',
            'sources': sources_used,
            'deficit_w': max(0, remaining_demand),
            'renewable_percent': ((sources_used.get('solar', 0) + sources_used.get('wind', 0)) / 
                                (demand.total_w + demand.safety_margin_w) * 100) if demand.total_w > 0 else 0
        }

    def allocate_off_grid(self, demand: EnergyDemand) -> Dict:
        """Strategy 3: Battery primary, mains emergency only"""
        sources_used = {}
        remaining_demand = demand.total_w + demand.safety_margin_w

        # Step 1: Prefer battery (no grid cost)
        battery = self.sources['battery']
        battery_usage = min(remaining_demand, battery.power_available_w)
        sources_used['battery'] = battery_usage
        remaining_demand -= battery_usage

        # Step 2: Use renewable to recharge
        solar_power = self.estimate_solar_power()
        wind_power = self.estimate_wind_power()
        sources_used['solar'] = min(remaining_demand * 0.7, solar_power)
        remaining_demand -= sources_used['solar']

        sources_used['wind'] = min(remaining_demand * 0.3, wind_power)
        remaining_demand -= sources_used['wind']

        # Step 3: Only use grid if emergency
        if remaining_demand > 0:
            grid = self.sources['grid']
            grid_usage = min(remaining_demand, grid.power_available_w)
            sources_used['grid'] = grid_usage
            sources_used['_emergency'] = True

        return {
            'strategy': 'OFF_GRID',
            'sources': sources_used,
            'battery_remaining_wh': 45,  # Estimate (50Wh * 90% SoC)
            'emergency_grid_used': sources_used.get('_emergency', False)
        }

    def balance(self, demand: Optional[EnergyDemand] = None) -> Dict:
        """Execute balancing based on selected strategy"""
        if demand is None:
            demand = EnergyDemand()

        if self.strategy == 'GRID_PRIORITY':
            result = self.allocate_grid_priority(demand)
        elif self.strategy == 'RENEWABLE_FIRST':
            result = self.allocate_renewable_first(demand)
        elif self.strategy == 'OFF_GRID':
            result = self.allocate_off_grid(demand)
        else:
            raise ValueError(f'Unknown strategy: {self.strategy}')

        result['timestamp'] = datetime.now().isoformat()
        result['demand_w'] = demand.total_w + demand.safety_margin_w
        
        # Log and return
        self._log_result(result)
        return result

    def _log_result(self, result: Dict):
        """Log energy allocation for analytics"""
        self.energy_log.append(result)
        
        if time.time() - self.last_log >= self.log_interval:
            total_from_grid = sum(r['sources'].get('grid', 0) for r in self.energy_log[-self.log_interval:])
            total_from_renewable = sum(
                r['sources'].get('solar', 0) + r['sources'].get('wind', 0) 
                for r in self.energy_log[-self.log_interval:]
            )
            total_from_battery = sum(r['sources'].get('battery', 0) for r in self.energy_log[-self.log_interval:])
            
            logger.info(f"Strategy: {self.strategy} | Grid: {total_from_grid:.0f}W | "
                       f"Renewable: {total_from_renewable:.0f}W | Battery: {total_from_battery:.0f}W")
            self.last_log = time.time()


if __name__ == '__main__':
    # Demo: Test all 3 strategies
    demand = EnergyDemand()
    
    for strategy in HybridBalancer.STRATEGIES:
        balancer = HybridBalancer(strategy=strategy)
        result = balancer.balance(demand)
        
        print(f"\n=== Strategy: {strategy} ===")
        print(json.dumps(result, indent=2, default=str))
        print(f"Deficit: {result.get('deficit_w', 0):.1f}W | "
              f"Cost estimate: {result.get('cost_estimate_uah_per_hour', 0):.2f} UAH/h | "
              f"Renewable: {result.get('renewable_percent', 0):.1f}%")
