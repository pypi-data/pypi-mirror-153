import numpy as np
import pandas as pd


class Histogram:
    def __init__(self, data, weights=None):
        self._data = data

        # FIXME for non-ihist, the width will impact the mass function
        if weights is None:
            weights = 1.

        # self._probs = counts / np.sum(counts)  # pmf

    @property
    def counts(self):
        return self._data

    @property
    def pmf(self):
        """

        Returns
        -------

        """

        df = self._data / self._data.sum(axis=0)

        if len(df.columns) > 1:
            df.columns.name = 'pmf'
        else:
            df.rename(columns={'count': 'pmf'}, inplace=True)

        return df

    def plot(self):
        import uplot as u
        u.plot(self.to_frame())

    # FIXME when count = False and probability = False, this will break because there will be a pandas index with no
    #  other content.
    def to_frame(self, count=True, probability=False):
        # df = pd.DataFrame({'bin': self._bins})
        # if count:
        #     df['count'] = self._counts
        # if probability:
        #     df['probability'] = self._probs
        #
        # return df.set_index('bin')
        return self._data


def hist(a, bins):
    """
    Classical histogram, numpy style.

    Parameters
    ----------
    a
    bins

    Returns
    -------

    """

    pass


def ihist(a, width, right=False):
    """
    Create an interval histogram, i.e., given a known `width`, count all the occurrences of `a` in all bins :math:`[
    width, 2*width)`. By default, `right = False`. If true, then we look at :math:`(width, 2*width]` instead.

    Parameters
    ----------
    a : array
        Collection of values to turn into histogram.
    width : number
        The interval that should be binned.
    right : bool
        Left or right inclusive? If False, left inclusive. (Default: False)

    Returns
    -------
    Histogram
        Object that contains the histogram.
    """

    # Take `a` and get binned values
    func = np.floor if not right else np.ceil
    a_binned = func(a / width) * width

    # Create histogram
    if isinstance(a_binned, pd.DataFrame):
        a_melt = pd.melt(a_binned, value_name='bin', var_name='count')
        data = pd.crosstab(a_melt['bin'], a_melt['count'])
    else:
        bins, counts = np.unique(a_binned, return_counts=True)
        data = pd.DataFrame({'bin': bins, 'count': counts}).set_index('bin')

    # Return Histogram object
    return Histogram(data)


if __name__ == '__main__':
    a = np.random.rand(100000)
    print(ihist(a, 0.1).to_frame(probability=True, count=False))
