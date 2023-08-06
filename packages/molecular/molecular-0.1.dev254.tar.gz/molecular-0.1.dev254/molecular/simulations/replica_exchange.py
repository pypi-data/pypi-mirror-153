"""
replica_exchange.py

author: C. Lockhart <clockha2@gmu.edu>
language: Python3
"""

from molecular.io import loadtxt

import numpy as np
import pandas as pd


# class MarkovChain ...
# class CoupledMarkovChain


# Class that stores exchange history, i.e., which replicas visited which states over time
class ExchangeHistory:
    """
    Replica-exchange and other coupled Markov chain simulations follow replicas over time as they walk across
    state space. Here, "state" is used generically and can refer to temperature (commonly), Hamiltonian
    scaling factors, etc.

    The purpose of this class is to permit easy evaluation of exchange performance. We can compute (and plot) parameters
    like the exchange rate, mosaic plot of the replica walk, the Hansmann parameter, and tunneling time.

    A replica is a Markov Chain... a state path is not a Markov chain...
    """

    __slots__ = '_data'

    # Initialize instance of exchange history
    # TODO allow "warm start" from initial conditions
    def __init__(self, data, only_neighbors=True):
        """
        `data` must be a pandas DataFrame with the columns "replica", "config", and "step". Note that the elements in
        "replica" and "config" refer to indices.

        Parameters
        ----------
        data : pandas.DataFrame
            Exchange history.
        only_neighbors : bool
            Were exchanges permitted only between neighbors?
        """

        # Validate input
        if not isinstance(data, pd.DataFrame) or ~np.in1d(['replica', 'config', 'step'], data.columns).all():
            raise AttributeError('data must be DataFrame')

        # Make sure that replicas do not jump by more than 1 configuration at a time if only_neighbors is true
        # TODO is it necessary to have this validation step?
        if only_neighbors:
            n_replicas = data['replica'].nunique()
            data = data.sort_values(['replica', 'step'])
            for replica in range(n_replicas):
                tmp = data.query(f'replica == {replica}')['config'].diff().fillna(0)
                assert tmp.min() == -1
                assert tmp.max() == 1

        # Save
        self._data = data

    # Read NAMD history file (from their RE multi-copy algorithm)
    # TODO what if someone loaded .sort.history? The labels replica and config would be swapped.
    @classmethod
    def from_namd(cls, fname, n_replicas, glob=False):
        """
        Construct the exchange history from the results of NAMD replica exchange.

        Parameters
        ----------
        fname : str
            Name of the history file. The assumption is that there is one history file per replica. This method expects
            to find the variable `{replica}` to specify the file for each replica.
        n_replicas : int
            The number of replicas.
        glob : bool
            Indicates if `fname` contains extra glob-like features, such as wild-cards.

        Returns
        -------
        ExchangeHistory
            Newly-created instance of ExchangeHistory.

        Examples
        --------
        >>> ExchangeHistory.from_namd('exchange_{replica}.history', n_replicas=16, glob=False)
        >>> ExchangeHistory.from_namd('exchange_job?.{replica}.history', n_replicas=16, glob=True)
        """

        # Initialize DataFrame to hold results
        data = pd.DataFrame()

        # Loop over all replicas and read in files
        for replica in range(n_replicas):
            tmp = loadtxt(fname.format(replica=replica), glob=glob)
            data = data.append(pd.DataFrame({
                'step': tmp[:, 0],
                'replica': np.repeat(replica, len(tmp)),
                'config': tmp[:, 1].astype(int),
                'temperature': tmp[:, 2]
            }), ignore_index=True)

        # Return instantiated ExchangeHistory class. This is sorted but there's strictly no reason to do this.
        return cls(data.sort_values(['replica', 'step']))

    # Read history from parquet
    @classmethod
    def from_parquet(cls, fname):
        """
        Read exchange history from parquet.

        Parameters
        ----------
        fname : str
            Parquet file.

        Returns
        -------
        ExchangeHistory
        """

        return cls(pd.read_parquet(fname))

    @property
    def n_configs(self):
        return self._data['config'].nunique()

    @property
    def n_replicas(self):
        return self._data['replica'].nunique()

    @property
    def n_steps(self):
        return self._data['step'].nunique()

    # Cross-tabulate by config and replica axes
    def crosstab(self, index='config', column='replica'):
        """
        Cross-tabulate by "config" and "replica" axes. In other words, count the number of snapshots at given
        config and replica indices.

        Parameters
        ----------
        index : str
            Axis to define rows.
        column : str
            Axis to define columns.

        Returns
        -------
        pandas.DataFrame
            Cross-tabulation of the ExchangeHistory instance.
        """

        # Get the exchange history trajectory by the index
        data = self.trajectory(by=index, reset_index=True)

        # Melt the data by the column
        data_melt = data.melt(value_name=column)

        # Return pandas cross tabulation
        return pd.crosstab(index=data_melt[index], columns=data_melt[column])

    # Compute the exchange rate
    def exchange_rate(self, by='config', add_initial_state=True, n_attempts=None, terminal_factor=0.5):
        """
        Compute the exchange rate.

        Parameters
        ----------
        by : str
            Default: config
        add_initial_state : bool
        n_attempts : int
            Number of attempts per config or replica.
        terminal_factor : float
            Factor to apply to the first and last config to reduce its number of attempts.

        Returns
        -------
        pandas.Series
            Exchange rate per config or replica.
        """

        # Pull the trajectory
        trj = self.trajectory(by=by if by is not None else 'config')
        
        #
        if add_initial_state:
            initial_state = pd.DataFrame(
                [np.arange(len(trj.columns), dtype='int')],
                columns=trj.columns
            )
            trj = pd.concat([initial_state, trj])

        # Derive number of attempts. This is tricky because it depends on how exchange was set up. In unbiased exchange,
        # we expect that every replica/config exchanges every step. However, the terminal configs usually only exchange
        # every other attempt (because they're at a boundary) so we apply the terminal factor. In the future, I would
        # like to make this more intuitive.
        if n_attempts is None:
            n_attempts = np.repeat(len(trj), len(trj.columns))
            n_attempts[0] = np.floor(n_attempts[0] * terminal_factor)
            n_attempts[-1] = np.floor(n_attempts[-1] * terminal_factor)

        # Compute number of exchanges. The logic here is that if the index from one step to the next changes, then an
        # exchange has happened.
        n_exchanges = (trj.diff().dropna(axis=0) != 0).sum()

        # Return the rate
        return np.sum(n_exchanges) / np.sum(n_attempts) if by is None else n_exchanges / n_attempts

    # TODO incorporate this into above
    def direction_exchange_rate(self):
        trj = self.trajectory(by='config')  # must be by the non-walker
        n_steps, n_states = trj.shape

        n_even_steps = (np.mod(trj.index.to_numpy(), 2) == 0).sum()
        n_odd_steps = n_steps - n_even_steps

        df = pd.DataFrame(columns=['state', 'direction', 'n_exchanges', 'n_attempts']).set_index(['state', 'direction'])
        for state in range(n_states):
            for direction in [-1, 1]:
                if (state == 0 and direction == -1) or (state == n_states - 1 and direction == 1):
                    continue
                df.loc[(state, direction), 'n_exchanges'] = (trj[state] == trj[state + direction].shift(-1)).sum()
                df.loc[(state, direction), 'n_attempts'] = n_even_steps if direction == 1 else n_odd_steps
        return df

    def hansmann(self, ):
        r"""
        The Hansmann parameter :math:`h(T)` shows the residence time :math:`\tau` replica :math:`r` (of :math:`R` total
        replicas) spends at configuration :math:`T`.

        .. math:: h(T) = 1 - \frac{\sqrt{\sum_{r=1}^R \tau_r^2}}{\sum_{r=1}^R \tau_r}

        If all replicas are equally sampled across all configurations, then :math:`h(T) = 1 - 1 / \sqrt{R}`.

        Returns
        -------
        pandas.Series
            Hansmann parameter computed for all configurations.
        """

        # Cross-tabulate replica by configuration
        data = self.crosstab(index='config', column='replica')

        # Return Hansmann parameter
        return 1. - np.sqrt(np.square(data).sum(axis=1)) / data.sum(axis=1)

    def hansmann_plot(self, x_title=None, y_title=None, height=None, width=None, plot_theoretical=True):
        """
        Plot the Hansmann parameter.

        Parameters
        ----------
        x_title : str
        y_title : str
        height : numeric
            Height of plot.
        width : numeric
            Width of plot.
        plot_theoretical : bool
            Should the theoretical Hansmann parameter in the case of equal sampling be plotted? (Default: True)
        """

        import uplot as u

        data = self.hansmann()
        x = data.index.to_numpy()
        if x[0] == 0:  # start everything from an index of 1 for aesthetics
            x += 1
        y = data.to_numpy()

        # Build figure
        fig = u.figure(style={
            'x_title': x_title if x_title else r'replica index, $r$',
            'y_title': y_title if y_title else r'mixing parameter, $m$($r$)',
            'y_min': 0.,
            'y_max': 1.,
            'height': height,
            'width': width
        })
        fig += u.line(x, y, style={'color': 'black', 'line_style': 'solid', 'marker': 'circle'})  # noqa
        if plot_theoretical:
            fig += u.hline(
                y=1. - 1. / np.sqrt(len(x)),  # noqa
                style={'color': 'black', 'line_style': 'longdash', 'line_width': 1.}
            )
        fig, ax = fig.to_mpl(show=False)
        fig.savefig('hansmann_plot.svg')

    def mosaic_plot(self, interval=100, cmap='ujet', height=None, width=None):
        """
        Plot the mosaic function using a heatmap.

        Parameters
        ----------
        interval : int
            Interval for plotting. We usually cannot plot every single step because there is too much data.
        cmap : str or object
            The matplotlib-compatible color map.
        height : numeric
            Height of plot.
        width : numeric
            Width of plot.
        """

        import matplotlib.pyplot as plt
        from matplotlib.ticker import MultipleLocator, MaxNLocator
        import uplot as u

        u.core.set_mpl_theme()

        data = self.trajectory(by='config', reset_index=True)
        steps = data.index.to_numpy(dtype='int')[::interval]
        replicas = data.columns.to_numpy(dtype='int')
        if replicas[0] == 0:
            replicas = replicas + 1
            data = data + 1
        mosaic = data.to_numpy(dtype='int')[::interval, :]
        x = np.arange(mosaic.shape[0] + 1)
        y = np.arange(mosaic.shape[1] + 1)

        # Start figure and axis
        figsize = None
        if height is not None and width is not None:
            figsize = (width, height)
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot()
        # im = ax.pcolormesh(mosaic, cmap=cmap, edgecolors='k', linewidth=0.5)  # bwr
        if cmap == 'ujet':
            import uplot
            cmap = uplot.jet
        im = ax.pcolormesh(x - 0.5, y - 0.5, mosaic.T, cmap=cmap, edgecolors='k', linewidth=0.5)

        # Format x axis
        # TODO change this so only units of X are display
        ax.set_xticks(np.arange(len(steps)))
        ax.set_xticklabels(steps)
        ax.set_xlabel(r'step')

        # Format y axis
        ax.set_yticks(np.arange(len(replicas)))
        ax.set_yticklabels(replicas)
        ax.set_ylabel(r'temperature index')

        # Format tick lines
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='both', which='both', direction='out')

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(MultipleLocator(10))

        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_minor_locator(MultipleLocator(1))

        # fig.colorbar()
        ax.set_aspect('auto')
        # ax.grid(which='minor', color='w', linestyle='-', linewidth=5)

        ax.grid(linestyle='')

        # plt.axis('equal')
        # Add color bar
        cbar = plt.colorbar(im, ax=ax, shrink=0.5, drawedges=False)
        cbar.outline.set_linewidth(0.5)
        # cbar.ax.spines['right'].set_visible(True)
        cbar.ax.tick_params(direction='out', length=5.)
        cbar.ax.tick_params(which='minor', length=0)
        #        cbar.ax.yaxis.set_major_locator(MultipleLocator(1))
        cbar.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        cbar.ax.set_ylabel(r'replica index')

        # Save the image
        # fig.show()
        fig.savefig('mosaic_plot.svg')

    # Exchange rate plot
    def rate_plot(self):
        import uplot as u
        u.plot(
            self.exchange_rate(by='config'),  # noqa
            x_title='replica',
            y_title='exchange rate',
            y_min=0.,
            y_max=1.,
            height=5,
            width=6,
            save_as='exchange_rate.svg',
        )

    # Reset the step index?
    def reset_step(self):
        """
        Resets step from arbitrary interval to rank from 1 ... N. This operation occurs in place.
        """

        self._data['step'] = self._data['step'].rank(method='dense')

    # Save to csv
    def to_csv(self, *args, **kwargs):
        """
        Save ExchangeHistory to csv format. Follows :ref:`pandas.DataFrame.to_csv`.
        """
        self._data.to_csv(*args, **kwargs)

    # Save to parquet
    def to_parquet(self, *args, **kwargs):
        """
        Save ExchangeHistory to parquet format. Follows :ref:`pandas.DataFrame.to_parquet`.
        """

        self._data.to_parquet(*args, **kwargs)

    # TODO should this be renamed mosaic?
    def trajectory(self, by='config', reset_index=True):
        """
        Compute the walk of config or replicas. This is a pivot of the melted ExchangeHistory._data.

        Parameters
        ----------
        by : str
            Default: config.
        reset_index : bool
            Should the index be reset?

        Returns
        -------
        pandas.DataFrame
        """

        # Define the columns and values for the pivot
        columns = 'config'
        values = 'replica'
        if by == 'replica':
            columns, values = values, columns
        elif by != 'config':
            raise AttributeError(f'do not understand by = {by}')

        # Perform the pivot
        data = self._data.pivot(index='step', columns=columns, values=values)

        # Reset index?
        if reset_index:
            data.reset_index(drop=True, inplace=True)
            data.index.name = 'step'

        # Return
        return data

    # State transitions
    def state_transitions(self, walker='replica'):
        """
        Compute state transitions similar to the "tunneling time" as referenced in [Straub09JCP]_. The language here is
        somewhat different than the rest of the class. We have a "walker" that randomly walks across "state" space.
        We are counting transitions of length :math:`r`, which occurs when a walker originally at state :math:`i`
        moves to the state :math:`i+r` or :math:`i-r`.

        Consider a walker samples 3 states given by indices 0-2.

        .. code-block::
           00011000112210012

        This can be decomposed in several ways. For instance, if :math:`i=0` and :math:`r=1`, then there are 3 such
        transition events: "0001-------------", "-----0001--------", and "-------------001-". For clarity,
        the states not involved explicitly in this type of transition are denoted by "-". Notice that we are always
        looking at the first instance of state :math:`i` and the steps after :math:`i` it takes to get to the first
        instance of state :math:`i+r` (or :math:`i-r`). We can do this again where :math:`i=1`, :math:`i+r=2`,
        and :math:`i-r=0`. The transition events are "---110-----------", "--------112------", "------------10---",
        and "---------------12". Taken together, for transitions of length :math:`r=1`, we have 7 events: 2 with 4
        steps, 3 with 3 steps, and 2 with 2 steps. We can therefore say that the  average number of steps
        for that transition length is :math:`3`.

        Returns
        -------
        dict of arrays
            The key in the dictionary is all possible transition lengths :math:`1...R-1`, where :math:`R` is the
            number of replicas.

        References
        ----------
        .. [Straub09JCP] Kim, J., Keyes, T., & Straub, J. E. (2009) Replica exchange statistical temperature Monte
        Carlo. *J. Chem. Phys.* 130, 124112.
        """

        data = self.trajectory(walker)
        if not (data.diff().abs().max() == 1.).all():  # noqa
            raise AttributeError(f'{walker} cannot be the walker, step size exceeds 1')

        # TODO can this be simplified?
        n_steps, n_walkers = data.shape
        n_states = n_walkers  # redundant, but makes logic clearer
        steps = {}
        for k in range(n_walkers):  # This is the walker
            walker_data = data[walker].to_frame('state')
            for state in range(n_states):  # First state
                for r in range(1, n_states - 1):  # To get either state - r or state + r
                    state_data = walker_data.query(f'state in [{state}, {state - r}, {state + r}]').reset_index()
                    mask = state_data['state'].diff() != 0  # remove repeated rows
                    state_data = state_data[mask].copy()  # apply mask
                    state_data['n_steps'] = state_data['step'].shift(-1) - state_data['step']
                    transitions = state_data.query(f'state == {state}')['n_steps'].dropna().to_numpy()  #
                    steps[r] = np.append(steps.get(r, []), transitions)

        return steps


# Replica state
class State:
    def __init__(self):
        self.temperature = None
        self.pressure = None


# Create a temperature schedule
def temp_schedule(temp_min=300, temp_max=440, n_temps=40, mode='geometric'):
    r"""
    Create a temperature schedule that could be used, for instance, with replica exchange.

    There are several choices for `mode`. Note that :math:`T` refers to the temperature at :math:`i = 1 ... R`, where
    :math:`T_1` is `temp_min` and :math:`T_R` is `temp_max`. In total, there are :math:`R` temperatures (= `n_temps`).

    * "geometric" [#]_

    .. math :: T_i = T_1 \left( \frac{T_R}{T_1} \right)^{\frac{i-1}{R-1}}

    * "linear"

    .. math :: T_i = T_1 + (i-1) \frac{T_R-T_1}{R-1}

    * "parabolic" (Note if `n_temps` is even, `temp_max` won't directly be sampled).

    .. math :: T_i = T_1 - \frac{T_R-T_1}{\left( \frac{R-1}{2} \right) ^2} (i-1) (i-R)

    Parameters
    ----------
    temp_min : float
        Lowest temperature
    temp_max : float
        Highest temperature
    n_temps : int
        Number of temperatures
    mode : str
        Mode to produce schedule. Valid options include "geometric", "linear", "parabolic". Any substring will match,
        but the preference should be to use the full option label. (Default: "geometric")

    Returns
    -------
    numpy.ndarray
        Temperature schedule

    Examples
    --------
    .. plot::
       :include-source:

       import matplotlib.pyplot as plt
       import molecular as mol

       n_temps = 10
       geometric = mol.temp_schedule(300, 440, n_temps, 'geometric')
       linear = mol.temp_schedule(300, 440, n_temps, 'linear')
       parabolic = mol.temp_schedule(300, 440, n_temps, 'parabolic')

       plt.figure()
       plt.plot(range(n_temps), geometric, label='geometric')
       plt.plot(range(n_temps), linear, label='linear')
       plt.plot(range(n_temps), parabolic, label='parabolic')
       plt.xlabel('index')
       plt.ylabel('temperature')
       plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
       plt.show()

    References
    ----------
    .. [#] Nymeyer, H., Gnanakaran, S., & García, A. E. (2004) Atomistic simulations of protein folding, using the
       replica exchange algorithm. *Methods Enzymol.* **383**: 119-149.
    """

    mode = mode.lower()

    if mode in 'geometric':
        schedule = temp_min * np.power(temp_max / temp_min, np.arange(n_temps) / (n_temps - 1.), dtype=np.float64)

    elif mode in 'linear':
        schedule = np.linspace(start=temp_min, stop=temp_max, num=n_temps)

    elif mode in 'parabolic':
        temp_range = temp_max - temp_min
        temp_ind = np.arange(n_temps)
        schedule = temp_min - (temp_range / np.square((n_temps - 1.) / 2.)) * temp_ind * (temp_ind - n_temps + 1.)

    else:
        raise AttributeError(f'mode {mode} not supported')

    return schedule


if __name__ == '__main__':
    print(temp_schedule(temp_min=300, temp_max=440, n_temps=5, mode='geometric'))
    # print(temp_schedule(temp_min=310, temp_max=500, n_temps=5, mode='parabolic'))
