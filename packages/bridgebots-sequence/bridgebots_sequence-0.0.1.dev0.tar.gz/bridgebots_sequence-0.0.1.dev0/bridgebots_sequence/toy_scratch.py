import pickle
from collections import defaultdict

from bridgebots.bids import LEGAL_BIDS

with open("/Users/frice/bridge/bid_learn/deals/no_duplicates_train.pickle", "rb") as no_duplicates:
    deal_records = pickle.load(no_duplicates)
    bid_counts = defaultdict(int)
    for i, deal_record in enumerate(deal_records):
        for board_record in deal_record.board_records:
            for bid in board_record.bidding_record:
                bid_counts[bid] += 1
            bid_counts["EOS"] += 1


for bid in [] + LEGAL_BIDS + ["EOS"]:
    print(bid, bid_counts[bid])
