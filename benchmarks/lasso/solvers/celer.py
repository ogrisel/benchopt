import warnings

from benchopt.base import BaseSolver
from benchopt.util import safe_import_context


with safe_import_context() as import_ctx:
    from celer import Lasso
    from celer.homotopy import ConvergenceWarning


class Solver(BaseSolver):
    name = 'Celer'
    sampling_strategy = 'iteration'

    install_cmd = 'conda'
    requirements = [
        'pip:git+https://github.com/mathurinm/celer.git'
    ]

    def set_objective(self, X, y, lmbd):
        self.X, self.y, self.lmbd = X, y, lmbd

        warnings.filterwarnings('ignore', category=ConvergenceWarning)
        n_samples = self.X.shape[0]
        self.lasso = Lasso(
            alpha=self.lmbd/n_samples, max_iter=1, gap_freq=10,
            max_epochs=100000, p0=10, verbose=False, tol=1e-12, prune=True,
            fit_intercept=False, normalize=False, warm_start=False,
            positive=False
        )

    def run(self, n_iter):
        self.lasso.max_iter = n_iter
        self.lasso.fit(self.X, self.y)

    def get_result(self):
        return self.lasso.coef_.flatten()
