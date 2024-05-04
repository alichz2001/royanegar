from time import sleep

import user_slug_aggregator
import user_aggregator
import slug_aggregator
import user_slug_state_aggregator

if __name__ == "__main__":
    while True:
        user_slug_aggregator.aggregate()
        user_aggregator.aggregate()
        slug_aggregator.aggregate()
        user_slug_state_aggregator.aggregate()
        sleep(5)