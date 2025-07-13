"""Comprehensive Analysis Framework - Integrates all methodologies"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ..astrological.chart_calculator import ChartCalculator, BirthChart
from ..genetic.variant_analyzer import VariantAnalyzer, GeneticProfile
from ..correlation.dignity_correlation import DignityCorrelation
from ..correlation.pathway_correlation import PathwayCorrelation
from ..statistical.validation import StatisticalValidator

@dataclass
class ComprehensiveResults:
    """Complete analysis results from all methodologies"""
    overall_correlation: float
    confidence_level: float
    methodology_results: Dict[str, Dict]
    top_correlations: List[Dict]
    statistical_validation: Dict
    interpretation: str
    recommendations: List[str]

class ComprehensiveAnalyzer:
    """Main analyzer implementing the integrated methodology framework"""
    
    def __init__(self):
        """Initialize comprehensive analyzer with all components"""
        self.chart_calc = ChartCalculator()
        self.variant_analyzer = VariantAnalyzer()
        self.dignity_correlation = DignityCorrelation()
        self.pathway_correlation = PathwayCorrelation()
        self.statistical_validator = StatisticalValidator()
    
    def comprehensive_astro_genetic_analysis(self, birth_datetime: datetime, 
                                           latitude: float, longitude: float,
                                           genetic_file_path: str) -> ComprehensiveResults:
        """Perform comprehensive astro-genetic correlation analysis
        
        Args:
            birth_datetime: Birth date and time (UTC)
            latitude: Geographic latitude 
            longitude: Geographic longitude
            genetic_file_path: Path to genetic data file
            
        Returns:
            Complete analysis results
        """
        # Step 1: Calculate birth chart
        chart = self.chart_calc.calculate_chart(birth_datetime, latitude, longitude)
        
        # Step 2: Load and process genetic data
        profile = self.variant_analyzer.load_genetic_data(genetic_file_path)
        
        # Step 3: Run all correlation methodologies
        methodology_results = {}
        
        # Traditional Dignity Analysis (Core Method)
        dignity_results = self.dignity_correlation.analyze_dignity_genetic_correlation(chart, profile)
        methodology_results['dignity'] = {
            'correlation': dignity_results.correlation_coefficient,
            'p_value': dignity_results.p_value,
            'confidence_interval': dignity_results.confidence_interval,
            'significant_correlations': dignity_results.significant_correlations,
            'method_weight': 0.4  # Highest weight as recommended
        }
        
        # Pathway Analysis (High Priority Method)
        pathway_results = self.pathway_correlation.analyze_planetary_pathway_correlations(chart, profile)
        methodology_results['pathway'] = {
            'correlation': pathway_results.overall_correlation,
            'p_value': pathway_results.p_value,
            'strongest_correlations': pathway_results.strongest_correlations,
            'confidence_level': pathway_results.confidence_level,
            'method_weight': 0.35  # Second highest weight
        }
        
        # Polygenic Risk Score Analysis
        polygenic_results = self._analyze_polygenic_correlations(chart, profile)
        methodology_results['polygenic'] = {
            'correlation': polygenic_results['overall_correlation'],
            'trait_correlations': polygenic_results['trait_correlations'],
            'confidence': polygenic_results['confidence'],
            'method_weight': 0.25  # Third priority
        }
        
        # Step 4: Meta-analysis across methods
        meta_results = self._meta_analyze_results(methodology_results)
        
        # Step 5: Statistical validation
        validation_results = self._validate_results(methodology_results, chart, profile)
        
        # Step 6: Generate interpretation and recommendations
        interpretation = self._generate_interpretation(methodology_results, meta_results)
        recommendations = self._generate_recommendations(methodology_results, validation_results)
        
        return ComprehensiveResults(
            overall_correlation=meta_results['combined_correlation'],
            confidence_level=meta_results['combined_confidence'],
            methodology_results=methodology_results,
            top_correlations=meta_results['top_correlations'],
            statistical_validation=validation_results,
            interpretation=interpretation,
            recommendations=recommendations
        )
    
    def _analyze_polygenic_correlations(self, chart: BirthChart, profile: GeneticProfile) -> Dict:
        """Analyze correlations using polygenic risk scores"""
        from ..genetic.polygenic_calculator import PolygenicCalculator
        
        polygenic_calc = PolygenicCalculator()
        prs_scores = polygenic_calc.calculate_all_prs(profile)
        
        # Map PRS traits to planetary strengths
        dignity_scores = self.dignity_correlation.dignity_calc.calculate_all_dignities(chart)
        
        trait_correlations = {}
        correlations = []
        
        # Trait-planet mappings based on traditional rulerships
        trait_planet_map = {
            'cardiovascular_disease': 'sun',
            'cognitive_ability': 'mercury', 
            'inflammatory_response': 'mars',
            'metabolic_efficiency': 'venus',
            'athletic_performance': 'mars'
        }
        
        for trait, planet in trait_planet_map.items():
            if trait in prs_scores and planet in dignity_scores:
                prs_score = prs_scores[trait].score
                dignity_score = dignity_scores[planet]['total']
                
                # Calculate correlation between PRS and dignity
                correlation = np.tanh(prs_score) * np.tanh(dignity_score / 5.0)
                
                trait_correlations[trait] = {
                    'correlation': correlation,
                    'prs_score': prs_score,
                    'prs_percentile': prs_scores[trait].percentile,
                    'dignity_score': dignity_score,
                    'confidence': prs_scores[trait].confidence
                }
                
                correlations.append(correlation)
        
        overall_correlation = np.mean(correlations) if correlations else 0.0
        confidence = np.mean([tc['confidence'] for tc in trait_correlations.values()]) if trait_correlations else 0.0
        
        return {
            'overall_correlation': overall_correlation,
            'trait_correlations': trait_correlations,
            'confidence': confidence
        }
    
    def _meta_analyze_results(self, methodology_results: Dict[str, Dict]) -> Dict:
        """Perform meta-analysis across all methodologies"""
        # Weight correlations by method importance and confidence
        weighted_correlations = []
        total_weight = 0.0
        
        for method_name, results in methodology_results.items():
            correlation = results['correlation']
            weight = results['method_weight']
            
            # Adjust weight by method-specific confidence if available
            if 'confidence_level' in results:
                weight *= results['confidence_level']
            elif 'confidence' in results:
                weight *= results['confidence']
            
            weighted_correlations.append(correlation * weight)
            total_weight += weight
        
        # Calculate combined correlation
        if total_weight > 0:
            combined_correlation = sum(weighted_correlations) / total_weight
        else:
            combined_correlation = 0.0
        
        # Calculate combined confidence
        confidences = []
        for results in methodology_results.values():
            if 'confidence_level' in results:
                confidences.append(results['confidence_level'])
            elif 'confidence' in results:
                confidences.append(results['confidence'])
        
        combined_confidence = np.mean(confidences) if confidences else 0.0
        
        # Identify top correlations across all methods
        top_correlations = self._extract_top_correlations(methodology_results)
        
        return {
            'combined_correlation': combined_correlation,
            'combined_confidence': combined_confidence,
            'total_weight': total_weight,
            'top_correlations': top_correlations
        }
    
    def _extract_top_correlations(self, methodology_results: Dict) -> List[Dict]:
        """Extract top correlations from all methodologies"""
        all_correlations = []
        
        # From dignity analysis
        if 'dignity' in methodology_results:
            for corr in methodology_results['dignity'].get('significant_correlations', []):
                all_correlations.append({
                    'method': 'dignity',
                    'type': 'planet-genetic',
                    'strength': corr['strength'],
                    'details': corr
                })
        
        # From pathway analysis  
        if 'pathway' in methodology_results:
            for corr in methodology_results['pathway'].get('strongest_correlations', []):
                all_correlations.append({
                    'method': 'pathway',
                    'type': 'planet-pathway',
                    'strength': corr['strength'],
                    'details': corr
                })
        
        # From polygenic analysis
        if 'polygenic' in methodology_results:
            for trait, corr_info in methodology_results['polygenic'].get('trait_correlations', {}).items():
                all_correlations.append({
                    'method': 'polygenic',
                    'type': 'trait-planet',
                    'strength': abs(corr_info['correlation']) * corr_info['confidence'],
                    'details': {'trait': trait, **corr_info}
                })
        
        # Sort by strength and return top 5
        return sorted(all_correlations, key=lambda x: x['strength'], reverse=True)[:5]
    
    def _validate_results(self, methodology_results: Dict, chart: BirthChart, profile: GeneticProfile) -> Dict:
        """Statistical validation of results"""
        validation = {}
        
        # Basic validation metrics
        correlations = [results['correlation'] for results in methodology_results.values()]
        
        validation['consistency'] = {
            'mean_correlation': np.mean(correlations),
            'std_correlation': np.std(correlations),
            'min_correlation': np.min(correlations),
            'max_correlation': np.max(correlations)
        }
        
        # Data quality assessment
        validation['data_quality'] = {
            'genetic_variant_count': len(profile.variants),
            'chart_completeness': len(chart.planets) / 10.0,  # 10 traditional planets
            'adequate_sample': len(profile.variants) >= 10
        }
        
        # Statistical significance
        significant_methods = 0
        for results in methodology_results.values():
            if results.get('p_value', 1.0) < 0.05:
                significant_methods += 1
        
        validation['significance'] = {
            'significant_methods': significant_methods,
            'total_methods': len(methodology_results),
            'significance_ratio': significant_methods / len(methodology_results)
        }
        
        return validation
    
    def _generate_interpretation(self, methodology_results: Dict, meta_results: Dict) -> str:
        """Generate human-readable interpretation"""
        combined_corr = meta_results['combined_correlation']
        combined_conf = meta_results['combined_confidence']
        
        # Determine overall strength
        if abs(combined_corr) > 0.6 and combined_conf > 0.7:
            strength = "strong"
        elif abs(combined_corr) > 0.3 and combined_conf > 0.5:
            strength = "moderate"
        else:
            strength = "weak"
        
        direction = "positive" if combined_corr > 0 else "negative"
        
        interpretation = f"""COMPREHENSIVE ASTRO-GENOMIC ANALYSIS RESULTS:

Overall Finding: {strength.title()} {direction} correlation detected between astrological factors and genetic expression.

Combined Correlation: {combined_corr:.3f}
Confidence Level: {combined_conf:.1%}

METHOD BREAKDOWN:
"""
        
        # Add method-specific interpretations
        for method, results in methodology_results.items():
            corr = results['correlation']
            interpretation += f"\n• {method.title()}: {corr:.3f} correlation"
        
        # Add top findings
        top_corrs = meta_results['top_correlations'][:3]
        if top_corrs:
            interpretation += "\n\nTOP CORRELATIONS:\n"
            for i, corr in enumerate(top_corrs, 1):
                interpretation += f"{i}. {corr['method'].title()} method: {corr['details']}\n"
        
        return interpretation
    
    def _generate_recommendations(self, methodology_results: Dict, validation_results: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Data quality recommendations
        variant_count = validation_results['data_quality']['genetic_variant_count']
        if variant_count < 20:
            recommendations.append(f"Consider expanding genetic testing - only {variant_count} variants analyzed. 50+ recommended for higher accuracy.")
        
        # Method-specific recommendations
        best_method = max(methodology_results.items(), key=lambda x: abs(x[1]['correlation']))
        recommendations.append(f"The {best_method[0]} methodology showed strongest results - consider focusing further analysis here.")
        
        # Statistical recommendations
        significance_ratio = validation_results['significance']['significance_ratio']
        if significance_ratio < 0.5:
            recommendations.append("Statistical significance is limited - consider larger sample size or additional data points.")
        
        # Practical recommendations
        combined_corr = max(abs(results['correlation']) for results in methodology_results.values())
        if combined_corr > 0.5:
            recommendations.append("Strong correlations detected - results warrant further investigation and replication studies.")
        elif combined_corr > 0.3:
            recommendations.append("Moderate correlations suggest potential relationships - additional data would strengthen analysis.")
        else:
            recommendations.append("Weak correlations observed - consider alternative methodologies or different genetic markers.")
        
        return recommendations