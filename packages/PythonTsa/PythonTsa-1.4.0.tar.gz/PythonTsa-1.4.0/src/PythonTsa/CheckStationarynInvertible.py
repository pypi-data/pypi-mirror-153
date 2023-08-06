import numpy as np

def isstationary(armaProcess):
        """
        Arma process is stationary if AR roots are outside unit circle.

        Returns
        -------
        bool
             True if AR roots all are outside unit circle.
        """
        narroots=armaProcess.arroots.shape[0]
        arrts=armaProcess.arroots
        for t in range(narroots):
            arrts[t]=float("%.6f" % abs(arrts[t]))
        if np.all(arrts > 1.0):
            return True
        else:
            return False


def isinvertible(armaProcess):
        """
        Arma process is invertible if MA roots are outside unit circle.

        Returns
        -------
        bool
             True if MA roots all are outside unit circle.
        """
        nmaroots=armaProcess.maroots.shape[0]
        marts=armaProcess.maroots
        for t in range(nmaroots):
            marts[t]=float("%.6f" % abs(marts[t]))
        if np.all(marts > 1.0):
            return True
        else:
            return False
