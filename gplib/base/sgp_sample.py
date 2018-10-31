from gplib.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        "gp": ["gplib.base", "PopulationGP"],
        "initializer": [
            "gplib.operators", "PopulationRandomInitializer", [500, 0.1, 10]
        ],
        "problem": [
            "gplib.problems", "EvenParity", {"dim": 3}
        ],
        "sequential": [
            ["gplib.operators", "PopulationOnePointCrossover", {"c_rate": 0.5, "destructive": False}],
            ["gplib.operators", "PopulationPointMutation", {"m_rate": 0.2}],
            ["gplib.operators", "TournamentSelection", {"k": 500, "tournament_size": 5}]
        ],
        "viewer": [
            "gplib.viewer", "DefaultViewer"
        ],
        "terminal_condition": [
            ["gplib.terminator", "GenerationTerminator", {"t_gene": 10}],
            ["gplib.terminator", "EvalCountTerminator", {"t_eval_cnt": 100000}]
        ],
    }

    gp = gp_from_config(config)
    gp()
