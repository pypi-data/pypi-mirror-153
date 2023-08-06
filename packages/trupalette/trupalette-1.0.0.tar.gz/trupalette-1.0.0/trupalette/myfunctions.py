def palette1():
    import matplotlib as mpl
    from cycler import cycler
    mpl.rcParams['axes.prop_cycle'] = cycler(color=['#003e51', '#00b0b9', '#bad1ba', '#9ab7c1', '#ffcd00', '#fff5de', '#00b18f'])
def palette2():
    import matplotlib as mpl
    from cycler import cycler
    mpl.rcParams['axes.prop_cycle'] = cycler(color=['#f88f23', '#007B81', '#ffcd00', '#9EE1E5','#00b0b9', '#FFEFA9', '#E0F6F7', '#ddd', '#d5e1e5', '#003e51', '#f3f3f3', '#e9e9e9'])
def palette_reset():
    import matplotlib as mpl
    from cycler import cycler
    mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')