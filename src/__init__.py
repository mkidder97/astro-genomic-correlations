"""Advanced Astrological-Genetic Correlation Framework"""

__version__ = "0.1.0"
__author__ = "Advanced Astro-Genomic Research"
__description__ = "Sophisticated scientific framework for testing correlations between astronomical data and genetic variants"

from .integration.comprehensive_analysis import ComprehensiveAnalyzer
from .astrological.chart_calculator import ChartCalculator
from .genetic.variant_analyzer import VariantAnalyzer

__all__ = [
    "ComprehensiveAnalyzer",
    "ChartCalculator", 
    "VariantAnalyzer"
]