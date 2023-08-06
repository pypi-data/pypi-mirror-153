-- depends: 035__add_weights

create index if not exists se_score_weight_name on ScoreWeights(score_name);
