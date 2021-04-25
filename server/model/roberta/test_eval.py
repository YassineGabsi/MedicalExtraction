from eval import eval
from config import NEW_MODEL_PATH


def test_performance():

    """
    Tests if results are logical or not and guarentees model accuracy
    """

    top1_performance , top3_performance = eval(NEW_MODEL_PATH)

    assert top1_performance < 1 and top1_performance > 0 
    assert top3_performance <1 and top3_performance > 0
    assert top1_performance > 0.5 and top3_performance > 0.7 