# -*- coding: utf-8 -*-

from ideabox.policy.faceted import subscriber
from unittest import mock

import unittest


class TestRandomizer(unittest.TestCase):
    @mock.patch("time.time", mock.Mock(return_value=1546380000.0))
    def test_cache_key_basic(self):
        # 2019-01-01 23:00
        self.assertEqual(
            ("generator", 35795.0), subscriber._cache_key("function", "generator")
        )

    @mock.patch("time.time", mock.Mock(side_effect=(1546300740.0, 1546300800.0)))
    def test_cache_key_night_change(self):
        # 2019-01-01 00:59 and 2019-01-01 01:00
        self.assertEqual(
            ("generator", 35793.0), subscriber._cache_key("function", "generator")
        )
        self.assertEqual(
            ("generator", 35794.0), subscriber._cache_key("function", "generator")
        )

    @mock.patch("time.time", mock.Mock(side_effect=(1546343940.0, 1546344000.0)))
    def test_cache_key_noon_change(self):
        # 2019-01-01 12:59 and 2019-01-01 13:00
        self.assertEqual(
            ("generator", 35794.0), subscriber._cache_key("function", "generator")
        )
        self.assertEqual(
            ("generator", 35795.0), subscriber._cache_key("function", "generator")
        )

    def test_cache_key_generator(self):
        self.assertEqual(
            "0cc175b9c0f1b6a831c399e269772661",
            subscriber.random_key_generator("a"),
        )

    def test_random_sort(self):
        request = type("request", (object,), {"cookies": {"__ac": "a"}})()
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="aa"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_1", randomizer.random_sort_key)
            self.assertEqual("descending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="bb"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_2", randomizer.random_sort_key)
            self.assertEqual("ascending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="ab"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_1", randomizer.random_sort_key)
            self.assertEqual("ascending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="cc"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_3", randomizer.random_sort_key)
            self.assertEqual("descending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="dd"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_4", randomizer.random_sort_key)
            self.assertEqual("ascending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="ee"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_5", randomizer.random_sort_key)
            self.assertEqual("descending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="ff"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_6", randomizer.random_sort_key)
            self.assertEqual("ascending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="gg"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("project_random_7", randomizer.random_sort_key)
            self.assertEqual("descending", randomizer.random_sort_order)
        with mock.patch(
            "ideabox.policy.faceted.subscriber.random_key_generator", return_value="hh"
        ):
            randomizer = subscriber.Randomizer(request)
            self.assertEqual("UID", randomizer.random_sort_key)
            self.assertEqual("ascending", randomizer.random_sort_order)
