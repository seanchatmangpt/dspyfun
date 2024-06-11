"""

"""
import dspy
from dspygen.utils.dspy_tools import init_dspy


deal = {"dealTerms": "2 month free, after that 10% discount for 3 month"}

invoice = [{
      "invoiceTerms": "Free month 2 of 2",
      "invoiceLineDescription": "Free month 2 of 2",
      "priceChangePercent": "-100",
      "priceChangeAmount": "0"
   },
   {
      "invoiceTerms": "35% increase month 3 of 6",
      "invoiceLineDescription": "35% increase month 3 of 6",
      "priceChangePercent": "35",
      "priceChangeAmount": "0"
   }]


class SplitDealTerms(dspy.Signature):
    """split the deal_terms to the terms relevant for each month"""

    deal_terms: str = dspy.InputField(desc="Deal terms to be split")
    invoice_period1: str = dspy.OutputField(desc="invoice period 1 terms")
    invoice_period2: str = dspy.OutputField(desc="invoice period 2 terms")
    invoice_period3: str = dspy.OutputField(desc="invoice period 3 terms")
    invoice_period4: str = dspy.OutputField(desc="invoice period 4 terms")
    invoice_period5: str = dspy.OutputField(desc="invoice period 5 terms")
    invoice_period6: str = dspy.OutputField(desc="invoice period 6 terms")
    invoice_period7: str = dspy.OutputField(desc="invoice period 7 terms")
    invoice_period8: str = dspy.OutputField(desc="invoice period 8 terms")
    invoice_period9: str = dspy.OutputField(desc="invoice period 9 terms")
    invoice_period10: str = dspy.OutputField(desc="invoice period 10 terms")
    invoice_period11: str = dspy.OutputField(desc="invoice period 11 terms")
    invoice_period12: str = dspy.OutputField(desc="invoice period 12 terms")


class DealTermSplitModule(dspy.Module):
    """DealTermSplitModule"""

    def __init__(self, **forward_args):
        super().__init__()
        self.forward_args = forward_args
        self.output = None

    def forward(self, deal_terms):
        pred = dspy.ChainOfThought(SplitDealTerms)
        self.output = pred(deal_terms=deal_terms)
        return self.output


def deal_term_split_call(deal_terms):
    deal_term_split = DealTermSplitModule()
    return deal_term_split.forward(deal_terms=deal_terms)


def main():
    init_dspy()
    deal_terms = ""
    result = deal_term_split_call(deal_terms=deal_terms)
    print(result)


if __name__ == "__main__":
    main()