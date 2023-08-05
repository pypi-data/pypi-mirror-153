SEP_LINE = "---------------------------------------------"


def read_rouge(rouge_path):
    """Read ROUGE scores from ROUGE-1.5.5 output (or wrapper)
    Args:
        rouge_path(str): path of ROUGE file
    Returns:
        rouge_scores(dict): all scores,
            {$m: {$s: float}}
            for $m in ['rouge-1', 'rouge-2', 'rouge-l']
            for $m in ['f', 'r', 'p']
    """
    with open(rouge_path) as f:
        lines = [_.strip() for _ in f]

    rouge = {}
    for i, line in enumerate(lines):
        if line == SEP_LINE:
            # print("Ignore SEP line")
            continue
        elif line.startswith("1 "):
            line = line[2:]

            metric, stat_and_score = line.split("Average")

            assert metric.startswith("ROUGE-")
            metric = metric.lower().strip()

            stat, score = stat_and_score.split(":")
            assert stat.startswith("_")
            stat = stat.replace("_", "").lower()

            score_value, confidence = score.split("(")
            score_value = float(score_value)

            conf_prct, conf_int = confidence.split("-conf.int. ")
            assert conf_prct.endswith("%")
            conf_prct = float(conf_prct.replace("%", "")) / 100

            assert conf_int.endswith(")")
            conf_lower, conf_upper = conf_int.replace(")", "").split(" - ")

            if not metric in rouge.keys():
                rouge[metric] = {}
            if stat in rouge[metric].keys():
                raise ValueError("Mutliple value for %s %s at line %d"
                                 % (metric, stat, i))
            rouge[metric][stat] = score_value

        elif len(line) == 0:
            # print("Ignore empty line")
            continue
        else:
            raise ValueError("Unkown line (%d): %s" % (i, line))

    return rouge
