from .s2gpp import s2gpp_local, s2gpp_distributed_main, s2gpp_distributed_sub
from sklearn.base import BaseEstimator
from typing import Optional
from multiprocessing import cpu_count
from pathlib import Path
from enum import Enum


class Clustering(Enum):
    KDE="kde"
    MeanShift="meanshift"


class Series2GraphPP(BaseEstimator):
    def __init__(self,
                 pattern_length: int,
                 latent: Optional[int] = None,
                 rate: int = 100,
                 query_length: Optional[int] = None,
                 n_threads: int = -1,
                 clustering: Clustering = Clustering.KDE,
                 # explainability: bool = False,
                 self_correction: bool = False,
                 local_host="127.0.0.1:1992"
                 ):
        self.pattern_length = pattern_length
        self.latent = latent or int(self.pattern_length / 3)
        self.rate = rate
        self.query_length = query_length or self.pattern_length
        self.n_threads = n_threads if n_threads > 0 else min(cpu_count() - 1, 1)
        self.clustering = clustering
        self.self_correction = self_correction
        self.local_host = local_host

    def fit(self, X: Path, output_path: Path = Path("./anomaly_scores.csv"), column_start=1, column_end=-1):
        s2gpp_local(
            str(X),
            self.pattern_length,
            self.latent,
            self.query_length,
            self.n_threads,
            output_path,
            column_start,
            column_end,
            self.clustering.value,
            self.self_correction,
            self.local_host
        )
