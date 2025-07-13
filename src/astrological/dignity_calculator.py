"""Traditional astrological dignity calculations"""

import numpy as np
from typing import Dict, List
from .chart_calculator import BirthChart

class DignityCalculator:
    """Calculate traditional astrological dignities and strengths"""
    
    # Traditional rulerships
    DOMICILES = {
        'sun': ['Leo'],
        'moon': ['Cancer'],
        'mercury': ['Gemini', 'Virgo'],
        'venus': ['Taurus', 'Libra'],
        'mars': ['Aries', 'Scorpio'],
        'jupiter': ['Sagittarius', 'Pisces'],
        'saturn': ['Capricorn', 'Aquarius']
    }
    
    EXALTATIONS = {
        'sun': 'Aries',
        'moon': 'Taurus',
        'mercury': 'Virgo',
        'venus': 'Pisces',
        'mars': 'Capricorn',
        'jupiter': 'Cancer',
        'saturn': 'Libra'
    }
    
    DETRIMENTS = {
        'sun': ['Aquarius'],
        'moon': ['Capricorn'],
        'mercury': ['Sagittarius', 'Pisces'],
        'venus': ['Scorpio', 'Aries'],
        'mars': ['Libra', 'Taurus'],
        'jupiter': ['Gemini', 'Virgo'],
        'saturn': ['Cancer', 'Leo']
    }
    
    FALLS = {
        'sun': 'Libra',
        'moon': 'Scorpio',
        'mercury': 'Pisces',
        'venus': 'Virgo',
        'mars': 'Cancer',
        'jupiter': 'Capricorn',
        'saturn': 'Aries'
    }
    
    # Triplicity rulers (by element)
    TRIPLICITIES = {
        'fire': {'day': 'sun', 'night': 'jupiter'},  # Aries, Leo, Sagittarius
        'earth': {'day': 'venus', 'night': 'moon'},  # Taurus, Virgo, Capricorn
        'air': {'day': 'saturn', 'night': 'mercury'},  # Gemini, Libra, Aquarius
        'water': {'day': 'mars', 'night': 'mars'}  # Cancer, Scorpio, Pisces
    }
    
    SIGN_ELEMENTS = {
        'Aries': 'fire', 'Leo': 'fire', 'Sagittarius': 'fire',
        'Taurus': 'earth', 'Virgo': 'earth', 'Capricorn': 'earth',
        'Gemini': 'air', 'Libra': 'air', 'Aquarius': 'air',
        'Cancer': 'water', 'Scorpio': 'water', 'Pisces': 'water'
    }
    
    def calculate_dignity_score(self, chart: BirthChart, planet: str) -> Dict[str, float]:
        """Calculate comprehensive dignity score for a planet
        
        Args:
            chart: Birth chart
            planet: Planet name
            
        Returns:
            Dictionary with dignity breakdown and total score
        """
        if planet not in chart.planets:
            raise ValueError(f"Planet {planet} not found in chart")
        
        planet_pos = chart.planets[planet]
        sign = planet_pos.sign
        
        scores = {
            'domicile': 0,
            'exaltation': 0,
            'triplicity': 0,
            'term': 0,  # Simplified for now
            'face': 0,   # Simplified for now
            'detriment': 0,
            'fall': 0
        }
        
        # Check domicile (+5 points)
        if planet in self.DOMICILES and sign in self.DOMICILES[planet]:
            scores['domicile'] = 5
        
        # Check exaltation (+4 points)
        if planet in self.EXALTATIONS and sign == self.EXALTATIONS[planet]:
            scores['exaltation'] = 4
        
        # Check detriment (-5 points)
        if planet in self.DETRIMENTS and sign in self.DETRIMENTS[planet]:
            scores['detriment'] = -5
        
        # Check fall (-4 points)
        if planet in self.FALLS and sign == self.FALLS[planet]:
            scores['fall'] = -4
        
        # Check triplicity (+3 points)
        if sign in self.SIGN_ELEMENTS:
            element = self.SIGN_ELEMENTS[sign]
            if element in self.TRIPLICITIES:
                # Simplified: assume day chart for now
                triplicity_ruler = self.TRIPLICITIES[element]['day']
                if planet == triplicity_ruler:
                    scores['triplicity'] = 3
        
        # Calculate total score
        total_score = sum(scores.values())
        
        return {
            **scores,
            'total': total_score,
            'sign': sign,
            'degree': planet_pos.degree_in_sign
        }
    
    def calculate_all_dignities(self, chart: BirthChart) -> Dict[str, Dict]:
        """Calculate dignity scores for all planets
        
        Args:
            chart: Birth chart
            
        Returns:
            Dictionary mapping planet names to dignity scores
        """
        dignities = {}
        
        for planet_name in chart.planets.keys():
            if planet_name in ['uranus', 'neptune', 'pluto']:
                continue  # Skip modern planets for traditional dignity
            
            dignities[planet_name] = self.calculate_dignity_score(chart, planet_name)
        
        return dignities
    
    def calculate_chart_strength(self, chart: BirthChart) -> float:
        """Calculate overall chart strength based on dignities
        
        Args:
            chart: Birth chart
            
        Returns:
            Total strength score for the chart
        """
        dignities = self.calculate_all_dignities(chart)
        
        total_strength = sum(
            dignity_info['total'] for dignity_info in dignities.values()
        )
        
        return total_strength
    
    def get_strongest_planets(self, chart: BirthChart, n: int = 3) -> List[Dict]:
        """Get the strongest planets by dignity
        
        Args:
            chart: Birth chart
            n: Number of strongest planets to return
            
        Returns:
            List of dictionaries with planet name and strength info
        """
        dignities = self.calculate_all_dignities(chart)
        
        # Sort by total score
        sorted_planets = sorted(
            [(planet, info) for planet, info in dignities.items()],
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        return [
            {
                'planet': planet,
                'total_score': info['total'],
                'sign': info['sign'],
                'degree': info['degree']
            }
            for planet, info in sorted_planets[:n]
        ]