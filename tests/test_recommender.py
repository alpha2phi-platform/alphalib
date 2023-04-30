import unittest

import numpy as np
import requests
from scipy.optimize import LinearConstraint, minimize, minimize_scalar, rosen


def objective_function1(x):
    return 3 * x**4 - 2 * x + 1


def objective_function2(x):
    return x**4 - x**2


class TestRecommender(unittest.TestCase):
    def test_minimize(self):
        x0 = [1.3, 0.7, 0.8, 1.9, 1.2]
        res = minimize(rosen, x0, method="Nelder-Mead", tol=1e-6)
        print(res)

    def test_numpy(self):
        x = np.random.choice([False, True], size=100000)
        print(x.shape)
        print(x[:-1].shape)
        print(np.empty((10, 2), dtype=int))

    def test_min_scalar(self):
        res = minimize_scalar(objective_function2)
        print(res)

    def test_min(self):
        # https://realpython.com/python-scipy-cluster-optimize/
        n_buyers = 10
        n_shares = 15
        np.random.seed(10)
        prices = np.random.random(n_buyers)
        money_available = np.random.randint(1, 4, n_buyers)
        n_shares_per_buyer = money_available / prices
        print(prices, money_available, n_shares_per_buyer, sep="\n")

        constraint = LinearConstraint(np.ones(n_buyers), lb=n_shares, ub=n_shares)
        bounds = [(0, n) for n in n_shares_per_buyer]

        def objective_function(x, prices):
            return -x.dot(prices)

        res = minimize(
            objective_function,
            x0=10 * np.random.random(n_buyers),
            args=(prices,),
            constraints=constraint,
            bounds=bounds,
        )
        print(res)
        print("The total number of shares is:", sum(res.x))
        print("Leftover money for each buyer:", money_available - res.x * prices)

    def test_requests(self):
        response = requests.get("https://reqres.in/api/users?page=2")
        print(response.text)
