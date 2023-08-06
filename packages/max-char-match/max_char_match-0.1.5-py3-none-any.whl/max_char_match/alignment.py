"""
This code comes partially from https://github.com/chrisjbryant/errant/blob/master/errant/alignment.py
"""
import re
from dataclasses import dataclass, field
from itertools import groupby


@dataclass
class CharSpan:
    start: int
    end: int
    sent: str = field(repr=False, compare=False)
    text: str = field(default="")

    def __post_init__(self):
        self.text = self.sent[self.start : self.end]


class CharDiff:
    def __init__(self, orig, cor, op):
        self.err_span = CharSpan(op[0], op[1], orig)
        self.cor_span = CharSpan(op[2], op[3], cor)

    def __str__(self):
        return f"'{self.err_span.text}' -> '{self.cor_span.text}'"

    def __eq__(self, other):
        if self.err_span != other.err_span:
            return False
        if self.cor_span != other.cor_span:
            return False
        return True

    def is_del(self):
        return len(self.err_span.text) and not len(self.cor_span.text)


class SpellAlignment:

    qwerty = "1234567890-=qwertyuiop[]asdfghjkl;' zxcvbnm,./"
    qwerty_dict = {k: i for i, k in enumerate(list(qwerty)) if k != " "}

    def __init__(self):
        self.only_letters = re.compile(r"[^a-zA-Z\s]")

    def __call__(self, orig: str, cor: str):
        """
        Input:
        - orig: original sent
        - cor: corrected sent
        """
        self.orig = orig
        self.cor = cor

        # Align orig and cor and get the cost and op matrices
        self.cost_matrix, self.op_matrix = self.align()

        # Get the cheapest align sequence from the op matrix
        self.align_seq = self.get_cheapest_align_seq()

        return self.get_all_merge_edits()

    @staticmethod
    def is_left_border(char):
        return char in ["1", "q", "a", "z"]

    @staticmethod
    def is_right_border(char):
        return char in ["=", "]", "'", "?"]

    def is_keyboard_neighbor(self, a, b):

        if a not in self.qwerty:
            return False

        if b not in self.qwerty:
            return False

        if not self.is_left_border(a):
            if self.qwerty_dict[a] - self.qwerty_dict[b] == 1:
                return True
            if abs(self.qwerty_dict[a] - self.qwerty_dict[b]) == 11:
                return True

        if not self.is_right_border(a):
            if self.qwerty_dict[a] - self.qwerty_dict[b] == -1:
                return True
            if abs(self.qwerty_dict[a] - self.qwerty_dict[b]) == 12:
                return True

        if self.is_left_border(a):
            if self.qwerty_dict[a] - self.qwerty_dict[b] == 11:
                return True

        if self.is_right_border(a):
            if self.qwerty_dict[a] - self.qwerty_dict[b] == 12:
                return True

        return False

    def align(self):
        """
        Returns:
        - cost matrix and the
        - operation matrix of the alignment
        """
        o_len = len(self.orig)
        c_len = len(self.cor)

        o_low = list(self.orig.lower())
        c_low = list(self.cor.lower())

        cost_matrix = [[0.0 for j in range(c_len + 1)] for i in range(o_len + 1)]
        op_matrix = [["O" for j in range(c_len + 1)] for i in range(o_len + 1)]

        for i in range(1, o_len + 1):
            cost_matrix[i][0] = cost_matrix[i - 1][0] + 1
            op_matrix[i][0] = "D"
        for j in range(1, c_len + 1):
            cost_matrix[0][j] = cost_matrix[0][j - 1] + 1
            op_matrix[0][j] = "I"

        for i in range(o_len):
            for j in range(c_len):
                # Matches
                if self.orig[i] == self.cor[j]:
                    cost_matrix[i + 1][j + 1] = cost_matrix[i][j]
                    op_matrix[i + 1][j + 1] = "M"
                # Non-matches
                else:
                    del_cost = cost_matrix[i][j + 1] + 1
                    ins_cost = cost_matrix[i + 1][j] + 1
                    trans_cost = float("inf")
                    # Custom substitution
                    sub_cost = cost_matrix[i][j] + self.get_sub_cost(
                        self.orig[i], self.cor[j]
                    )
                    # Transpositions require >=2 tokens
                    # Traverse the diagonal while there is not a Match.
                    k = 1
                    while (
                        i - k >= 0
                        and j - k >= 0
                        and cost_matrix[i - k + 1][j - k + 1]
                        != cost_matrix[i - k][j - k]
                    ):
                        if sorted(o_low[i - k : i + 1]) == sorted(c_low[j - k : j + 1]):
                            trans_cost = cost_matrix[i - k][j - k] + k
                            break
                        k += 1

                    # Costs
                    costs = [trans_cost, sub_cost, ins_cost, del_cost]
                    # Get the index of the cheapest (first cheapest if tied)
                    l = costs.index(min(costs))
                    # Save the cost and the op in the matrices
                    cost_matrix[i + 1][j + 1] = costs[l]
                    if l == 0:
                        op_matrix[i + 1][j + 1] = "T" + str(k + 1)
                    elif l == 1:
                        op_matrix[i + 1][j + 1] = "S"
                    elif l == 2:
                        op_matrix[i + 1][j + 1] = "I"
                    else:
                        op_matrix[i + 1][j + 1] = "D"
        return cost_matrix, op_matrix

    def get_sub_cost(self, o, c):
        """
        o - input char
        c - output char
        Returns:
            char cost between 0 < x < 2
        """
        # Short circuit if the only difference is case
        if o.lower() == c.lower():
            return 0

        # If space to not space: dissimilar
        if (o == " " and c != o) or (c == " " and o != c):
            return 2
        # If alpha to non alpha: dissimilar
        if self.is_nonalpha(o) and not self.is_nonalpha(c):
            return 2
        if self.is_nonalpha(c) and not self.is_nonalpha(o):
            return 2

        # Fat finger
        if self.is_keyboard_neighbor(c, o):
            return 0.5

        return 1

    def is_nonalpha(self, flagged_text: str):
        non_letters = self.only_letters.findall(flagged_text)
        return non_letters != []

    def get_cheapest_align_seq(self):
        """
        Get the cheapest alignment sequence and indices from the op matrix
        D - deletions, I - insertions, S - substitutions, M - matching
        """
        i = len(self.op_matrix) - 1
        j = len(self.op_matrix[0]) - 1
        align_seq = []
        while i + j != 0:

            op = self.op_matrix[i][j]
            if op in {"M", "S"}:
                align_seq.append((op, i - 1, i, j - 1, j))
                i -= 1
                j -= 1
            elif op == "D":
                align_seq.append((op, i - 1, i, j, j))
                i -= 1
            elif op == "I":
                align_seq.append((op, i, i, j - 1, j))
                j -= 1
            else:
                k = int(op[1:])
                align_seq.append((op, i - k, i, j - k, j))
                i -= k
                j -= k
        align_seq.reverse()
        return align_seq

    def edit_to_type(self, edit):
        """
        P (pass) - M or punct
        W (word correction) - not P and not space
        """
        is_matched = edit[0] == "M"

        edit_type = "W"

        if is_matched:
            edit_type = "P"

        return edit_type

    def get_all_merge_edits(self):
        """
        Merge all adjacent non-match ops
        accept punct-punct corrections but leave out other-punct
        spelling can't add, remove or replace by something else purely punct tokens
        """
        edits = []
        for op, group in groupby(self.align_seq, lambda x: self.edit_to_type(x)):
            if op != "P":
                merged = self.merge_edits(list(group))
                edits.append(CharDiff(self.orig, self.cor, merged[0][1:]))
        return edits

    def merge_edits(self, seq):
        """
        Merge the input alignment sequence to a single edit span
        """
        if seq:
            return [("X", seq[0][1], seq[-1][2], seq[0][3], seq[-1][4])]
        else:
            return seq


if __name__ == "__main__":

    sa = SpellAlignment()
    orig = "thiz is hutright, ro no!"
    cor = "this is hot right, or not?"
    edits = sa(orig, cor)
    for e in edits:
        print(e)
