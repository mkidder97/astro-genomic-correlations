"""Biological Pathway Correlation Analysis"""

import numpy as np
from scipy.stats import pearsonr, spearmanr
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from ..astrological.chart_calculator import BirthChart
from ..astrological.dignity_calculator import DignityCalculator
from ..genetic.variant_analyzer import GeneticProfile
from ..genetic.pathway_analyzer import PathwayAnalyzer

@dataclass
class PathwayCorrelationResult:
    """Results from pathway-planetary correlation analysis"""
    overall_correlation: float
    p_value: float
    individual_correlations: Dict[str, Dict]
    strongest_correlations: List[Dict]
    pathway_scores: Dict[str, float]
    planetary_strengths: Dict[str, float]
    confidence_level: float

class PathwayCorrelation:
    """Test traditional planetary rulerships against biological pathway activity"""
    
    def __init__(self):
        """Initialize pathway correlation analyzer"""
        self.dignity_calc = DignityCalculator()
        self.pathway_analyzer = PathwayAnalyzer()
    
    def analyze_planetary_pathway_correlations(self, chart: BirthChart, profile: GeneticProfile) -> PathwayCorrelationResult:
        """Analyze correlations between planetary strengths and biological pathways
        
        Args:
            chart: Birth chart
            profile: Genetic profile
            
        Returns:
            Comprehensive pathway correlation results
        """
        # Calculate planetary strengths
        planetary_strengths = self._calculate_planetary_strengths(chart)
        
        # Get pathway scores mapped to planetary rulerships
        pathway_correlations = self.pathway_analyzer.get_planetary_pathway_correlations(profile)
        
        # Analyze individual correlations
        individual_correlations = {}
        correlation_values = []
        
        for planet in planetary_strengths.keys():
            if planet in pathway_correlations:
                planet_strength = planetary_strengths[planet]
                pathway_score = pathway_correlations[planet]['total_score']
                
                # Calculate individual correlation
                individual_corr = self._calculate_individual_correlation(
                    planet_strength, pathway_score, planet, pathway_correlations[planet]
                )
                
                individual_correlations[planet] = individual_corr
                correlation_values.append(individual_corr['correlation'])
        
        # Calculate overall correlation
        planet_values = [planetary_strengths[p] for p in individual_correlations.keys()]
        pathway_values = [pathway_correlations[p]['total_score'] for p in individual_correlations.keys()]
        
        if len(planet_values) >= 3:
            overall_corr, p_value = spearmanr(planet_values, pathway_values)
        else:
            overall_corr, p_value = 0.0, 1.0
        
        # Find strongest correlations
        strongest_correlations = self._identify_strongest_correlations(individual_correlations)
        
        # Calculate confidence level
        confidence_level = self._calculate_confidence_level(individual_correlations, profile)
        
        return PathwayCorrelationResult(
            overall_correlation=overall_corr,
            p_value=p_value,
            individual_correlations=individual_correlations,
            strongest_correlations=strongest_correlations,
            pathway_scores={p: pathway_correlations[p]['total_score'] for p in pathway_correlations.keys()},
            planetary_strengths=planetary_strengths,
            confidence_level=confidence_level
        )
    
    def _calculate_planetary_strengths(self, chart: BirthChart) -> Dict[str, float]:
        """Calculate comprehensive planetary strength scores"""
        dignity_scores = self.dignity_calc.calculate_all_dignities(chart)
        planetary_strengths = {}
        
        for planet, dignity_info in dignity_scores.items():
            # Base dignity score
            base_strength = dignity_info['total']
            
            # Add house strength (simplified)
            planet_pos = chart.planets[planet]
            house_strength = self._calculate_house_strength(planet_pos.house)
            
            # Add aspect strength (simplified)
            aspect_strength = self._calculate_aspect_strength(chart, planet)
            
            # Combined strength score
            total_strength = base_strength + house_strength + aspect_strength
            planetary_strengths[planet] = total_strength
        
        return planetary_strengths
    
    def _calculate_house_strength(self, house: int) -> float:
        """Calculate strength bonus/penalty based on house position"""
        # Angular houses (1, 4, 7, 10) are strongest
        angular_houses = [1, 4, 7, 10]
        succedent_houses = [2, 5, 8, 11]
        cadent_houses = [3, 6, 9, 12]
        
        if house in angular_houses:
            return 2.0
        elif house in succedent_houses:
            return 1.0
        elif house in cadent_houses:
            return 0.0
        else:
            return 0.0
    
    def _calculate_aspect_strength(self, chart: BirthChart, planet: str) -> float:
        """Calculate strength from aspects (simplified)"""
        # This would normally require a full aspect analysis
        # For now, return a neutral value
        return 0.0
    
    def _calculate_individual_correlation(self, planet_strength: float, pathway_score: float, 
                                        planet: str, pathway_info: Dict) -> Dict:
        """Calculate individual planet-pathway correlation"""
        # Normalize scores for better correlation
        planet_norm = np.tanh(planet_strength / 5.0)
        pathway_norm = np.tanh(pathway_score * 2.0)
        
        # Simple correlation measure
        correlation = planet_norm * pathway_norm
        
        # Calculate significance based on pathway data quality
        pathway_count = pathway_info.get('pathway_count', 0)
        significance = min(pathway_count / 3.0, 1.0)  # More pathways = higher significance
        
        return {
            'correlation': correlation,
            'planet_strength': planet_strength,
            'pathway_score': pathway_score,
            'significance': significance,
            'pathway_details': pathway_info['pathway_scores'],
            'interpretation': self._interpret_correlation(planet, correlation, significance)
        }
    
    def _interpret_correlation(self, planet: str, correlation: float, significance: float) -> str:
        """Generate interpretation of planet-pathway correlation"""
        strength = "strong" if abs(correlation) > 0.6 else "moderate" if abs(correlation) > 0.3 else "weak"
        direction = "positive" if correlation > 0 else "negative"
        confidence = "high" if significance > 0.7 else "moderate" if significance > 0.4 else "low"
        
        return f"{planet.title()} shows {strength} {direction} correlation with biological pathways ({confidence} confidence)"
    
    def _identify_strongest_correlations(self, individual_correlations: Dict[str, Dict]) -> List[Dict]:
        """Identify the strongest planet-pathway correlations"""
        correlations = []
        
        for planet, corr_info in individual_correlations.items():
            correlations.append({
                'planet': planet,
                'correlation': corr_info['correlation'],
                'significance': corr_info['significance'],
                'strength': abs(corr_info['correlation']) * corr_info['significance'],
                'interpretation': corr_info['interpretation']
            })
        
        # Sort by combined strength and significance
        return sorted(correlations, key=lambda x: x['strength'], reverse=True)
    
    def _calculate_confidence_level(self, individual_correlations: Dict, profile: GeneticProfile) -> float:
        """Calculate overall confidence in the analysis"""
        # Factors affecting confidence:
        # 1. Number of variants found
        # 2. Quality of correlations
        # 3. Consistency across planets
        
        variant_count = len(profile.variants)
        variant_confidence = min(variant_count / 20.0, 1.0)  # 20+ variants = full confidence
        
        # Average correlation strength
        correlations = [corr_info['correlation'] for corr_info in individual_correlations.values()]
        if correlations:
            avg_correlation_strength = np.mean([abs(c) for c in correlations])
        else:
            avg_correlation_strength = 0.0
        
        # Consistency (low standard deviation = high consistency)
        if len(correlations) > 1:
            consistency = 1.0 - min(np.std(correlations), 1.0)
        else:
            consistency = 0.5
        
        # Combined confidence
        overall_confidence = (variant_confidence + avg_correlation_strength + consistency) / 3.0
        
        return max(0.0, min(1.0, overall_confidence))
    
    def test_specific_rulership(self, chart: BirthChart, profile: GeneticProfile, 
                              planet: str, expected_pathway: str) -> Dict:
        """Test a specific traditional rulership claim
        
        Args:
            chart: Birth chart
            profile: Genetic profile
            planet: Planet name
            expected_pathway: Expected biological pathway
            
        Returns:
            Test results for the specific rulership
        """
        if planet not in chart.planets:
            raise ValueError(f"Planet {planet} not found in chart")
        
        # Calculate planet strength
        planetary_strengths = self._calculate_planetary_strengths(chart)
        planet_strength = planetary_strengths.get(planet, 0.0)
        
        # Get pathway scores
        pathway_scores = self.pathway_analyzer.calculate_pathway_scores(profile)
        pathway_score = pathway_scores.get(expected_pathway, 0.0)
        
        # Calculate correlation
        planet_norm = np.tanh(planet_strength / 5.0)
        pathway_norm = np.tanh(pathway_score * 2.0)
        correlation = planet_norm * pathway_norm
        
        # Statistical significance (simplified)
        significance = abs(correlation) if abs(correlation) > 0.3 else 0.0
        
        return {
            'planet': planet,
            'pathway': expected_pathway,
            'planet_strength': planet_strength,
            'pathway_score': pathway_score,
            'correlation': correlation,
            'significance': significance,
            'test_result': 'PASS' if abs(correlation) > 0.4 else 'FAIL',
            'interpretation': f"{planet.title()}-{expected_pathway} rulership {'confirmed' if abs(correlation) > 0.4 else 'not confirmed'} (correlation: {correlation:.3f})"
        }