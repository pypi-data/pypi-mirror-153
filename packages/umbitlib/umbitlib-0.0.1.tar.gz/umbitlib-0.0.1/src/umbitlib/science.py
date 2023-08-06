
# %%
import numpy as np
import matplotlib.pyplot as plt   
import seaborn as sns
from scipy import stats  
import pylab


def p_pass_fail(p1, p2=.05) -> str:
    """Checks if a p value is > than chosen p-value and return pass/fail string

    Args:
        p1 (float): calculated p-value input to compare to chosen p-value
        p2 (float, optional): chosen p-value or significance level. Defaults to .05.

    Returns:
        (string): either '[PASSED]' or '[FAILED]' based on result
    """
    for var in [p1, p2]:        
        if not (isinstance(var, int) or isinstance(var, float) or isinstance(var, complex)):
            raise TypeError('Please make sure all inputs are numerical')
    
    result = "[PASSED] " if p1 > p2 else "[FAILED] "        
    return result


def z_pass_fail(z1, z2=1.96) -> str:
    """Checks if a z-score/test statistic is > than chosen z-score/test statistic and return pass/fail string

    Args:
        p1 (float): calculated z-score/test statistic input to compare to chosen z-score/test statistic
        p2 (float, optional): chosen z-score/test statistic or significance level. Defaults to .05.

    Returns:
        (string): either '[PASSED]' or '[FAILED]' based on result
    """
    for var in [z1, z2]:        
        if not (isinstance(var, int) or isinstance(var, float) or isinstance(var, complex)):
            raise TypeError('Please make sure all inputs are numerical')
        
    result = "[PASSED] " if (z1 < z2) and (z1 > -z2) else "[FAILED] "        
    return result
        


def run_normality_tests(series=np.random.normal(size=150), pvalue=.05, zscore=1.96):   
    """Runs multiple normality tests on a numerical pandas dataframe column (list, series or vector) 
       series must be numerical and not contain missing values i.e. na, n/a, None, Null, NaN, string type, etc.
       runs best in .ipynb files or python code chunks (#%%) in a .py file
       to test failure output use run_normality_tests(np.random.randint(1000, size=5000))
       to test success output run without inputs run_normality_tests()

    Args:
        series (_type_, optional): the collection of values to test can be a column, list, series, vector. Defaults to a random normal distribution.
        pvalue (float, optional): the p-value or level of significance to test against. Defaults to .05.
        zscore (float, optional): the z-score or test statistic to test against. Defaults to 1.96.
        
    Returns:
        multiple strings and graphs with test results
    """

    # Skewness check
    skewness_result = stats.skewtest(series)
    print(f"{p_pass_fail(skewness_result.pvalue, pvalue)}Skewness p-value: {skewness_result.pvalue:.3f} (Should be > {pvalue} to pass)")
    print(f"{z_pass_fail(skewness_result.statistic, zscore)}Skewness Z-Score: {skewness_result.statistic:.3f} (Should be between +/- {zscore} to pass)\n")


    # Kurtosis check 
    kurtosis_result = stats.kurtosistest(series)
    print(f"{p_pass_fail(kurtosis_result.pvalue, pvalue)}Kurtosis p-value: {kurtosis_result.pvalue:.3f} (Should be > {pvalue} to pass)")
    print(f"{z_pass_fail(kurtosis_result.statistic, zscore)}Kurtosis Z-Score: {kurtosis_result.statistic:.3f} (Should be between +/- {zscore} to pass)\n")


    # Shapiro-Wilks Normality Test
    shapiro_result = stats.shapiro(series)
    print(f"{p_pass_fail(shapiro_result.pvalue, pvalue)}Shapiro p-value: {shapiro_result.pvalue:.3f} (Should be > {pvalue} to pass)")
    print(f"{z_pass_fail(shapiro_result.statistic, zscore)}Shapiro test statistic: {shapiro_result.statistic:.3f} \n")    


    # Kolmogorov–Smirnov Normality Test
    smirnov_result = stats.kstest(series, 'norm', N=100)
    print(f"{p_pass_fail(smirnov_result.pvalue, pvalue)}Smirnov p-value: {smirnov_result.pvalue:.3f} (Should be > {pvalue} to pass)")
    print(f"{z_pass_fail(smirnov_result.statistic, zscore)}Smirnov test statistic: {smirnov_result.statistic:.3f} \n")


    # (START) Anderson-Darling Normality Test https://www.statology.org/anderson-darling-test-python/
    ## If the statistic is < all of the critical values then the results are not significant enough to reject the null hypothesis that this data is normally distributed
    ## If the statistic is > one of the critical values we have sufficient evidence to reject the null hypothesis (fails normality test)

    anderson_result = stats.anderson(series, dist='norm')
    a = anderson_result.statistic
    b = anderson_result.critical_values
    c = anderson_result.significance_level    

    if a > b[4]:
        print(f"[FAILED] ANDERSON INTERPRETATION: We are {100-c[4]}% certain the data is NOT normally distributed.\n")
    elif a > b[3]:
        print(f"[FAILED] ANDERSON INTERPRETATION: We are {100-c[3]}% certain the data is NOT normally distributed.\n")
    elif a > b[2]:
        print(f"[FAILED] ANDERSON INTERPRETATION: We are {100-c[2]}% certain the data is NOT normally distributed.\n")
    elif a > b[1]:
        print(f"[FAILED] ANDERSON INTERPRETATION: We are {100-c[1]}% certain the data is NOT normally distributed.\n")
    elif a > b[0]:
        print(f"[FAILED] ANDERSON INTERPRETATION: We are {100-c[0]}% certain the data is NOT normally distributed.\n")
    elif (a <= b[0]) & (a <= b[1]) & (a <= b[2]) & (a <= b[3]) & (a <= b[4]):
         print("\n[PASSED] ANDERSON INTERPRETATION: This data is likely normally distributed\n(results are not significant enough to rule out a normal distribution).\n")
    elif np.isnan(a):
        print('[ERROR] There is an issue with the dataset.')
    else:
        print('[ERROR] Anderson Interpretation could not be automatically derived for this dataset.')
    
    print(f"Anderson statistic: {a:.3f}")
    print(f"Anderson critical values: {b}")
    print(f"Anderson signifance levels: {c}")
    # (END) Anderson-Darling Normality Test
    
    
    # Q-Q Plot
    try:
        stats.probplot(series, dist='norm', plot=pylab)
        print("Q-Q (Quantile Quantile) Plot:  (points should follow a straight line)")
        pylab.show()
    except Exception as e:
        print(e)
    
    
    # Distribution Plot
    try:        
        print("Distribution Plot: (The Curve should be Bell Shaped)")
        sns.histplot(series, kde=True, stat="density", linewidth=0)
        plt.show()
    except Exception as e:
        print(str(e) + ' (You might have tried to log() a negative number)')