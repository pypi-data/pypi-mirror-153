#!/usr/bin/env python
import os
import re
import numpy as np

from pltrdy.rouge import read_rouge
from pltrdy.wc import wordcount


def srcrougefct(x):
    if x["src_rouge"] == "none":
        return 0.0
    else:
        return -float(x["src_rouge"].split(";")[0])


def perplexity(rouge_path, incl_oov=True):
    n_line = 0 if incl_oov else 1

    ppl_path = rouge_path.replace("rouge", "ppl")
    with open(ppl_path) as f:
        lines = [_.strip() for _ in f]
    line = lines[n_line]
    ppl = line.split("OOVs:")[-1]
    ppl = float(ppl)
    return ppl


def dual_xent(rouge_path, agg=np.mean, n=None):
    dual_xent_path = rouge_path.replace(".rouge", ".dual_xent.src-pred")

    xents = []
    with open(dual_xent_path) as f:
        for line in f:
            line = line.strip()
            xent = float(line)
            xents.append(xent)
    if n is not None:
        assert len(xents) == n

    return agg(xents)


def src_rouge(rouge_path):
    src_rouge_path = rouge_path.replace('.rouge', '.src_rouge')
    r = read_rouge(src_rouge_path)
    return r


def read_rouge_memory(rouge_path, memory={}, key="rouge"):
    if key in memory.keys():
        return memory[key]
    score = read_rouge(rouge_path)
    memory[key] = score
    return score


def step_field_fct(self, rouge_path, memory):
    name = os.path.basename(rouge_path)

    try:
        step = name.split("_pred.")[1].split("k")[0]
    except IndexError:
        raise IndexError("Cannot read step of '%s'" % rouge_path)
    return step


def dec_suffix_field_fct(self, rouge_path, memory):
    step = memory.get("step")
    if step is None:
        raise ValueError(
            "dec_suffix suppose 'step' field (absent from memory)")
    dec_suffix = rouge_path.split(str(step) + "k")[1]\
        .split(".txt")[0]\
        .replace('.', '')\
        .replace('true_test', '')
    return clean_suffix(dec_suffix)


def wc_field_fct(self, rouge_path, memory):
    wc = int(wordcount(rouge_path.replace('.rouge', '')))
    return wc


def src_rouge_field_fct(self, rouge_path, memory):
    r = src_rouge(rouge_path)
    return " ; ".join([
        "%2.2f" % (100 * float(r["rouge-1"][k]))
        for k in ["r", "p", "f"]
    ])


def model_name_by_pred(result_name):
    return result_name.split("_pred.")[0]


def clean_suffix(suffix):
    to_remove = ["bpe", "decoded", "rouge"]
    for r in to_remove:
        suffix = suffix.replace(r, "")
    return suffix


class ResultsExplorer(object):
    MODEL_NOTOK_REG = r'model_(.*)notok(.*)_pred(.*)'

    # Fields function
    # i.e. calculate field value from self, rouge_path, memory
    DEFAULT_FIELDS = {
        'exp': lambda s, p, m: os.path.dirname(p),
        'model': lambda s, p, m: s.model_from_result_name(os.path.basename(p)),
        'step': lambda s, p, m: step_field_fct(s, p, m),
        'dec_suffix': lambda s, p, m: dec_suffix_field_fct(s, p, m),
        'wc': lambda s, p, m: wc_field_fct(s, p, m),
        'rouge_1': lambda s, p, m: read_rouge_memory(p, m)["rouge-1"]["f"],
        'rouge_2': lambda s, p, m: read_rouge_memory(p, m)["rouge-2"]["f"],
        'rouge_l': lambda s, p, m: read_rouge_memory(p, m)["rouge-l"]["f"],
        'src_rouge': lambda s, p, m: src_rouge_field_fct(s, p, m)
    }

    FILTERS = {
        "valid": lambda p: ".valid" in p,
        "predtok": lambda p: ("predtok" in p or re.match(ResultsExplorer.MODEL_NOTOK_REG, p) is not None),
        "onlytoks": lambda p: "onlytoks" in p,
    }

    SORT_FCT = {
        "copy_desc": srcrougefct,
        "ppl": lambda x: -x["ppl"]
    }

    DEFAULT_REGEX = r"model(.*)\.rouge"

    def __init__(self, name, exps=[], default_regex=DEFAULT_REGEX, exps_with_regex={},
                 custom_filters={}, extra_fields={},
                 exclude_fields=[], fields=DEFAULT_FIELDS.keys(),
                 model_name_fct=model_name_by_pred):
        """
            name:
            exps: list of directories where *.rouge files are
            exps_with_regex: dict of `directory: regex`
            custom_filters: dict of filters `name: filter function`
            extra_fields: dict of `name: field function` that take a .rouge
                          path and should return the field value

        """
        self.name = name

        self.exps_with_regex = exps_with_regex
        self.exps_with_regex.update({
            e: default_regex
            for e in exps
        })

        self.fields = {}
        for k in fields:
            if k in exclude_fields:
                continue
            if k in ResultsExplorer.DEFAULT_FIELDS.keys():
                self.fields[k] = ResultsExplorer.DEFAULT_FIELDS[k]
            else:
                raise ValueError("Unknow field %s, choices are: %s"
                                 % (k, list(ResultsExplorer.DEFAULT_FIELDS[k])))
        self.fields.update(extra_fields)

        self.filters = dict(ResultsExplorer.FILTERS)
        self.filters.update(custom_filters)

        self.model_name_fct = model_name_fct

    def model_from_result_name(self, result_name):
        return self.model_name_fct(result_name)

    def all_filters(self, path, filters_switch):
        for k, v in filters_switch.items():
            _v = self.filters[k](path)
            print(path, k, v, _v)
            if not v == _v:
                return False
        return True
        return all([
            self.filters[k](path) == v
            for k, v in filters_switch.items()
        ])

    def explore_results(self, sort_field=None, **filters):
        fields = self.fields
        results = []

        for exp_root, reg in self.exps_with_regex.items():
            print(exp_root)
            exp_results = sorted([
                _ for _ in os.listdir(exp_root)
                if re.match(reg, _) is not None
                and self.all_filters(_, filters)
            ])
            for result_name in exp_results:
                rouge_path = os.path.join(exp_root, result_name)

                r = {}
                for key, fct in fields.items():
                    r[key] = fct(self, rouge_path, r)

                results.append(r)

        if sort_field is None:
            results = sorted(results,
                             key=lambda x: (
                                 x['rouge_1'],
                                 x['exp'],
                                 x['model'],
                                 x['step']
                             ),
                             reverse=True)
        else:
            if sort_field in ResultsExplorer.SORT_FCT:
                sort_fct = ResultsExplorer.SORT_FCT[sort_field]
            else:
                def sort_fct(x): return x[sort_field]
            results = sorted(results,
                             key=lambda x: (
                                 sort_fct(x),
                                 x['rouge_1'],
                                 x['exp'],
                                 x['model'],
                                 int(x['step'].replace('k', ''))
                             ),
                             reverse=True)

        assert len(results) > 0
        m = ["| " + "|  ".join(fields) + " |"]
        m += ["|---" * len(fields) + " |"]

        top = {k: max([r[k] for r in results])
               for k in ['rouge_1', 'rouge_2', 'rouge_l', 'wc']}
        for r in results:
            for k in ['rouge_1', 'rouge_2', 'rouge_l', 'wc']:
                if r[k] == top[k]:
                    r[k] = "**%f**" % r[k]

            _r = "| " + "| ".join([str(r[k]).replace('_', '_')
                                   for k in fields])
            _r += " |"
            m += [_r]

        filters_suffix = ""
        for k, v in filters.items():
            if v:
                filters_suffix += ".%s" % k

        sort_suffix = "" if sort_field is None else ".%s" % sort_field
        out_path = "results.%s%s%s.md" % (
            self.name, filters_suffix, sort_suffix)
        with open(out_path, 'w') as f:
            print("Output in '%s'" % out_path)
            print("\n".join(m), file=f)

    def cli(self, filters):
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("-sort_field", type=str)
        for f in filters:
            parser.add_argument("-%s" % f, action="store_true")

        args = parser.parse_args()
        filters_args = {
            f: getattr(args, f)
            for f in filters
        }
        self.explore_results(sort_field=args.sort_field, **filters_args)
