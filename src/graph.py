def build_graph(f, name, angles, y_axis):
    """
    Build a matplotlib graph of angle on x axis and drag/lift on y axis will
    sort them to correspond to eachother and write it to the file handle `f`.
    """
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.ioff()
    plt.plot(angles, y_axis, label='Mean {}'.format(name))
    plt.xlabel('Angle')
    plt.title('Results produced by the airfoil application')
    plt.grid(True)

    plt.legend(fancybox=True, shadow=True)
    plt.savefig(f, format='png')
    plt.close()


if __name__ == '__main__':
    """Example on slightly unsorted list."""

    angle = [21, 20, 22, 23, 24, 25, 26, 27, 28, 29]
    lift = [24.50, 22.13, 25.80, 26.62, 27.82, 28.28,
            28.22, 29.97, 30.37, 31.45]
    drag = [246.29, 242.49, 244.64, 244.64, 244.34,
            243.59, 244.14, 243.96, 243.46, 243.90]

    from StringIO import StringIO
    f1, f2 = StringIO(), StringIO()
    graph1 = build_graph(f1, 'Lift', angle, lift)
    graph2 = build_graph(f2, 'Drag', angle, drag)

    assert f1
    assert f2
