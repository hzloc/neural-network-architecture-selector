import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks", rc={"axes.spines.right": False, "axes.spines.top": False})


def plot(historical, prediction, actual, ylabel="Radiation"):
    x = np.arange(len(historical) + 1)
    print(prediction, actual)
    historical = np.append(historical, actual)

    print(len(x), len(historical), print(x[-1]))
    plt.plot(x, historical, linestyle="--", label="hist")
    plt.scatter(x[-1], prediction, color="green", marker="*", label="pred")
    plt.scatter(x[-1], actual, marker="o", label="act")
    axs = plt.gca()
    axs.yaxis.get_ticklocs(minor=True)
    axs.minorticks_on()

    #     axs.tick_params(axis='x', which='minor', bottom=False)
    plt.legend()
    plt.title("Prediction of the radiation")
    plt.ylabel(ylabel)
    plt.xlabel("Time steps")
    plt.show()


def plot_pred_vs_act(preds, actuals, ylabel="Radiation"):
    x = np.arange(len(preds))
    fig = plt.figure()
    plt.plot(x, preds, "*g-", label="pred")
    plt.plot(x, actuals, "xr-", label="act")
    plt.legend()
    plt.title("Prediction vs Actuals")
    plt.ylabel(ylabel)
    plt.xlabel("Time steps")
    plt.show()
