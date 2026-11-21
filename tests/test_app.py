"""ランダム病気（randomdisease）のテスト。

外部通信は行わず、内蔵データと Flask テストクライアントで検証する。
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module  # noqa: E402

SAMPLE = {
    "name": "テスト病",
    "category": "テスト分類",
    "overview": "これはテスト用の概要です。",
    "symptoms": "テスト症状A、テスト症状B",
    "cause": "テスト原因です。",
    "points": "テストポイントです。",
    "url": "https://ja.wikipedia.org/wiki/テスト病",
}


class RandomDiseaseTest(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()
        self._orig_fetch = app_module.fetch_random_disease

    def tearDown(self):
        app_module.fetch_random_disease = self._orig_fetch

    def test_healthz(self):
        res = self.client.get("/healthz")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")

    def test_index_ok(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn("ランダム病気", body)
        self.assertIn("ランダムで病気を表示", body)
        self.assertIn("診断や治療の代わりにはなりません", body)

    def test_random_success(self):
        app_module.fetch_random_disease = lambda: dict(SAMPLE)
        res = self.client.get("/random")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn("テスト病", body)
        self.assertIn("テスト分類", body)
        self.assertIn("これはテスト用の概要です。", body)
        self.assertIn("テスト症状A", body)
        self.assertIn("テスト原因です。", body)
        self.assertIn("テストポイントです。", body)
        self.assertIn("https://ja.wikipedia.org/wiki/テスト病", body)
        self.assertIn("Wikipediaで詳しく見る", body)

    def test_random_real_data_has_all_fields(self):
        res = self.client.get("/random")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn("概要", body)
        self.assertIn("主な症状", body)
        self.assertIn("原因", body)
        self.assertIn("一般的なポイント", body)

    def test_dataset_size_and_uniqueness(self):
        diseases = app_module.DISEASES
        self.assertEqual(len(diseases), 60)
        names = [d["name"] for d in diseases]
        self.assertEqual(len(names), len(set(names)))

    def test_dataset_fields_complete(self):
        for d in app_module.DISEASES:
            for key in ("name", "category", "overview", "symptoms",
                        "cause", "points", "url"):
                self.assertTrue(d[key], (d.get("name"), key))
            self.assertTrue(
                d["url"].startswith("https://ja.wikipedia.org/wiki/"),
                d["name"],
            )

    def test_fetch_returns_copy_from_dataset(self):
        one = app_module.fetch_random_disease()
        self.assertIn(one["name"], [d["name"] for d in app_module.DISEASES])
        one["name"] = "書き換え"
        self.assertNotIn(
            "書き換え", [d["name"] for d in app_module.DISEASES]
        )


if __name__ == "__main__":
    unittest.main()
