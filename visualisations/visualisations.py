import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from constants import PortfolioFilter

def plot_allocations(group_filter: PortfolioFilter, group_data):
    
    fig = plt.figure(figsize=(10,6))
    groups = list(map(lambda x: x[0], group_data))
    group_pct = np.array(list(map(lambda x: x[1], group_data)))
    pal = sns.color_palette("Greens_d", len(groups))
    rank = group_pct.argsort().argsort()
    g = sns.barplot(x=groups, y=group_pct, palette=np.array(pal)[rank])
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.ylabel('Weight Percent')
    plt.title('Portfolio allocations by %s' % group_filter.value)
    plt.show()