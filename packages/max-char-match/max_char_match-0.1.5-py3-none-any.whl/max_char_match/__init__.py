""" MaxCharMatch metric. """

import datetime
import os
import string
from dataclasses import dataclass
from typing import Dict, List, Tuple

import datasets
import diff_match_patch as dmp_module
import numpy as np
from more_itertools import chunked
from tqdm import tqdm

from max_char_match.alignment import SpellAlignment

_CITATION = """\
@misc{havens2019mcm,
    title  = {MaxCharMatch metric},
    author = {Sam Havens, Aneta Melisa Stal},
    year   = {2021}
}
"""

_DESCRIPTION = """\
MaxCharMatch metric is adaptation of MaxMatch (M^2) metrics (https://github.com/nusnlp/m2scorer) for spelling.
"""

_KWARGS_DESCRIPTION = """
Compute MaxCharMatch.
Args:
    predictions: list of predictions to score.
    references: list of references.
Returns:
    "tp": True Positive Count
    "fp": False Positive Count
    "fn": False Negative Count
    "precision": Precision
    "recall": Recall
    "F05": F0.5
Examples:
    >>> mcm_metric = datasets.load_metric("mcm.py")
    >>> mcm_metric._load_data(["Thiz si cool"], ["This is cool"])
    >>> mcm_metric._save_to(path/to/some/dir)
    >>> mcm_metric.compute(predictions=["This si cools"], references=["This is cool"])
    {'tp': 2, 'fp': 2, 'fn': 2, 'precision': 0.5, 'recall': 0.5, 'f05': 0.5}
"""


@dataclass
class EvalExample:
    sentence: str
    norm_form: str = ""

    def __post_init__(self):
        self.norm_form = self.normalize_sentence(sentence)

    @staticmethod
    def normalize_sentence(sent: str) -> str:
        sent = sent.strip().lower()
        return sent.translate(str.maketrans("", "", string.punctuation))

    @staticmethod
    def label_sentence(sent: str) -> str:
        return sent


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MaxCharMatch(datasets.Metric):
    def __init__(self, *args, **kwargs):
        super(MaxCharMatch, self).__init__(*args, **kwargs)
        self.sa = SpellAlignment()
        self.save = False
        self.tokenizer = None
        self.batch_size = 16
        self.origs = []
        self.cors = []

    @staticmethod
    def normalize_sentence(sent: str) -> str:
        sent = sent.strip().lower()
        return sent.translate(str.maketrans("", "", string.punctuation))

    def convert_to_text(self, inputs) -> List[str]:
        text = []
        num_batches = int(len(inputs) / self.batch_size)
        for chunk in tqdm(chunked(inputs, self.batch_size), total=num_batches):
            text += self.tokenizer.batch_decode(
                chunk,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True,
            )
        return text

    def generator_to_text(self, inputs_generator) -> Tuple[List[str], List[str]]:
        inputs = []
        references = []
        for i in tqdm(range(len(inputs_generator))):
            sample = inputs_generator[i]
            inputs.append(sample["input_ids"])
            references.append(sample["labels"])
        inputs_text = self.convert_to_text(inputs)
        references_text = self.convert_to_text(references)
        return inputs_text, references_text

    def _load_from_generator(self, data_generator) -> None:
        self.tokenizer = data_generator.tokenizer
        self.origs, self.cors = self.generator_to_text(data_generator)

    def _load_data(self, origs: List[str], cors: List[str]):
        self.origs = origs
        self.cors = cors

    def _save_to(self, output_dir: str) -> None:
        self.save = True
        self.dmp = dmp_module.diff_match_patch()
        self.output_dir = os.path.join(output_dir, "eval_outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string"),
                    "references": datasets.Value("string"),
                }
            ),
            codebase_urls=[],
            reference_urls=[],
            format="numpy",
        )

    def compare_edits(self, orig: str, cor: str, pred: str) -> Tuple[int, int, int]:
        orig = self.normalize_sentence(orig)
        cor = self.normalize_sentence(cor)
        pred = self.normalize_sentence(pred)

        pred_edits = self.sa(orig, pred)
        ref_edits = self.sa(orig, cor)

        tp = len([pred_edit for pred_edit in pred_edits if pred_edit in ref_edits])
        fp = len(pred_edits) - tp
        fn = len([ref_edit for ref_edit in ref_edits if ref_edit not in pred_edits])

        return tp, fp, fn

    def get_html_diff(self, sent1: str, sent2: str) -> str:
        diff = self.dmp.diff_main(sent1, sent2)
        self.dmp.diff_cleanupSemantic(diff)
        return self.dmp.diff_prettyHtml(diff)

    def _compute(
        self, predictions: List[str], references: List[str]
    ) -> Dict[str, float]:
        tp_agg, fp_agg, fn_agg = 0, 0, 0

        f_out = None

        if self.save:
            f_name = os.path.join(
                self.output_dir,
                datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S") + ".html",
            )
            f_out = open(f_name, "w", encoding="utf8")

        for o, c, p in tqdm(
            zip(self.origs, self.cors, predictions), total=len(self.origs)
        ):
            tp, fp, fn = self.compare_edits(o, c, p)
            tp_agg += tp
            fp_agg += fp
            fn_agg += fn

            if f_out:
                f_out.write(self.get_html_diff(o, c) + "<br>\n")
                f_out.write(self.get_html_diff(o, p) + "<br><br>\n\n")
        if self.save:
            f_out.close()

        precision = tp_agg / (fp_agg + tp_agg) if fp_agg * tp_agg else 0
        recall = tp_agg / (tp_agg + fn_agg) if tp_agg * fn_agg else 0
        f05 = (
            1.25 * precision * recall / (0.25 * precision + recall)
            if precision * recall
            else 0
        )
        f2 = (
            (5 * precision * recall) / (4 * precision + recall)
            if precision * recall
            else 0
        )

        return {
            "tp": tp_agg,
            "fp": fp_agg,
            "fn": fn_agg,
            "precision": precision,
            "recall": recall,
            "f05": f05,
            "f2": f2,
        }
