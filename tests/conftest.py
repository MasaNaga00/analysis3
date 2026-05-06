"""
conftest.py
===========
pytest 全体で使う共通fixture。
合成データはすべて実データ（R001〜R018相当）のパターンを反映している。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def _make_record(
    repair_id: str,
    product_type: str = "ML",
    user_comment: str = "",
    repair_comment: str = "",
    internal_1: str = "",
    internal_2: str = "",
) -> dict:
    """1レコードを辞書として生成。"""
    return {
        "repair_id": repair_id,
        "product_type": product_type,
        "user_comment": user_comment,
        "repair_comment": repair_comment,
        "internal_1": internal_1,
        "internal_2": internal_2,
    }


@pytest.fixture
def sample_records_no_markers() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R001",
            user_comment="冬場の屋外撮影でピントが合わなくなります",
            repair_comment="低温環境下でのAF動作不良を確認、AFユニット交換にて復旧",
            internal_1="共通情報1",
        ),
        _make_record(
            repair_id="R002", product_type="LENS",
            user_comment="ズームが固い",
            repair_comment="ズームリング洗浄",
        ),
    ])


@pytest.fixture
def sample_records_well_formed_split() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R101",
            user_comment="①AFが効きません ②シャッターも切れません",
            repair_comment="①AFユニット交換 ②シャッターブロック交換",
            internal_1="顧客優先",
        ),
        _make_record(
            repair_id="R102",
            user_comment="①シャッター切れず ②画像にノイズ ③LCDムラ",
            repair_comment="①シャッターユニット交換 ②センサー清掃 ③LCD交換",
        ),
    ])


@pytest.fixture
def sample_records_marker_mismatch() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R201",
            user_comment="①ピント不良 ②電源不安定",
            repair_comment="①AF調整実施",
        ),
        _make_record(
            repair_id="R202",
            user_comment="①AF不良 ②シャッター異音 ③LCDノイズ",
            repair_comment="①AF調整 ②清掃のみ",
        ),
    ])


@pytest.fixture
def sample_records_one_marker_only() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R301",
            user_comment="①AFが効きません",
            repair_comment="①AF調整実施",
        ),
    ])


@pytest.fixture
def sample_records_fallback() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R401",
            user_comment="(1)AF不良 (2)電源不良",
            repair_comment="(1)AF調整 (2)電池接点清掃",
        ),
    ])


@pytest.fixture
def sample_records_empty() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(repair_id="R501"),
        _make_record(
            repair_id="R502",
            user_comment="",
            repair_comment=None,
        ),
    ])


@pytest.fixture
def sample_records_abnormal_split() -> pd.DataFrame:
    return pd.DataFrame([
        _make_record(
            repair_id="R601",
            user_comment="①A ②B ③C ④D ⑤E ⑥F ⑦G ⑧H",
            repair_comment="①修A ②修B ③修C ④修D ⑤修E ⑥修F ⑦修G ⑧修H",
        ),
    ])


@pytest.fixture
def sample_records_with_preamble() -> pd.DataFrame:
    """preamble（マーカー前のフリーテキスト）あり。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R009",
            user_comment="【前回履歴】H111①AF ②電源 ▪️同時預かり",
            repair_comment="①AF調整 ②電池清掃",
        ),
        _make_record(
            repair_id="R012",
            user_comment="フリーズ・エラー70・ブラックアウト①エラー ②マウント板ばね破損",
            repair_comment="①現象確認できず ②破損確認",
        ),
    ])


@pytest.fixture
def sample_records_repair_preamble() -> pd.DataFrame:
    """修理者にpreambleあり。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R013",
            user_comment="【ショック品】【オーバホール】①エラー ②マウント板ばね破損",
            repair_comment="オーバーホールを実施いたしました ①現象確認できず ②破損確認",
        ),
    ])


@pytest.fixture
def sample_records_user_brackets_in_marker_zone() -> pd.DataFrame:
    """マーカーゾーン内の【】（ユーザコメントは除去）。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R014",
            user_comment="①AF 【ご指摘外の現象】②電源 【追加ご指摘】③シャッター 【修理時に発見しました】④外装ラバー劣化",
            repair_comment="①AF調整 ②電池清掃 ③シャッター交換 ④外装ラバー交換",
        ),
    ])


@pytest.fixture
def sample_records_grouped_markers() -> pd.DataFrame:
    """連続マーカー（①②）まとめ回答。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R015",
            user_comment="①AF ②電源",
            repair_comment="①②ご指摘の現象確認",
        ),
        _make_record(
            repair_id="R017",
            user_comment="①レンズ接点 ②電源",
            repair_comment="①②レンズ側にて対応します。カメラには異常なし",
        ),
    ])


@pytest.fixture
def sample_records_mixed_grouped() -> pd.DataFrame:
    """連続マーカーと単独マーカーの混在。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R016",
            user_comment="①レンズ接点 ②電源 ③シャッター ④LCD ⑤画像 ⑥音声 ⑦動画",
            repair_comment="①②レンズ側にて対応 ③④⑤⑥⑦ご指摘外の現象",
        ),
    ])


@pytest.fixture
def sample_records_duplicate_markers() -> pd.DataFrame:
    """文中で同じ番号が複数回出現。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R018",
            user_comment="メンテを依頼したが、①AF ②電源 ③雨の中で撮影",
            repair_comment="①②ご指摘の現象確認できませんでしたが③により発生した可能性が考えられる。③内部の腐食確認",
        ),
    ])


@pytest.fixture
def sample_records_postamble() -> pd.DataFrame:
    """postamble（後置き情報）あり。"""
    return pd.DataFrame([
        _make_record(
            repair_id="R011",
            user_comment="【前回履歴】H111①AF ②電源 ※同時預かり",
            repair_comment="①AF調整 ②電池清掃 ※同時預かり",
        ),
    ])


@pytest.fixture
def sample_records_custom_columns() -> pd.DataFrame:
    """カラム名がデフォルトと異なるDataFrame。"""
    return pd.DataFrame([
        {
            "id": "X001",
            "category": "ML",
            "user_text_jp": "①AF不良 ②電源不良",
            "repair_text_jp": "①AF調整 ②電池清掃",
            "memo1": "メモ1",
            "memo2": "メモ2",
        }
    ])
