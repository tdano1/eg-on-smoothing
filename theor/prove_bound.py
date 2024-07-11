from scipy.stats import gamma
from scipy.special import loggamma as lngamma
import numpy as np
import matplotlib.pyplot as plt

def get_m(dm2k, eta, tau, mu, beta):
    gamma_quo = np.exp(0.5 * (lngamma((dm2k + 2)/ eta) - lngamma(dm2k / eta)))
    ans = (gamma_quo * ((1 - 2 * tau) * mu + 
        np.sqrt(beta + (4 * tau * tau - 4 * tau) * mu * mu))) ** eta
    return ans

def bin_on_mu(dm2k, mu, eta):
    # print(mu, eta)
    return gamma(dm2k / eta).cdf(get_m(dm2k, eta, tau, mu, beta))

dm2k = np.arange(1, 31)
tau = 0.6
mu = 0.02
beta = 0.99
frac = True

with open('print_proof.txt', 'a') as f:
    f.write('\\resizebox{20cm}{!}{')
    f.write('\\begin{tabular}' + '{' + 'c' * 31 + '}\n\t\\toprule\n\t$\\eta\\backslash d-2k$')
    for i in range(30):
        f.write(f' & {i + 1}')
    f.write(' \\\\\n\t\\midrule\n')
    etas = np.arange(1, 11)[::-1]
    for now_eta in etas:
        f.write('\t' + f'{now_eta}')
        flag_for_red = True
        for j in dm2k:
            val = gamma(j / now_eta).cdf(get_m(j, now_eta, tau, mu, beta))
            if val < 1 / 2 / 0.999 and flag_for_red == True:
                f.write(' & \\textcolor{red}{' + f'{val:.3f}' + '}')
                flag_for_red = False
            else:
                f.write(f' & {val:.3f}')
        f.write(' \\\\\n')
    etas = np.arange(2, 51)
    for now_eta in etas:
        if frac:
            f.write('\t' + '$\\frac{1}' + '{' + f'{now_eta}' + '}$')
        else:
            f.write('\t' + '1/' + f'{now_eta}')
        now_eta = 1 / now_eta
        for j in dm2k:
            f.write(f' & {gamma(j / now_eta).cdf(get_m(j, now_eta, tau, mu, beta)):.3f}')
        f.write(' \\\\\n')
    f.write('\t\\bottomrule\n\end{tabular}\n}')