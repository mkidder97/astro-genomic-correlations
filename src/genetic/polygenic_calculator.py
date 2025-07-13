"""Polygenic Risk Score (PRS) calculations"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .variant_analyzer import GeneticProfile

@dataclass
class PolygenicRiskScore:
    """Polygenic Risk Score for a specific trait"""
    trait: str
    score: float
    percentile: float
    risk_category: str
    variant_count: int
    confidence: float

class PolygenicCalculator:
    """Calculate Polygenic Risk Scores for various traits"""
    
    # Simplified PRS weights for demonstration
    # In practice, these would come from large GWAS studies
    PRS_WEIGHTS = {
        'cardiovascular_disease': {
            'rs429358': 0.35,   # APOE ε4
            'rs7412': -0.28,    # APOE ε2
            'rs662': 0.15,      # PON1
            'rs1333049': 0.22,  # CDKN2A
            'rs1801133': 0.12   # MTHFR
        },
        'cognitive_ability': {
            'rs4680': -0.18,    # COMT Val158Met
            'rs6265': 0.25,     # BDNF
            'rs25531': 0.15,    # 5-HTTLPR
            'rs1800497': -0.12  # DRD2
        },
        'inflammatory_response': {
            'rs1800629': 0.30,  # TNF-α
            'rs1800896': -0.20, # IL-10
            'rs1143634': 0.25,  # IL-1β
            'rs16944': 0.18     # IL-6
        },
        'metabolic_efficiency': {
            'rs1801133': 0.22,  # MTHFR
            'rs1801282': -0.28, # PPARG
            'rs7903146': 0.32,  # TCF7L2
            'rs9939609': 0.18   # FTO
        },
        'athletic_performance': {
            'rs1815739': 0.45,  # ACTN3 R577X
            'rs4994': 0.25,     # ACE I/D
            'rs1800012': 0.15   # COL1A1
        }
    }
    
    # Population percentile references (simplified)
    POPULATION_REFERENCES = {
        'cardiovascular_disease': {
            'mean': 0.0,
            'std': 1.0,
            'high_risk_threshold': 1.5
        },
        'cognitive_ability': {
            'mean': 0.0,
            'std': 1.0,
            'high_ability_threshold': 1.0
        },
        'inflammatory_response': {
            'mean': 0.0,
            'std': 1.0,
            'high_inflammation_threshold': 1.2
        },
        'metabolic_efficiency': {
            'mean': 0.0,
            'std': 1.0,
            'efficient_threshold': -0.5
        },
        'athletic_performance': {
            'mean': 0.0,
            'std': 1.0,
            'elite_threshold': 1.8
        }
    }
    
    def __init__(self):
        """Initialize polygenic calculator"""
        self.trait_weights = self.PRS_WEIGHTS.copy()
        self.references = self.POPULATION_REFERENCES.copy()
    
    def calculate_prs(self, profile: GeneticProfile, trait: str) -> PolygenicRiskScore:
        """Calculate Polygenic Risk Score for a specific trait
        
        Args:
            profile: Genetic profile
            trait: Trait name (e.g., 'cardiovascular_disease')
            
        Returns:
            PolygenicRiskScore object
        """
        if trait not in self.trait_weights:
            raise ValueError(f"Unknown trait: {trait}")
        
        weights = self.trait_weights[trait]
        score = 0.0
        variant_count = 0
        
        for rsid, weight in weights.items():
            if rsid in profile.variants:
                variant = profile.variants[rsid]
                genotype_effect = self._calculate_genotype_effect(variant.genotype, weight)
                score += genotype_effect
                variant_count += 1
        
        # Normalize score
        if variant_count > 0:
            score = score / np.sqrt(variant_count)  # Adjust for variant count
        
        # Calculate percentile and risk category
        percentile = self._calculate_percentile(score, trait)
        risk_category = self._determine_risk_category(score, trait)
        confidence = min(variant_count / len(weights), 1.0)  # Confidence based on coverage
        
        return PolygenicRiskScore(
            trait=trait,
            score=score,
            percentile=percentile,
            risk_category=risk_category,
            variant_count=variant_count,
            confidence=confidence
        )
    
    def _calculate_genotype_effect(self, genotype: str, weight: float) -> float:
        """Calculate effect based on genotype and weight"""
        if len(genotype) != 2:
            return 0.0
        
        # Count risk alleles (simplified - assumes second allele is risk allele)
        risk_allele_count = 0
        if genotype[0] == genotype[1]:
            # Homozygous
            if weight > 0:  # Risk variant
                risk_allele_count = 2
            else:  # Protective variant
                risk_allele_count = 0
        else:
            # Heterozygous
            risk_allele_count = 1
        
        return weight * risk_allele_count
    
    def _calculate_percentile(self, score: float, trait: str) -> float:
        """Calculate population percentile for the score"""
        ref = self.references[trait]
        
        # Convert to z-score
        z_score = (score - ref['mean']) / ref['std']
        
        # Convert to percentile using normal CDF
        from scipy.stats import norm
        percentile = norm.cdf(z_score) * 100
        
        return max(0, min(100, percentile))
    
    def _determine_risk_category(self, score: float, trait: str) -> str:
        """Determine risk category based on score"""
        ref = self.references[trait]
        z_score = (score - ref['mean']) / ref['std']
        
        if trait == 'cardiovascular_disease':
            if z_score >= ref['high_risk_threshold']:
                return 'High Risk'
            elif z_score >= 0.5:
                return 'Moderate Risk'
            elif z_score >= -0.5:
                return 'Average Risk'
            else:
                return 'Low Risk'
        
        elif trait == 'cognitive_ability':
            if z_score >= ref['high_ability_threshold']:
                return 'High Ability'
            elif z_score >= 0:
                return 'Above Average'
            elif z_score >= -1:
                return 'Average'
            else:
                return 'Below Average'
        
        elif trait == 'inflammatory_response':
            if z_score >= ref['high_inflammation_threshold']:
                return 'High Inflammation'
            elif z_score >= 0:
                return 'Moderate Inflammation'
            else:
                return 'Low Inflammation'
        
        elif trait == 'metabolic_efficiency':
            if z_score <= ref['efficient_threshold']:
                return 'Highly Efficient'
            elif z_score <= 0:
                return 'Efficient'
            elif z_score <= 1:
                return 'Average'
            else:
                return 'Inefficient'
        
        elif trait == 'athletic_performance':
            if z_score >= ref['elite_threshold']:
                return 'Elite Potential'
            elif z_score >= 1:
                return 'High Potential'
            elif z_score >= 0:
                return 'Above Average'
            else:
                return 'Average'
        
        return 'Unknown'
    
    def calculate_all_prs(self, profile: GeneticProfile) -> Dict[str, PolygenicRiskScore]:
        """Calculate PRS for all available traits
        
        Args:
            profile: Genetic profile
            
        Returns:
            Dictionary mapping trait names to PRS scores
        """
        prs_scores = {}
        
        for trait in self.trait_weights.keys():
            prs_scores[trait] = self.calculate_prs(profile, trait)
        
        return prs_scores
    
    def get_top_risk_traits(self, profile: GeneticProfile, n: int = 3) -> List[PolygenicRiskScore]:
        """Get top risk traits based on percentile scores
        
        Args:
            profile: Genetic profile
            n: Number of top traits to return
            
        Returns:
            List of top risk PRS scores
        """
        all_prs = self.calculate_all_prs(profile)
        
        # Sort by percentile (descending for risk traits)
        sorted_prs = sorted(
            all_prs.values(),
            key=lambda prs: prs.percentile if 'risk' in prs.trait or 'disease' in prs.trait else 100 - prs.percentile,
            reverse=True
        )
        
        return sorted_prs[:n]
    
    def add_custom_trait(self, trait_name: str, variant_weights: Dict[str, float], 
                        population_params: Dict[str, float]):
        """Add custom trait for PRS calculation
        
        Args:
            trait_name: Name of the new trait
            variant_weights: Dictionary mapping RSIDs to effect weights
            population_params: Population parameters (mean, std, thresholds)
        """
        self.trait_weights[trait_name] = variant_weights
        self.references[trait_name] = population_params