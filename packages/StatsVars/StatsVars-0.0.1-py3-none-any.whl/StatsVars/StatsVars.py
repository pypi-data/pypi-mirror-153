#Common Stats Vars
from random import choice
from scipy.stats import norm
from scipy.stats import t
from scipy import special as sc
import math 
def parse_kwargs(keys, **kwargs):
    return {key: kwargs[key] for key in keys if key in kwargs}.values()

def sign(x):
    if x >= 0:
        return '+'
    else:
        return '-'

def count(vals):
    return len(vals)

def two_sample_degrees_of_freedom(s1 = [], s2 = [], **kwargs):
    '''kwargs:
        sd1: standard deviation of sample 1
        sd2: standard deviation of sample 2
        n1: # of values of sample 1
        n2: # of values of sample 2
    '''
    if not s1 and not s2:
        keys = ['sd1', 'sd2', 'n1', 'n2']
        sd1, sd2, n1, n2 = parse_kwargs(keys, **kwargs)
    else:
        sd1, sd2 = sample_standard_deviation(s1), sample_standard_deviation(s2)
        n1, n2 = count(s1), count(s2)
    p1 = (sd1**2)/n1
    p2 = (sd2**2)/n2

    num = (p1 + p2)**2
    den1 = (1/(n1 - 1)) * (p1**2)
    den2 = (1/(n2 - 1)) * (p2**2)
    
    return num/(den1 + den2)

def mean (vals):
    n = len(vals)
    return sum(vals)/n

def summation(vals):
    return sum(vals)

def differences(val1, val2):
    if type(val1) != list:
        val1 = [val1 for _ in range(count(val2))]
    
    elif type(val2) != list:
        val2 = [val2 for _ in range(count(val1))]
        
    return [num1 - num2 for num1, num2 in zip(val1, val2)]

def sum_squared_differences(val1, val2):
    if type(val1) != list:
        val1 = [val1 for _ in range(count(val2))]
    
    elif type(val2) != list:
        val2 = [val2 for _ in range(count(val1))]
    
    return sum([(num1 - num2)**2 for num1, num2 in zip(val1, val2)])

def min_max(vals):
    return min(vals), max(vals)


def pop_standard_deviation(vals):
    n = len(vals)
    mu = mean(vals)
    
    running_total = 0
    for num in vals:
        running_total += (num - mu)**2
    
    s = (running_total/n)**(1/2)
    return s

def sample_standard_deviation(vals):
    n = len(vals)
    mu = mean(vals)
    
    running_total = 0
    for num in vals:
        running_total += (num - mu)**2
    
    sd = (running_total/(n-1))**(1/2)
    return sd

def residual_standard_deviation(x_vals, y_vals, eq):
    total = 0
    for x, y in zip(x_vals, y_vals):
        y_hat = eval(eq)
        total += (y - y_hat)**2
    return (total/(count(x_vals) - 2))**(1/2)

def two_sample_z_standard_deviation(p1, n1, p2, n2):
    first = (p1*(1 - p1))/n1
    second = (p2*(1 - p2))/n2
    return math.sqrt(first + second)


def standard_error(vals = [], **kwargs):
    '''
    kwargs:
        -sd: standard deviation
        -n: # of values
    '''
    if not vals:
        keys = ['sd', 'n']
        sd, n = parse_kwargs(keys, **kwargs)
        return sd/n**(1/2)
    else: 
        n = len(vals)
        return sample_standard_deviation(vals)/n**(1/2)

def two_sample_error(s1 = [], s2 = [], **kwargs): #for t models
    '''kwargs:
        sd1: standard deviation for first sample
        sd2: standard deviation for second sample
        n1: # of values for first sample
        n2: # of values for second sample
    '''
    if not s1 and not s2:
        keys = ['sd1', 'sd2', 'n1', 'n2']
        sd1, sd2, n1, n2 = parse_kwargs(keys, **kwargs)
    else:
        sd1, sd2 = sample_standard_deviation(s1), sample_standard_deviation(s2)
        n1, n2 = count(s1), count(s2)
    return ((sd1**2/n1) + (sd2**2/n2))**(1/2)

def slope_standard_error(res_sd, x_values):
    n = count(x_values)
    sd_x = sample_standard_deviation(x_values)
    
    return res_sd/((n - 1)**(1/2) * sd_x)

def intercept_standard_error(MSE, x_values):
    n = count(x_values)
    x_mean = mean(x_values)
    second = (x_mean**2)/sum_squared_differences(x_values, x_mean)
    return math.sqrt(MSE * (1/n + second))

def mean_squared_error(expected, predicted):
    return (1/count(expected)) * sum_squared_differences(expected, predicted)


def prediction_interval_error(crit_score, slope_error, x, x_mean, residual_sd, n):
    return crit_score * math.sqrt((slope_error**2)*((x - x_mean)**2)+((residual_sd**2)/n)+(residual_sd**2))


def z_score(vals, score, expected_mean):
    return (score - expected_mean)/mean(vals)


def X_score(vals, expected):
    if not isinstance(expected, list):
        expectations = [expected for _ in range(len(vals))]
    else:
        expectations = expected
    total = sum([(obs - expected)**2/expected for obs, expected in zip(vals, expectations)])
    return total


def t_score(vals = [], expected_mean = 0, **kwargs):
    '''
    kwargs
        -mu: data mean
        -sd: data standard deviation
        -n: # of values
    '''
    if not vals:
        keys = ['mu', 'sd', 'n']
        mu, sd, n = parse_kwargs(keys, **kwargs)
        
        numerator = mu - expected_mean
        denominator = standard_error(sd=sd, n=n)
    else:
        numerator = mean(vals) - expected_mean
        denominator = standard_error(vals)
    return numerator/denominator

def two_sample_t_score(s1 = [], s2 = [], **kwargs):
    '''kwargs:
        x1 = mean of sample 1
        x2 = mean of sample 2
        sd1 = standard deviation of sample 1
        sd2 = standard deviation of sample 2
        n1 = # of values of sample 1
        n2 = # of values of sample 2
    '''
    if not s1 and not s2:
        keys = ['x1', 'x2', 'sd1', 'sd2', 'n1', 'n2']
        x1, x2, sd1, sd2, n1, n2 = parse_kwargs(keys, **kwargs)
    else:
        x1, x2 = mean(s1), mean(s2)
        sd1, sd2 = sample_standard_deviation(s1), sample_standard_deviation(s2)
        n1, n2 = count(s1), count(s2)
    return (x1 - x2)/two_sample_error(sd1=sd1, sd2=sd2, n1=n1, n2=n2)

def pairwise_t_score(val1 = [], val2 = [], expected_difference = 0, **kwargs):
    '''
    kwargs:
        -mu: mean of differences
        -sd: standard deviation of differences
        -n: # of pairs of differences
    '''
    if not val1 and not val2:
        keys = ['mu', 'sd', 'n']
        mu, sd, n = parse_kwargs(keys, **kwargs)        
    else:
        pairs = differences(val1=val1, val2=val2)
        mu, sd, n = get_vars(pairs, ['mu', 'sd', 'n']).values()

    SE = standard_error(sd=sd, n=n)
    t = (mu - expected_difference)/SE
    return t

def regression_t_score(b, B, SE):
    return (b - B)/SE


def invNorm(z, mu = 0, sd = 1):
    z += (1-z)/2

    return norm.ppf(z, loc = mu, scale = sd)

def invT(confidence, df, mu = 0, sd = 1):
    confidence += (1-confidence)/2
    return t.ppf(confidence, df, loc = mu, scale = sd)


def Normalcdf(z, mu = 0, sd = 1):
    return norm.cdf(z, loc = mu, scale = sd)

def Tcdf(q, df):
    return t._cdf(q, df)

def Xcdf(x, df):
    return upper_regularized_gamma(df/2, x/2)


def complete_gamma(n):
    return sc.gamma(n)

def lower_regularized_gamma(a, x):
    return sc.gammainc(a, x)

def upper_regularized_gamma(a, x):
    return sc.gammaincc(a, x)

def X_crit_value(df, alpha=0.5):
    return sc.chdtri(df, alpha)

def X_expected(categories_true, categories_false, rounding=4):
    n = count(categories_true)
    total_true = sum(categories_true)
    total_false = sum(categories_false)
    total_all = total_true + total_false
    true_prop = total_true/total_all
    
    expected_true = []
    expected_false = []
    for i in range(n):
        category_total = categories_true[i] + categories_false[i]
        category_true_prop = category_total*true_prop
        expected_true.append(round(category_true_prop, rounding))
        expected_false.append(round(category_total - category_true_prop, rounding))
    return expected_true, expected_false

def interval_notation(v1, v2, rounding = -1):
    if round == -1:
        return f'({v1}, {v2})'
    return f'({round(v1, rounding)}, {round(v2, rounding)})'

def random_sample(lst, amount):
    return [choice(lst) for _ in range (amount)]

def estimate_t_sample_size(margin_of_error, sd, confidence = .95, cutoff = 60):
    score = invNorm(confidence)
    sqrroot_n = (score * sd)/margin_of_error
    n = sqrroot_n ** 2
    if n < cutoff:
        df = n - 1
        t_val = invT(confidence, df)
        sqrroot_n = (t_val * sd)/margin_of_error
        n = sqrroot_n ** 2
    return n

def complete_summary(vals, formatted = False):
    n = count(vals)
    mu = mean(vals)
    sigma = sample_standard_deviation(vals)
    small, large = min_max(vals)
    SE = standard_error(vals)

    if formatted:
        print(f'''
            n = {n}
            mu (x bar) = {mu}
            sd (sigma) = {sigma}
            min = {small}
            max = {large}
            error = {SE}
            ''')
    else:
        return {
            'n' : n,
            'mu' : mu,
            'sigma' : sigma,
            'min' : small,
            'max' : large,
            'standard error' : SE
        }

def get_vars(vals, keys):
    parsed_keys = [key.strip().lower() for key in keys]
    funcs = {
        'n': count, 
        'mu': mean,
        'sd': sample_standard_deviation, 
        'min max': min_max,
        'se': standard_error,
        '2se': two_sample_error,
        'df': count,
        '2df': two_sample_degrees_of_freedom
        }
    
    summary = {}
    for name in parsed_keys:
        func = funcs[name]
        summary[name] = func(vals)
    return summary

def linreg_intercept(x_vals, y_vals):
    #(sumy * sumx^2) - (sumx * sumxy)
    #--------------------------------
    #       n*sumx^2 - (sumx)^2
    sum_y = sum(y_vals)
    sum_x = sum(x_vals)
    
    sum_x2 = sum([x**2 for x in x_vals])
    sum_xy = sum([x * y for x, y in zip(x_vals, y_vals)])
    
    n = count(x_vals)

    b = ((sum_y * sum_x2) - (sum_x * sum_xy))/(n *sum_x2 - (sum_x)**2)
    return b

def linreg_slope(x_vals, y_vals):
    #(n * sumxy) - (sumx * sumy)
    #--------------------------------
    #       n*sumx^2 - (sumx)^2
    sum_y = sum(y_vals)
    sum_x = sum(x_vals)
    
    sum_x2 = sum([x**2 for x in x_vals])
    sum_xy = sum([x * y for x, y in zip(x_vals, y_vals)])
    
    n = count(x_vals)
    
    a = ((n * sum_xy) - (sum_x * sum_y))/(n *sum_x2 - (sum_x)**2)
    return a

def residuals(x_vals, y_vals, eq):
    lst = []
    for x, y in zip(x_vals, y_vals):
        y_approx = eval(eq)
        res = y - y_approx
        lst.append(res)
    return lst

def get_cords(x_vals, line):
    y_vals = []
    for x in x_vals:
        y_vals.append(eval(line))
    return y_vals

def correlation_coefficient(x_vals, y_vals):
    sum_y = sum(y_vals)
    sum_x = sum(x_vals)
    
    sum_x2 = sum([x**2 for x in x_vals])
    sum_xy = sum([x * y for x, y in zip(x_vals, y_vals)])
    sum_y2 = sum([y**2 for y in y_vals])
    
    n = count(x_vals)
    
    num = (n*sum_xy) - (sum_x * sum_y)
    den = math.sqrt(((n*sum_x2) - (sum_x**2)) * ((n*sum_y2) - (sum_y**2)))
    return num/den

if __name__ == '__main__':
    def parse_nums(raw_values):
        str_values_list = raw_values.strip().split('\n')
        values = [float(i) for i in str_values_list]
        return values

    true = [325, 225, 150]
    false = [125, 100, 75]
    print(X_expected(true, false))    
