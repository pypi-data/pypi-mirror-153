import numpy as np
from pycsou.core.linop import LinearOperator
from typing import Union, Optional
from numbers import Number
from scipy import fft
from scipy.fftpack import next_fast_len


class RealFFTConvolve2D(LinearOperator):
    def __init__(self, filter, dtype: Optional[type] = None):
        """
        Linear operator that performs convolution in Fourier domain, and assumes
        real-valued signals.

        Parameters
        ----------
        filter :py:class:`~numpy.ndarray`
            2D filter to use. Must be of shape (height, width, channels) even if
            only one channel.
        dtype : float32 or float64
            Data type to use for optimization.
        """

        assert len(filter.shape) == 3
        self._filter_shape = np.array(filter.shape)
        self._n_channels = filter.shape[2]

        # cropping / padding indices
        self._padded_shape = 2 * self._filter_shape[:2] - 1
        self._padded_shape = np.array([next_fast_len(i) for i in self._padded_shape])
        self._padded_shape = np.r_[self._padded_shape, [self._n_channels]]
        self._start_idx = (self._padded_shape[:2] - self._filter_shape[:2]) // 2
        self._end_idx = self._start_idx + self._filter_shape[:2]

        # precompute filter in frequency domain
        self._H = fft.rfft2(self._pad(filter), axes=(0, 1))
        self._Hadj = np.conj(self._H)
        self._padded_data = np.zeros(self._padded_shape).astype(dtype)

        shape = (int(np.prod(self._filter_shape)), int(np.prod(self._filter_shape)))
        super(RealFFTConvolve2D, self).__init__(shape=shape, dtype=dtype)

    def _crop(self, x):
        return x[self._start_idx[0] : self._end_idx[0], self._start_idx[1] : self._end_idx[1]]

    def _pad(self, v):
        vpad = np.zeros(self._padded_shape).astype(v.dtype)
        vpad[self._start_idx[0] : self._end_idx[0], self._start_idx[1] : self._end_idx[1]] = v
        return vpad

    def __call__(self, x: Union[Number, np.ndarray]) -> Union[Number, np.ndarray]:
        # like here: https://github.com/PyLops/pylops/blob/3e7eb22a62ec60e868ccdd03bc4b54806851cb26/pylops/signalprocessing/ConvolveND.py#L103
        self._padded_data[
            self._start_idx[0] : self._end_idx[0], self._start_idx[1] : self._end_idx[1]
        ] = np.reshape(x, self._filter_shape)
        y = self._crop(
            fft.ifftshift(
                fft.irfft2(fft.rfft2(self._padded_data, axes=(0, 1)) * self._H, axes=(0, 1)),
                axes=(0, 1),
            )
        )
        return y.ravel()

    def adjoint(self, y: Union[Number, np.ndarray]) -> Union[Number, np.ndarray]:
        self._padded_data[
            self._start_idx[0] : self._end_idx[0], self._start_idx[1] : self._end_idx[1]
        ] = np.reshape(y, self._filter_shape)
        x = self._crop(
            fft.ifftshift(
                fft.irfft2(fft.rfft2(self._padded_data, axes=(0, 1)) * self._Hadj, axes=(0, 1)),
                axes=(0, 1),
            )
        )
        return x.ravel()
