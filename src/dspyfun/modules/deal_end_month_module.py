from pydantic import BaseModel, Field
import dspy


# Define the input and output models
class DealTermsInput(BaseModel):
    deal_terms: str = Field(description="The terms of the deal, including free and discounted periods")


class DealEndMonthOutput(BaseModel):
    end_month: int = Field(description="The month number when the deal ends")


# Define the Typed Signature
class DealEndMonthSignature(dspy.Signature):
    input: DealTermsInput = dspy.InputField()
    output: DealEndMonthOutput = dspy.OutputField()


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_dspy
    init_dspy()

    # Create the Typed Predictor
    deal_end_month_predictor = dspy.TypedPredictor(DealEndMonthSignature)

    # Example input
    deal_terms_input = DealTermsInput(deal_terms="2 months free, after that 10% discount for 3 months")

    # Get the prediction
    prediction = deal_end_month_predictor(input=deal_terms_input)

    # Access the output
    end_month = prediction.output.end_month

    print(f"The deal ends on month: {end_month}")


if __name__ == '__main__':
    main()
