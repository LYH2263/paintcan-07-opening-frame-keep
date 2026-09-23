import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters
from app.engines.wall_area import wall_area
from app.modules.opening_trim import deduct_area, inner_size

def test_living_room_net():
    a = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}])
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}], 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_trim_zero_matches_legacy():
    # 留边缺省/为 0 时净面积与改造前同房同洞一致
    legacy = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}])
    trimmed = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1, "trim": 0}, {"w": 1.5, "h": 1.4, "trim": 0}])
    assert trimmed["net_m2"] == legacy["net_m2"] == 46.41
    assert trimmed["openings_m2"] == legacy["openings_m2"] == 3.99

def test_trim_shrinks_deduction():
    # 留边 0.05：内口 = 洞口 − 两侧留边
    a = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1, "trim": 0.05}])
    assert a["opening_items"][0]["inner_w"] == 0.8
    assert a["opening_items"][0]["inner_h"] == 2.0
    assert a["opening_items"][0]["deduct_m2"] == 1.6
    assert a["openings_m2"] == 1.6
    assert a["net_m2"] == 48.8

def test_inner_size_rejects_nonpositive():
    with pytest.raises(ValueError):
        inner_size(0.9, 2.1, 0.45)   # 内口宽 = 0
    with pytest.raises(ValueError):
        inner_size(0.9, 2.1, 1.2)    # 内口宽高皆负
    with pytest.raises(ValueError):
        deduct_area(1.0, 0.1, 0.06)   # 内口高 < 0

def test_wall_area_rejects_oversized_trim():
    with pytest.raises(ValueError):
        wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1, "trim": 0.5}])

def test_estimate_carries_opening_items():
    e = estimate_room(5, 4, 2.8, [{"id": 7, "kind": "door", "w": 0.9, "h": 2.1, "trim": 0.05}], 8, 2)
    item = e["opening_items"][0]
    assert item["id"] == 7 and item["trim"] == 0.05 and item["deduct_m2"] == 1.6
    assert e["net_m2"] == 48.8
    assert e["liters"] == 12.2
