#!/usr/bin/env python3
"""Development environment setup script"""

import os
import sys
from pathlib import Path

def create_directory_structure():
    """Create complete directory structure"""
    directories = [
        "data/astrological",
        "data/genetic", 
        "data/results",
        "tests/unit",
        "tests/integration",
        "docs/methodology",
        "docs/api",
        "scripts/analysis",
        "scripts/validation",
        "examples",
        "notebooks"
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")

def create_data_templates():
    """Create template data files"""
    print("\n📄 Creating data templates...")
    
    # Genetic data template
    genetic_template = '''# Genetic Data Template (23andMe format)
# rsid\tchromosome\tposition\tgenotype
rs4680\t22\t19963748\tAA
rs1815739\t11\t66560624\tCC
rs429358\t19\t44908822\tCT
rs7412\t19\t44908684\tCC
rs1801133\t1\t11796321\tTT
rs662\t7\t94943158\tAA
'''
    
    with open("data/genetic/template_genetic_data.txt", "w") as f:
        f.write(genetic_template)
    print("   ✅ data/genetic/template_genetic_data.txt")
    
    # Birth data template
    birth_template = '''# Birth Data Template
# Format: YYYY-MM-DD HH:MM (UTC), Latitude, Longitude, Location
1990-06-15 14:30, 40.7128, -74.0060, New York City
1985-12-03 08:15, 51.5074, -0.1278, London
1992-09-22 20:45, 34.0522, -118.2437, Los Angeles
'''
    
    with open("data/astrological/template_birth_data.txt", "w") as f:
        f.write(birth_template)
    print("   ✅ data/astrological/template_birth_data.txt")

def create_documentation_stubs():
    """Create documentation stubs"""
    print("\n📚 Creating documentation stubs...")
    
    # Methodology documentation
    methodology_doc = '''# Methodology Documentation

## Traditional Dignity Analysis
- Classical astrological strength calculations
- Correlation with genetic variant effect sizes
- Expected accuracy: Very High

## Biological Pathway Analysis
- Groups genetic variants by biological pathways
- Correlates with traditional planetary rulerships
- Expected accuracy: Very High

## Polygenic Risk Score Correlation
- Quantitative genetic risk scores
- Precise planetary mathematical relationships
- Expected accuracy: High

## Statistical Validation
- Bootstrap confidence intervals
- Permutation testing
- Multiple testing correction
'''
    
    with open("docs/methodology/overview.md", "w") as f:
        f.write(methodology_doc)
    print("   ✅ docs/methodology/overview.md")
    
    # API documentation
    api_doc = '''# API Documentation

## ComprehensiveAnalyzer
Main analysis class implementing integrated methodology.

### Usage
```python
from src.integration.comprehensive_analysis import ComprehensiveAnalyzer

analyzer = ComprehensiveAnalyzer()
results = analyzer.comprehensive_astro_genetic_analysis(
    birth_datetime=datetime(1990, 6, 15, 14, 30),
    latitude=40.7128,
    longitude=-74.0060,
    genetic_file_path="data/genetic/sample_data.txt"
)
```

## ChartCalculator
High-precision astrological chart calculations.

## VariantAnalyzer
Genetic variant processing and analysis.
'''
    
    with open("docs/api/reference.md", "w") as f:
        f.write(api_doc)
    print("   ✅ docs/api/reference.md")

def create_analysis_scripts():
    """Create analysis script templates"""
    print("\n🔬 Creating analysis scripts...")
    
    # Batch analysis script
    batch_script = '''#!/usr/bin/env python3
"""Batch analysis script for multiple subjects"""

import sys
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from integration.comprehensive_analysis import ComprehensiveAnalyzer

def run_batch_analysis(data_file):
    """Run analysis on multiple subjects"""
    print(f"Running batch analysis on {data_file}")
    
    # Load subject data
    df = pd.read_csv(data_file)
    
    analyzer = ComprehensiveAnalyzer()
    results = []
    
    for _, row in df.iterrows():
        try:
            result = analyzer.comprehensive_astro_genetic_analysis(
                birth_datetime=datetime.fromisoformat(row['birth_datetime']),
                latitude=row['latitude'],
                longitude=row['longitude'],
                genetic_file_path=row['genetic_file']
            )
            results.append({
                'subject_id': row['subject_id'],
                'correlation': result.overall_correlation,
                'confidence': result.confidence_level
            })
        except Exception as e:
            print(f"Error processing {row['subject_id']}: {e}")
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('data/results/batch_results.csv', index=False)
    print(f"Results saved to data/results/batch_results.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/analysis/batch_analysis.py <data_file>")
        sys.exit(1)
    
    run_batch_analysis(sys.argv[1])
'''
    
    with open("scripts/analysis/batch_analysis.py", "w") as f:
        f.write(batch_script)
    print("   ✅ scripts/analysis/batch_analysis.py")
    
    # Validation script
    validation_script = '''#!/usr/bin/env python3
"""Statistical validation script"""

import sys
import os
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from statistical.validation import StatisticalValidator

def run_validation_tests():
    """Run comprehensive validation tests"""
    print("Running statistical validation tests...")
    
    validator = StatisticalValidator()
    
    # Test data
    test_correlations = {
        'strong_positive': ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),
        'moderate_negative': ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        'weak_correlation': ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5])
    }
    
    results = validator.comprehensive_validation(test_correlations)
    
    for name, test_results in results.items():
        print(f"\n{name}:")
        for result in test_results:
            print(f"  {result.test_name}: {result.statistic:.3f} (p={result.p_value:.4f})")

if __name__ == "__main__":
    run_validation_tests()
'''
    
    with open("scripts/validation/statistical_tests.py", "w") as f:
        f.write(validation_script)
    print("   ✅ scripts/validation/statistical_tests.py")

def create_example_notebooks():
    """Create example Jupyter notebooks"""
    print("\n📓 Creating example notebooks...")
    
    # Example notebook structure
    notebook_content = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Advanced Astro-Genomic Correlation Analysis\n",
    "\n",
    "This notebook demonstrates the sophisticated methodologies for testing correlations between astrological factors and genetic variants.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "sys.path.append('../src')\n",
    "\n",
    "from integration.comprehensive_analysis import ComprehensiveAnalyzer\n",
    "from datetime import datetime\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
'''
    
    with open("notebooks/example_analysis.ipynb", "w") as f:
        f.write(notebook_content)
    print("   ✅ notebooks/example_analysis.ipynb")

def make_scripts_executable():
    """Make scripts executable"""
    print("\n⚡ Making scripts executable...")
    
    scripts = [
        "demo/demo_analysis.py",
        "tests/test_basic_functionality.py",
        "scripts/analysis/batch_analysis.py",
        "scripts/validation/statistical_tests.py"
    ]
    
    for script in scripts:
        if Path(script).exists():
            os.chmod(script, 0o755)
            print(f"   ✅ {script}")

def main():
    """Main setup function"""
    print("🚀 Setting up Advanced Astro-Genomic Development Environment")
    print("=" * 60)
    
    create_directory_structure()
    create_data_templates()
    create_documentation_stubs()
    create_analysis_scripts()
    create_example_notebooks()
    make_scripts_executable()
    
    print("\n✨ Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up Swiss Ephemeris data files")
    print("3. Add your genetic data to data/genetic/")
    print("4. Run demo: python demo/demo_analysis.py")
    print("5. Run tests: python tests/test_basic_functionality.py")
    print("\n🔬 Framework ready for advanced astro-genomic research!")

if __name__ == "__main__":
    main()