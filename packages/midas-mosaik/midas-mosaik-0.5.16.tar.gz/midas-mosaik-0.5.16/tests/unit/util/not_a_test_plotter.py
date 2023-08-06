import matplotlib
import matplotlib.pyplot as plt
import pandapower as pp
import simbench as sb

from midas.util.plotter import Plotter, SIMBENCH_CFG


class TestPlotter:
    def __init__(self):
        pass

    def test_simple_plot(self):
        plot = Plotter()
        plot.cfg = SIMBENCH_CFG
        plot.grid = sb.get_simbench_net("1-MV-rural--0-sw")
        pp.runpp(plot.grid)
        plot.simple_plot()

        plt.show()


def main():
    tpl = TestPlotter()
    tpl.test_simple_plot()


if __name__ == "__main__":
    main()
