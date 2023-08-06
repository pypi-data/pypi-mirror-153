# from keras.layers import Dense, LSTM

from bridgebots_sequence.bidding_context_features import ContextFeature, TargetHcp
from bridgebots_sequence.bidding_sequence_features import (
    CategoricalSequenceFeature, )

target = TargetHcp()
print(issubclass(target.__class__, CategoricalSequenceFeature))
print(isinstance(target, ContextFeature))

target_name = target.sequence_name if isinstance(target, ContextFeature) else target.prepared_name
print(target_name)
