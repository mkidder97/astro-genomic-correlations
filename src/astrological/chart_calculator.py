"""Core astrological chart calculation using Swiss Ephemeris"""

import swisseph as swe
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class PlanetPosition:
    """Represents a planet's position and metadata"""
    longitude: float
    latitude: float
    distance: float
    speed: float
    house: Optional[int] = None
    sign: Optional[str] = None
    degree_in_sign: Optional[float] = None

@dataclass
class BirthChart:
    """Complete birth chart data structure"""
    datetime: datetime
    latitude: float
    longitude: float
    planets: Dict[str, PlanetPosition]
    houses: List[float]
    ascendant: float
    midheaven: float

class ChartCalculator:
    """Advanced astrological chart calculator with Swiss Ephemeris precision"""
    
    PLANETS = {
        'sun': swe.SUN,
        'moon': swe.MOON,
        'mercury': swe.MERCURY,
        'venus': swe.VENUS,
        'mars': swe.MARS,
        'jupiter': swe.JUPITER,
        'saturn': swe.SATURN,
        'uranus': swe.URANUS,
        'neptune': swe.NEPTUNE,
        'pluto': swe.PLUTO
    }
    
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self):
        """Initialize calculator with Swiss Ephemeris"""
        # Set ephemeris path if needed
        swe.set_ephe_path('/usr/share/swisseph')  # Adjust path as needed
    
    def calculate_chart(self, birth_datetime: datetime, latitude: float, longitude: float) -> BirthChart:
        """Calculate complete birth chart with high precision
        
        Args:
            birth_datetime: Birth date and time (UTC)
            latitude: Geographic latitude
            longitude: Geographic longitude
            
        Returns:
            BirthChart object with all planetary positions and houses
        """
        # Convert datetime to Julian day
        jd = swe.julday(birth_datetime.year, birth_datetime.month, birth_datetime.day,
                       birth_datetime.hour + birth_datetime.minute/60.0)
        
        # Calculate planetary positions
        planets = {}
        for planet_name, planet_id in self.PLANETS.items():
            position = self._calculate_planet_position(jd, planet_id)
            planets[planet_name] = position
        
        # Calculate houses using Placidus system
        houses, ascmc = swe.houses(jd, latitude, longitude, b'P')
        
        # Assign houses to planets
        for planet_name, planet_pos in planets.items():
            planet_pos.house = self._find_house(planet_pos.longitude, houses)
            planet_pos.sign = self._find_sign(planet_pos.longitude)
            planet_pos.degree_in_sign = planet_pos.longitude % 30
        
        return BirthChart(
            datetime=birth_datetime,
            latitude=latitude,
            longitude=longitude,
            planets=planets,
            houses=list(houses),
            ascendant=ascmc[0],
            midheaven=ascmc[1]
        )
    
    def _calculate_planet_position(self, jd: float, planet_id: int) -> PlanetPosition:
        """Calculate precise position for single planet"""
        result, flag = swe.calc_ut(jd, planet_id)
        
        return PlanetPosition(
            longitude=result[0],
            latitude=result[1],
            distance=result[2],
            speed=result[3]
        )
    
    def _find_house(self, longitude: float, houses: List[float]) -> int:
        """Determine which house a longitude falls into"""
        for i in range(12):
            house_start = houses[i]
            house_end = houses[(i + 1) % 12]
            
            # Handle crossing 0° Aries
            if house_start > house_end:
                if longitude >= house_start or longitude < house_end:
                    return i + 1
            else:
                if house_start <= longitude < house_end:
                    return i + 1
        
        return 1  # Default to first house
    
    def _find_sign(self, longitude: float) -> str:
        """Determine zodiac sign from longitude"""
        sign_index = int(longitude // 30)
        return self.SIGNS[sign_index]
    
    def get_planetary_aspects(self, chart: BirthChart, orb: float = 8.0) -> List[Dict]:
        """Calculate aspects between planets
        
        Args:
            chart: Birth chart to analyze
            orb: Maximum orb for aspect consideration
            
        Returns:
            List of aspect dictionaries
        """
        aspects = []
        major_aspects = {
            'conjunction': 0,
            'sextile': 60,
            'square': 90,
            'trine': 120,
            'opposition': 180
        }
        
        planet_names = list(chart.planets.keys())
        
        for i, planet1 in enumerate(planet_names):
            for planet2 in planet_names[i+1:]:
                angle = abs(chart.planets[planet1].longitude - chart.planets[planet2].longitude)
                if angle > 180:
                    angle = 360 - angle
                
                for aspect_name, aspect_angle in major_aspects.items():
                    if abs(angle - aspect_angle) <= orb:
                        aspects.append({
                            'planet1': planet1,
                            'planet2': planet2,
                            'aspect': aspect_name,
                            'angle': angle,
                            'orb': abs(angle - aspect_angle),
                            'exact_angle': aspect_angle
                        })
                        break
        
        return aspects
    
    def close(self):
        """Clean up Swiss Ephemeris resources"""
        swe.close()