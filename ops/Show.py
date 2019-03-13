import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def general_plot(indicate_path,xlabel,ylabel,title,xdata,ydata):
    plt.cla()
    plt.clf()
    plt.plot(xdata,ydata,'r-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(indicate_path)
def draw_bar(labels,quants,indicate_path,xlabel,ylabel,title):
    width=0.35
    plt.figure(figsize=(8,(width+0.1)*len(quants)), dpi=300)
    # Bar Plot
    plt.cla()
    plt.clf()
    plt.barh(range(len(quants)),quants,tick_label=labels)
    plt.grid(True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(indicate_path)
    plt.close()