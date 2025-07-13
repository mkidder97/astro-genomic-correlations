# Advanced Astrological-Genetic Correlation Framework

## Project Overview
Sophisticated scientific framework for testing correlations between precise astronomical data and genetic variants using advanced astrological and genomic methodologies.

**Goal**: Achieve 80-90% accuracy using quantitative approaches vs current 30-60% with crude counting methods.

## Core Methodologies

### 1. Polygenic Risk Score Correlation
- Correlates quantitative genetic risk scores with precise planetary mathematical relationships
- Uses planetary aspect strength, dignity points, harmonic resonance
- Expected accuracy: High

### 2. Biological Pathway Analysis
- Groups genetic variants by biological pathways
- Correlates with traditional planetary rulerships
- Expected accuracy: Very High

### 3. Traditional Dignity Analysis
- Classical astrological strength calculations
- Correlated with genetic variant effect sizes
- Expected accuracy: Very High

### 4. Harmonic Resonance Analysis
- Mathematical harmonic patterns between planetary positions
- Quantitative genetic trait correlations
- Expected accuracy: Moderate to High

### 5. Aspect Configuration Analysis
- Complex planetary aspect patterns (Grand Trines, T-Squares)
- Genetic trait cluster correlations
- Expected accuracy: High

## Project Structure
```
src/
├── astrological/          # Astrological calculation modules
├── genetic/               # Genetic analysis modules  
├── correlation/           # Correlation methodologies
├── statistical/           # Statistical validation
├── integration/           # Integrated analysis framework
data/
├── astrological/          # Birth chart data
├── genetic/               # Genetic variant data
tests/
├── unit/                  # Unit tests
├── integration/           # Integration tests
docs/                      # Documentation
scripts/                   # Analysis scripts
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.integration.comprehensive_analysis import ComprehensiveAnalyzer

analyzer = ComprehensiveAnalyzer()
results = analyzer.analyze(birth_chart, genetic_variants)
```

## Statistical Validation
All methods include:
- Pearson/Spearman correlation coefficients
- Bootstrap confidence intervals (n=10,000)
- Permutation testing for significance
- Multiple testing correction
- Cross-validation with train/test splits

## License
MIT License