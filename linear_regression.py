# -*- coding: utf-8 -*-
import numpy as np
from scipy import stats
# Implement LinearRegression for large data with split and conquer method
# see https://zhuanlan.zhihu.com/p/25312342


def score_r2(y_label, y_pred):
    m_y = np.mean(y_label)
    lyy = np.sum(np.square(y_label - m_y))
    if lyy <= 1e-15:
        return -1
    return float(1.0 - np.sum(np.square(y_label - y_pred)) / lyy)


class LinearRegressionBase:
    """
    LinearRegressionBase:
    for speed consideration, user should be aware of data preprocessing, e.g. normalization
    """
    def __init__(self, n_features):
        """
        :param n_features: a positive integer

        :member_variable sk: X'X, store it for later used in split and conquer method
        :member_variable beta_: regression coefficients
        :member_variable is_singular_: indicate whether the last fit method is valid or not
        """

        self.sk = np.zeros((n_features, n_features), dtype=np.float64)
        self.beta_ = np.zeros(n_features, dtype=np.float64)
        self.is_singular_ = True

    def reset_features(self, n_features):
        if n_features != self.beta_.shape[0]:
            self.sk = np.zeros((n_features, n_features), dtype=np.float64)
            self.beta_ = np.zeros(n_features, dtype=np.float64)
            self.is_singular_ = True

    @property
    def is_singular(self):
        return self.is_singular_

    @property
    def is_non_singular(self):
        return not self.is_singular_

    def set_coef(self, coef):
        """
        :param coef: np.1darray with same shape as self.beta_
        :return:
        """
        assert coef.shape == self.beta_.shape
        self.beta_[:] = coef
        self.is_singular_ = False

    def fit(self, x, y):
        """
        :param x: numpy array or sparse matrix of shape [n_samples,n_features]
        :param y: numpy array of shape [n_samples, ]
        :return:
        """
        assert x.shape[1] == self.beta_.shape[0]
        # self.sk = np.dot(x.T, x)  # X'X
        np.dot(x.T, x, out=self.sk)  # X'X  for performance
        try:
            sk_inv = np.linalg.inv(self.sk)
            self.is_singular_ = False

            # self.beta_ = np.dot(sk_inv, np.dot(x.T, y))

            np.dot(sk_inv, np.dot(x.T, y), out=self.beta_)  # for performance
        except np.linalg.LinAlgError as e:
            print('LinearRegressionBase:', e)
            self.is_singular_ = True

    def predict(self, x, out=None):
        """
        :param x: np.2darray with shape (n_samples, n_features)
        :param out:
        :return: 
        """
        return np.dot(x, self.beta_, out=out)

    def r2(self, x, y):
        y_pred = self.predict(x)
        return float(score_r2(y, y_pred))


class LinearRegression(LinearRegressionBase):
    def __init__(self, n_features):
        LinearRegressionBase.__init__(self, n_features)
        self.f_value = 0
        self.f_pvalue = 1
        self.ssr = 0

    def stat(self, x, y, full_stats=True,  display=True):
        """
        :param x:
        :param y:
        :param full_stats: boolean, whether compute all relative stats
        :param display:
        :return: None or pd.DataFrame
        """
        n, m = x.shape

        y_pred = self.predict(x)
        self.ssr = np.sum(np.square(y_pred - y))  # sum( (\hat y_i - y_i)^2 )
        lyy = np.sum(np.square(y - np.mean(y)))
        r2_value = 1.0 - self.ssr / lyy
        # r2_value = self.r2(x, y)

        self.f_value = (r2_value / m) / ((1 - r2_value) / (n - m - 1.))
        self.f_pvalue = (1 - stats.f.cdf(self.f_value, m, n - m - 1))

        if not full_stats:
            return None

        Q = self.ssr
        adj_r2 = 1 - (1 - r2_value) * (n - 1.0) / (n - m - 1.0)

        cc = np.linalg.inv(self.sk)  # Inverse(X'X)

        t_values = self.beta_ / np.sqrt(np.diagonal(cc) * Q / (n - m - 1.0))
        # f_values = np.square(t_values)      # \beta_i^2 / (l^{ii} * Q /(n-m-1))
        # pf_values = 1.0 - stats.f.cdf(f_values, 1, n - m - 1)
        p_values = (1. - stats.t.cdf(np.abs(t_values), n - m - 1)) * 2.
        # error_variance = Q / (n - m - 1.0)

        def code_function(x):
            if x < 0.001:
                return "***"
            elif x < 0.01:
                return "**"
            elif x < 0.05:
                return "*"
            elif x < 0.1:
                return "."
            return " "

        codes = list(map(code_function, p_values))

        import pandas as pd
        df = pd.DataFrame({"coef": self.beta_, "t values": t_values, "p(>|t|)": p_values, "Signif": codes},
                           # "f values": f_values, "p(>f)": pf_values},
                          columns=["coef", "t values", "p(>|t|)", "Signif"], index=range(1, len(codes) + 1))

        if display:
            print(df)
            print("\nSignif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1\n")
            print("R-squared: %.8f, Adjust R-squared: %.8f" % (r2_value, adj_r2))

        return df


# # Suppose we have chunk data X_1, X_2, ..., X_N, 
# # We train a model with m consecutive chunk data X_i, X_(i+1), ..., X_(i + m -1), where m << N.
# # The class LinearRegressionConquer is specialized for a fasting training in such a situation when training N-m+1 models.
class LinearRegressionConquer(LinearRegressionBase):
   """
   LinearRegressionConquer:
   for speed consideration, user should be aware of data preprocessing, e.g. normalization
   """
   def __init__(self, num_features, chunk_size):
        super().__init__(num_features)
        self.chunk_size_ = chunk_size

        self.lr_base_ = LinearRegressionBase(num_features)

        # # first line store (sk*beta), last num_features lines store (sk)
        self.sk_beta_sum_ = np.zeros((num_features + 1, num_features), dtype=np.float64)

        self.cache_ = np.zeros((chunk_size, num_features + 1, num_features), dtype=np.float64)

        self.chunk_index_ = 0
        self.can_regress_ = False

    def reset_features(self, num_features):
        if num_features == self.beta_.shape[0]:
            return
        super().reset_features(num_features)

        self.lr_base_ = LinearRegressionBase(num_features)

        # # first line store (sk*beta), last num_features lines store (sk)
        self.sk_beta_sum_ = np.zeros((num_features + 1, num_features), dtype=np.float64)

        self.cache_ = np.zeros((self.chunk_size_, num_features + 1, num_features), dtype=np.float64)

        self.chunk_index_ = 0
        self.can_regress_ = False

    def add_and_fit(self, x, y):
        lr_base = self.lr_base_
        lr_base.fit(x, y)
        if lr_base.is_non_singular:
            # # store chunk linear regression's result

            # self.cache_[self.chunk_index_, -1, :] = np.dot(lr_base.sk, lr_base.beta_)
            np.dot(lr_base.sk, lr_base.beta_, out=self.cache_[self.chunk_index_, 0, :])  # for performance
            self.cache_[self.chunk_index_, 1:, :] = lr_base.sk

            # # addition new data
            self.sk_beta_sum_ += self.cache_[self.chunk_index_, :, :]

            self.chunk_index_ += 1
            if self.chunk_index_ >= self.chunk_size_:
                self.can_regress_ = True

                self.chunk_index_ -= self.chunk_size_

            if self.can_regress_:
                # do regression
                try:
                    sk_inv = np.linalg.inv(self.sk_beta_sum_[1:, :])
                    self.is_singular_ = False

                    # self.beta_ = np.dot(sk_inv, self.sk_beta_sum_)
                    np.dot(sk_inv, self.sk_beta_sum_[0, :], out=self.beta_)  # for performance

                except np.linalg.LinAlgError as e:
                    print('LinearRegressionConquer:', e)
                    pass

                # # subtract old data
                self.sk_beta_sum_ -= self.cache_[self.chunk_index_, :, :]


