import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma
from prove_bound import get_m

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.style.use('seaborn')
NUM_COLORS = 30

cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
plt.subplots_adjust(left=0.08, right=0.97, top=0.98, bottom=0.08)
ax = fig.add_subplot(111)
ax.set_prop_cycle(color=[cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])

dm2k_list = range(1, 31)
rev_eta_list = range(1, 51)
eta_list = [1 / rev_eta for rev_eta in rev_eta_list]
tau, beta = 0.6, 0.99

def bin_on_mu(dm2k, mu, eta):
    # print(mu, eta)
    return gamma(dm2k / eta).cdf(get_m(dm2k, eta, tau, mu, beta))

for dm2k in dm2k_list:
    mu_list = []
    for eta in eta_list:
        # print(eta)
        mu_l, mu_r = 0, 1
        while mu_r - mu_l > 1e-6:
            mu_m = (mu_r + mu_l) / 2 
            p_m = bin_on_mu(dm2k, mu_m, eta)
            if p_m > 0.5 / 0.999:
                mu_l = mu_m
            else:
                mu_r = mu_m
        mu_list.append(mu_l)
    x = np.arange(1, 51)
    ax.plot(x, mu_list, label=dm2k)
ax.set_xlabel('$\eta$')
ax.set_ylabel('$\mu$')
_x_label = [f'1/{eta}' for eta in [10, 20, 30, 40, 50]]
ax.set_xticks([10, 20, 30, 40, 50])
ax.set_xticklabels(_x_label)
ax.legend(loc='lower right', ncol=3, title='d-2k')
plt.savefig('tight_const.pdf')
# plt.show()