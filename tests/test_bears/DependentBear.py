from coalib.bears.LocalBear import LocalBear
from tests.test_bears.BearA import BearA


class DependentBear(LocalBear):
    BEAR_DEPS = {BearA}
