#!/usr/bin/env python3
"""
Genetic Variant Analyzer - Core genetic data processing module
Extracted from comprehensive analysis scripts and modularized
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

@dataclass
class GeneticVariant:
    """Represents a genetic variant with all associated data"""
    rsid: str
    chromosome: str
    position: int
    genotype: str
    effect_size: Optional[float] = None
    clinical_significance: Optional[str] = None
    gene: Optional[str] = None
    pathway: Optional[str] = None
    element: Optional[str] = None
    
    def __post_init__(self):
        """Calculate derived properties"""
        if self.genotype and self.genotype not in ['--', 'II', 'DD']:
            alleles = list(self.genotype.upper())
            if len(alleles) == 2:
                unique_alleles = set(alleles)
                if len(unique_alleles) == 1:
                    self.numeric_genotype = 0 if alleles[0] <= 'G' else 2
                else:
                    self.numeric_genotype = 1  # Heterozygous
                
                self.genotype_category = 'sensitive' if self.numeric_genotype == 0 else (
                    'extreme' if self.numeric_genotype == 2 else 'intermediate'
                )

@dataclass
class GeneticProfile:
    """Complete genetic profile for an individual"""
    sample_id: str
    variants: Dict[str, GeneticVariant]
    total_snps_processed: int = 0
    
    def get_variants_by_element(self) -> Dict[str, List[GeneticVariant]]:
        """Group variants by astrological element"""
        element_variants = {'fire': [], 'earth': [], 'air': [], 'water': []}
        
        for variant in self.variants.values():
            if variant.element and variant.element in element_variants:
                element_variants[variant.element].append(variant)
        
        return element_variants
    
    def get_variants_by_pathway(self) -> Dict[str, List[GeneticVariant]]:
        """Group variants by biological pathway"""
        pathway_variants = {}
        
        for variant in self.variants.values():
            if variant.pathway:
                if variant.pathway not in pathway_variants:
                    pathway_variants[variant.pathway] = []
                pathway_variants[variant.pathway].append(variant)
        
        return pathway_variants

class VariantAnalyzer:
    """Main class for genetic variant analysis"""
    
    def __init__(self):
        """Initialize with comprehensive variant database"""
        self.variant_db = self._load_variant_database()
    
    def _load_variant_database(self) -> Dict[str, Dict]:
        """Load comprehensive genetic variant database with astrological mappings"""
        return {
            # Fire/Inflammation variants (Mars ruled)
            'rs1800896': {
                'gene': 'IL10', 'pathway': 'inflammation', 'element': 'fire', 
                'effect_size': 0.5, 'clinical_significance': 'moderate'
            },
            'rs1143634': {
                'gene': 'IL1B', 'pathway': 'inflammation', 'element': 'fire',
                'effect_size': 0.7, 'clinical_significance': 'moderate'
            },
            'rs20541': {
                'gene': 'IL13', 'pathway': 'inflammation', 'element': 'fire',
                'effect_size': 0.6, 'clinical_significance': 'moderate'
            },
            'rs361525': {
                'gene': 'TNF', 'pathway': 'inflammation', 'element': 'fire',
                'effect_size': 0.8, 'clinical_significance': 'high'
            },
            'rs1800795': {
                'gene': 'IL6', 'pathway': 'inflammation', 'element': 'fire',
                'effect_size': 0.9, 'clinical_significance': 'high'
            },
            'rs1815739': {
                'gene': 'ACTN3', 'pathway': 'athletic', 'element': 'fire',
                'effect_size': 1.2, 'clinical_significance': 'high'
            },
            
            # Earth/Physical variants (Saturn/Venus ruled)
            'rs1801282': {
                'gene': 'PPARG', 'pathway': 'metabolic', 'element': 'earth',
                'effect_size': 1.2, 'clinical_significance': 'high'
            },
            'rs7903146': {
                'gene': 'TCF7L2', 'pathway': 'metabolic', 'element': 'earth',
                'effect_size': 1.5, 'clinical_significance': 'very_high'
            },
            'rs1333049': {
                'gene': 'CDKN2A', 'pathway': 'cardiovascular', 'element': 'earth',
                'effect_size': 1.1, 'clinical_significance': 'moderate'
            },
            'rs10757278': {
                'gene': 'CDKN2A', 'pathway': 'cardiovascular', 'element': 'earth',
                'effect_size': 1.0, 'clinical_significance': 'moderate'
            },
            'rs429358': {
                'gene': 'APOE', 'pathway': 'cardiovascular', 'element': 'earth',
                'effect_size': 2.5, 'clinical_significance': 'very_high'
            },
            'rs7412': {
                'gene': 'APOE', 'pathway': 'cardiovascular', 'element': 'earth',
                'effect_size': -1.8, 'clinical_significance': 'high'  # Protective
            },
            
            # Air/Cognitive variants (Mercury ruled)
            'rs53576': {
                'gene': 'OXTR', 'pathway': 'neurotransmitter', 'element': 'air',
                'effect_size': 0.8, 'clinical_significance': 'moderate'
            },
            'rs6265': {
                'gene': 'BDNF', 'pathway': 'neurotransmitter', 'element': 'air',
                'effect_size': 1.0, 'clinical_significance': 'moderate'
            },
            'rs1800497': {
                'gene': 'DRD2', 'pathway': 'neurotransmitter', 'element': 'air',
                'effect_size': 0.9, 'clinical_significance': 'moderate'
            },
            'rs4680': {
                'gene': 'COMT', 'pathway': 'neurotransmitter', 'element': 'air',
                'effect_size': 0.8, 'clinical_significance': 'moderate'
            },
            
            # Water/Emotional variants (Moon ruled)
            'rs6295': {
                'gene': 'HTR1A', 'pathway': 'emotional', 'element': 'water',
                'effect_size': 0.7, 'clinical_significance': 'moderate'
            },
            'rs1006737': {
                'gene': 'CACNA1C', 'pathway': 'emotional', 'element': 'water',
                'effect_size': 1.1, 'clinical_significance': 'moderate'
            },
            'rs4570625': {
                'gene': 'TPH2', 'pathway': 'emotional', 'element': 'water',
                'effect_size': 0.9, 'clinical_significance': 'moderate'
            },
            
            # Additional high-impact variants
            'rs1801133': {
                'gene': 'MTHFR', 'pathway': 'metabolic', 'element': 'earth',
                'effect_size': 1.3, 'clinical_significance': 'high'
            },
            'rs662': {
                'gene': 'PON1', 'pathway': 'detoxification', 'element': 'earth',
                'effect_size': 0.6, 'clinical_significance': 'moderate'
            },
            'rs1045642': {
                'gene': 'ABCB1', 'pathway': 'drug_metabolism', 'element': 'earth',
                'effect_size': 0.7, 'clinical_significance': 'moderate'
            }
        }
    
    def load_genetic_data(self, file_path: str) -> GeneticProfile:
        """Load genetic data from 23andMe or similar format"""
        found_variants = {}
        total_lines = 0
        
        print(f"📊 Loading genetic data from {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    total_lines += 1
                    
                    if total_lines % 100000 == 0:
                        print(f"   Processing line {total_lines:,}...")
                    
                    if line.startswith('#'):
                        continue
                    
                    parts = line.strip().split('\t')
                    if len(parts) >= 4:
                        rsid = parts[0]
                        chromosome = parts[1]
                        position = parts[2]
                        genotype = parts[3]
                        
                        if rsid in self.variant_db:
                            variant_info = self.variant_db[rsid]
                            
                            variant = GeneticVariant(
                                rsid=rsid,
                                chromosome=chromosome,
                                position=int(position),
                                genotype=genotype,
                                gene=variant_info['gene'],
                                pathway=variant_info['pathway'],
                                element=variant_info['element'],
                                effect_size=variant_info['effect_size'],
                                clinical_significance=variant_info['clinical_significance']
                            )
                            
                            found_variants[rsid] = variant
            
            profile = GeneticProfile(
                sample_id=Path(file_path).stem,
                variants=found_variants,
                total_snps_processed=total_lines
            )
            
            print(f"✅ Total SNPs processed: {total_lines:,}")
            print(f"✅ Key variants found: {len(found_variants)}/{len(self.variant_db)}")
            print(f"✅ Coverage: {len(found_variants)/len(self.variant_db)*100:.1f}%")
            
            return profile
            
        except FileNotFoundError:
            print(f"❌ Error: Could not find file: {file_path}")
            return GeneticProfile(sample_id="unknown", variants={})
        except Exception as e:
            print(f"❌ Error: {e}")
            return GeneticProfile(sample_id="unknown", variants={})