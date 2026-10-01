import unittest
from api.developer.pagination import InvalidCursor, decode_cursor, encode_cursor
from api.developer.subscriptions import SubscriptionRegistry
from packages.contracts.developer_api import ApiSubscription,SubscriptionEvent

class DeveloperApiTests(unittest.TestCase):
    def test_cursor_round_trip_and_tamper_detection(self):
        cursor=encode_cursor(42,secret="test")
        self.assertEqual(decode_cursor(cursor,secret="test"),42)
        with self.assertRaises(InvalidCursor):
            decode_cursor(cursor,secret="wrong")
    def test_subscription_requires_https(self):
        registry=SubscriptionRegistry({})
        with self.assertRaises(ValueError):
            registry.add(ApiSubscription("s","t",SubscriptionEvent.CHANGE,"changes","http://example.com/hook"))
    def test_subscription_filter(self):
        registry=SubscriptionRegistry({})
        registry.add(ApiSubscription("s","t",SubscriptionEvent.CHANGE,"changes","https://example.com/hook"))
        self.assertEqual(len(registry.active_for(SubscriptionEvent.CHANGE,"changes")),1)

if __name__=="__main__": unittest.main()
