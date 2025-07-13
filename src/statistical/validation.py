"""Statistical validation and testing framework"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Statistical validation results"""
    test_name: str
    statistic: float
    p_value: float
    confidence_interval: Tuple[float, float]
    interpretation: str
    passed: bool

class StatisticalValidator:
    """Comprehensive statistical validation framework"""
    
    def __init__(self, alpha: float = 0.05):
        """Initialize validator with significance level"""
        self.alpha = alpha
    
    def validate_correlation(self, x: List[float], y: List[float], 
                           method: str = 'pearson') -> ValidationResult:
        """Validate correlation with statistical testing
        
        Args:
            x: First variable values
            y: Second variable values  
            method: Correlation method ('pearson', 'spearman')
            
        Returns:
            Validation results
        """
        if len(x) != len(y) or len(x) < 3:
            raise ValueError("Invalid data for correlation analysis")
        
        # Calculate correlation
        if method == 'pearson':
            corr, p_value = stats.pearsonr(x, y)
            test_name = "Pearson Correlation"
        elif method == 'spearman':
            corr, p_value = stats.spearmanr(x, y)
            test_name = "Spearman Correlation"
        else:
            raise ValueError(f"Unknown correlation method: {method}")
        
        # Calculate confidence interval
        n = len(x)
        if n > 3:
            # Fisher z-transformation for confidence interval
            z = np.arctanh(corr)
            se = 1 / np.sqrt(n - 3)
            z_crit = stats.norm.ppf(1 - self.alpha/2)
            z_lower = z - z_crit * se
            z_upper = z + z_crit * se
            ci_lower = np.tanh(z_lower)
            ci_upper = np.tanh(z_upper)
        else:
            ci_lower, ci_upper = -1.0, 1.0
        
        # Interpretation
        if p_value < self.alpha:
            interpretation = f"Significant correlation detected (p = {p_value:.4f})"
            passed = True
        else:
            interpretation = f"No significant correlation (p = {p_value:.4f})"
            passed = False
        
        return ValidationResult(
            test_name=test_name,
            statistic=corr,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            interpretation=interpretation,
            passed=passed
        )
    
    def bootstrap_validation(self, x: List[float], y: List[float], 
                           n_bootstrap: int = 1000) -> ValidationResult:
        """Bootstrap validation of correlation"""
        n = len(x)
        if n < 3:
            raise ValueError("Insufficient data for bootstrap validation")
        
        # Original correlation
        original_corr, _ = stats.spearmanr(x, y)
        
        # Bootstrap correlations
        bootstrap_corrs = []
        for _ in range(n_bootstrap):
            indices = np.random.choice(n, size=n, replace=True)
            x_boot = [x[i] for i in indices]
            y_boot = [y[i] for i in indices]
            
            try:
                corr, _ = stats.spearmanr(x_boot, y_boot)
                if not np.isnan(corr):
                    bootstrap_corrs.append(corr)
            except:
                continue
        
        if len(bootstrap_corrs) == 0:
            return ValidationResult(
                test_name="Bootstrap Validation",
                statistic=original_corr,
                p_value=1.0,
                confidence_interval=(-1.0, 1.0),
                interpretation="Bootstrap validation failed",
                passed=False
            )
        
        # Calculate confidence interval
        bootstrap_corrs.sort()
        ci_lower = np.percentile(bootstrap_corrs, 2.5)
        ci_upper = np.percentile(bootstrap_corrs, 97.5)
        
        # P-value approximation (proportion of bootstrap samples with correlation near zero)
        p_value = np.mean([abs(corr) <= abs(original_corr) for corr in bootstrap_corrs])
        
        interpretation = f"Bootstrap validation: {len(bootstrap_corrs)} successful resamples"
        passed = ci_lower * ci_upper > 0  # CI doesn't include zero
        
        return ValidationResult(
            test_name="Bootstrap Validation",
            statistic=original_corr,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            interpretation=interpretation,
            passed=passed
        )
    
    def permutation_test(self, x: List[float], y: List[float], 
                        n_permutations: int = 1000) -> ValidationResult:
        """Permutation test for correlation significance"""
        if len(x) != len(y) or len(x) < 3:
            raise ValueError("Invalid data for permutation test")
        
        # Original correlation
        original_corr, _ = stats.spearmanr(x, y)
        
        # Permutation correlations
        perm_corrs = []
        for _ in range(n_permutations):
            y_perm = np.random.permutation(y)
            try:
                corr, _ = stats.spearmanr(x, y_perm)
                if not np.isnan(corr):
                    perm_corrs.append(corr)
            except:
                continue
        
        if len(perm_corrs) == 0:
            return ValidationResult(
                test_name="Permutation Test",
                statistic=original_corr,
                p_value=1.0,
                confidence_interval=(-1.0, 1.0),
                interpretation="Permutation test failed",
                passed=False
            )
        
        # Calculate p-value
        p_value = np.mean([abs(corr) >= abs(original_corr) for corr in perm_corrs])
        
        # Confidence interval from permutation distribution
        perm_corrs.sort()
        ci_lower = np.percentile(perm_corrs, 2.5)
        ci_upper = np.percentile(perm_corrs, 97.5)
        
        interpretation = f"Permutation test: {len(perm_corrs)} permutations completed"
        passed = p_value < self.alpha
        
        return ValidationResult(
            test_name="Permutation Test",
            statistic=original_corr,
            p_value=p_value,
            confidence_interval=(ci_lower, ci_upper),
            interpretation=interpretation,
            passed=passed
        )
    
    def multiple_testing_correction(self, p_values: List[float], 
                                  method: str = 'bonferroni') -> List[float]:
        """Apply multiple testing correction
        
        Args:
            p_values: List of p-values
            method: Correction method ('bonferroni', 'fdr')
            
        Returns:
            Corrected p-values
        """
        p_array = np.array(p_values)
        n = len(p_array)
        
        if method == 'bonferroni':
            return (p_array * n).tolist()
        
        elif method == 'fdr':  # Benjamini-Hochberg
            # Sort p-values
            sorted_indices = np.argsort(p_array)
            sorted_p = p_array[sorted_indices]
            
            # Apply correction
            corrected = np.zeros_like(sorted_p)
            for i in range(n-1, -1, -1):
                if i == n-1:
                    corrected[i] = sorted_p[i]
                else:
                    corrected[i] = min(corrected[i+1], 
                                     sorted_p[i] * n / (i + 1))
            
            # Restore original order
            result = np.zeros_like(p_array)
            result[sorted_indices] = corrected
            return result.tolist()
        
        else:
            raise ValueError(f"Unknown correction method: {method}")
    
    def comprehensive_validation(self, correlations: Dict[str, Tuple[List[float], List[float]]]) -> Dict[str, List[ValidationResult]]:
        """Comprehensive validation of multiple correlations
        
        Args:
            correlations: Dict mapping names to (x, y) data pairs
            
        Returns:
            Dict mapping names to validation results
        """
        all_results = {}
        all_p_values = []
        
        # Run all validation tests
        for name, (x, y) in correlations.items():
            results = []
            
            try:
                # Pearson correlation test
                results.append(self.validate_correlation(x, y, 'pearson'))
                
                # Spearman correlation test  
                results.append(self.validate_correlation(x, y, 'spearman'))
                
                # Bootstrap validation
                if len(x) >= 5:
                    results.append(self.bootstrap_validation(x, y))
                
                # Permutation test
                if len(x) >= 5:
                    results.append(self.permutation_test(x, y))
                
                all_results[name] = results
                
                # Collect p-values for multiple testing correction
                for result in results:
                    all_p_values.append(result.p_value)
                    
            except Exception as e:
                # Handle validation errors gracefully
                error_result = ValidationResult(
                    test_name="Validation Error",
                    statistic=0.0,
                    p_value=1.0,
                    confidence_interval=(-1.0, 1.0),
                    interpretation=f"Validation failed: {str(e)}",
                    passed=False
                )
                all_results[name] = [error_result]
        
        # Apply multiple testing correction
        if len(all_p_values) > 1:
            corrected_p = self.multiple_testing_correction(all_p_values, 'fdr')
            
            # Update results with corrected p-values
            idx = 0
            for name, results in all_results.items():
                for result in results:
                    if result.test_name != "Validation Error":
                        # Create new result with corrected p-value
                        corrected_result = ValidationResult(
                            test_name=f"{result.test_name} (FDR corrected)",
                            statistic=result.statistic,
                            p_value=corrected_p[idx],
                            confidence_interval=result.confidence_interval,
                            interpretation=f"{result.interpretation} [FDR corrected p = {corrected_p[idx]:.4f}]",
                            passed=corrected_p[idx] < self.alpha
                        )
                        results.append(corrected_result)
                        idx += 1
        
        return all_results