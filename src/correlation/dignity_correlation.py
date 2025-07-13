"""Traditional Dignity Correlation Analysis"""

import numpy as np
from scipy.stats import pearsonr, spearmanr
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from ..astrological.chart_calculator import BirthChart
from ..astrological.dignity_calculator import DignityCalculator
from ..genetic.variant_analyzer import GeneticProfile
from ..genetic.polygenic_calculator import PolygenicCalculator

@dataclass
class DignityCorrelationResult:
    """Results from dignity-genetic correlation analysis"""
    correlation_coefficient: float
    p_value: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    method: str
    dignity_scores: Dict[str, float]
    genetic_scores: Dict[str, float]
    significant_correlations: List[Dict]

class DignityCorrelation:
    """Correlate traditional astrological dignities with genetic effect sizes"""
    
    def __init__(self):
        """Initialize dignity correlation analyzer"""
        self.dignity_calc = DignityCalculator()
        self.polygenic_calc = PolygenicCalculator()
    
    def analyze_dignity_genetic_correlation(self, chart: BirthChart, profile: GeneticProfile) -> DignityCorrelationResult:
        """Analyze correlation between traditional dignities and genetic effects
        
        Args:
            chart: Birth chart
            profile: Genetic profile
            
        Returns:
            Correlation analysis results
        """
        # Calculate dignity scores for all planets
        dignity_scores = self.dignity_calc.calculate_all_dignities(chart)
        
        # Calculate genetic impact scores
        genetic_impact = self._calculate_weighted_genetic_impact(profile)
        
        # Prepare data for correlation
        dignity_values = []
        genetic_values = []
        planet_names = []
        
        for planet in dignity_scores.keys():
            if planet in genetic_impact:
                dignity_values.append(dignity_scores[planet]['total'])
                genetic_values.append(genetic_impact[planet])
                planet_names.append(planet)
        
        if len(dignity_values) < 3:
            raise ValueError("Insufficient data for correlation analysis")
        
        # Calculate correlation
        correlation, p_value = spearmanr(dignity_values, genetic_values)
        
        # Calculate confidence interval (bootstrap method)
        ci_lower, ci_upper = self._bootstrap_confidence_interval(
            dignity_values, genetic_values, correlation
        )
        
        # Identify significant individual correlations
        significant_correlations = self._find_significant_individual_correlations(
            dignity_scores, genetic_impact
        )
        
        return DignityCorrelationResult(
            correlation_coefficient=correlation,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            sample_size=len(dignity_values),
            method="Spearman",
            dignity_scores={planet: dignity_scores[planet]['total'] for planet in planet_names},
            genetic_scores={planet: genetic_impact[planet] for planet in planet_names},
            significant_correlations=significant_correlations
        )
    
    def _calculate_weighted_genetic_impact(self, profile: GeneticProfile) -> Dict[str, float]:
        """Calculate weighted genetic impact scores mapped to planetary rulerships"""
        impact_scores = {}
        
        # Traditional planetary rulerships for genetic traits
        planetary_traits = {
            'sun': ['cardiovascular_disease', 'vitality'],
            'moon': ['emotional_regulation', 'circadian'],
            'mercury': ['cognitive_ability', 'nervous_system'],
            'venus': ['metabolic_efficiency', 'hormonal'],
            'mars': ['inflammatory_response', 'athletic_performance'],
            'jupiter': ['growth', 'liver_function'],
            'saturn': ['structural', 'aging']
        }
        
        # Calculate PRS scores for available traits
        prs_scores = self.polygenic_calc.calculate_all_prs(profile)
        
        for planet, traits in planetary_traits.items():
            planet_score = 0.0
            trait_count = 0
            
            for trait in traits:
                if trait in prs_scores:
                    # Convert percentile to z-score for better correlation
                    percentile = prs_scores[trait].percentile
                    z_score = self._percentile_to_zscore(percentile)
                    planet_score += z_score * prs_scores[trait].confidence
                    trait_count += 1
            
            if trait_count > 0:
                impact_scores[planet] = planet_score / trait_count
            else:
                impact_scores[planet] = 0.0
        
        return impact_scores
    
    def _percentile_to_zscore(self, percentile: float) -> float:
        """Convert percentile to z-score"""
        from scipy.stats import norm
        return norm.ppf(percentile / 100.0)
    
    def _bootstrap_confidence_interval(self, x: List[float], y: List[float], 
                                     observed_corr: float, n_bootstrap: int = 1000) -> Tuple[float, float]:
        """Calculate bootstrap confidence interval for correlation"""
        correlations = []
        n = len(x)
        
        for _ in range(n_bootstrap):
            # Resample with replacement
            indices = np.random.choice(n, size=n, replace=True)
            x_boot = [x[i] for i in indices]
            y_boot = [y[i] for i in indices]
            
            try:
                corr, _ = spearmanr(x_boot, y_boot)
                if not np.isnan(corr):
                    correlations.append(corr)
            except:
                continue
        
        if len(correlations) == 0:
            return (-1.0, 1.0)
        
        # Calculate 95% confidence interval
        correlations.sort()
        lower_idx = int(0.025 * len(correlations))
        upper_idx = int(0.975 * len(correlations))
        
        return (correlations[lower_idx], correlations[upper_idx])
    
    def _find_significant_individual_correlations(self, dignity_scores: Dict, 
                                                genetic_impact: Dict, 
                                                alpha: float = 0.05) -> List[Dict]:
        """Find individually significant planet-trait correlations"""
        significant = []
        
        for planet in dignity_scores.keys():
            if planet in genetic_impact:
                dignity_score = dignity_scores[planet]['total']
                genetic_score = genetic_impact[planet]
                
                # Simple significance test (would need more data points in practice)
                if abs(dignity_score) > 2 and abs(genetic_score) > 1:
                    significant.append({
                        'planet': planet,
                        'dignity_score': dignity_score,
                        'genetic_score': genetic_score,
                        'strength': abs(dignity_score * genetic_score),
                        'sign': dignity_scores[planet]['sign']
                    })
        
        return sorted(significant, key=lambda x: x['strength'], reverse=True)
    
    def analyze_planetary_genetic_mapping(self, chart: BirthChart, profile: GeneticProfile) -> Dict[str, Dict]:
        """Detailed analysis of planetary-genetic mappings
        
        Args:
            chart: Birth chart
            profile: Genetic profile
            
        Returns:
            Detailed mapping analysis
        """
        dignity_scores = self.dignity_calc.calculate_all_dignities(chart)
        genetic_impact = self._calculate_weighted_genetic_impact(profile)
        
        planetary_analysis = {}
        
        for planet in dignity_scores.keys():
            if planet in genetic_impact:
                dignity_info = dignity_scores[planet]
                genetic_score = genetic_impact[planet]
                
                # Calculate harmony score (how well dignity matches genetic expression)
                harmony_score = self._calculate_harmony_score(dignity_info['total'], genetic_score)
                
                planetary_analysis[planet] = {
                    'dignity_total': dignity_info['total'],
                    'dignity_breakdown': {
                        key: value for key, value in dignity_info.items() 
                        if key not in ['total', 'sign', 'degree']
                    },
                    'genetic_impact': genetic_score,
                    'harmony_score': harmony_score,
                    'sign': dignity_info['sign'],
                    'degree': dignity_info['degree'],
                    'interpretation': self._interpret_planetary_correlation(
                        planet, dignity_info['total'], genetic_score, harmony_score
                    )
                }
        
        return planetary_analysis
    
    def _calculate_harmony_score(self, dignity_score: float, genetic_score: float) -> float:
        """Calculate harmony between dignity and genetic expression
        
        Positive harmony: Both high or both low
        Negative harmony: One high, one low
        """
        # Normalize scores to same scale
        dignity_norm = np.tanh(dignity_score / 5.0)  # Dignity scores typically -5 to +5
        genetic_norm = np.tanh(genetic_score)         # Genetic scores are z-scores
        
        # Calculate harmony as product (same sign = positive harmony)
        harmony = dignity_norm * genetic_norm
        
        return harmony
    
    def _interpret_planetary_correlation(self, planet: str, dignity_score: float, 
                                       genetic_score: float, harmony_score: float) -> str:
        """Generate interpretation of planetary correlation"""
        dignity_strength = "strong" if abs(dignity_score) > 3 else "moderate" if abs(dignity_score) > 1 else "weak"
        dignity_nature = "dignified" if dignity_score > 0 else "debilitated"
        
        genetic_strength = "strong" if abs(genetic_score) > 1.5 else "moderate" if abs(genetic_score) > 0.5 else "weak"
        genetic_nature = "elevated" if genetic_score > 0 else "suppressed"
        
        harmony_nature = "harmonious" if harmony_score > 0.3 else "conflicting" if harmony_score < -0.3 else "neutral"
        
        return f"{planet.title()} shows {dignity_strength} {dignity_nature} dignity with {genetic_strength} {genetic_nature} genetic expression - {harmony_nature} correlation"