"""门窗框留边模块：开洞除宽高外可带留边宽度 trim（缺省 0）。

扣除面积按内口宽高计算：内口 = 洞口尺寸 − 两侧留边。
留边为 0 时内口即洞口，净面积与改造前同房同洞一致。
内口宽或高算后不大于 0 时抛 ValueError，由上层整单拒绝且不写记录。
"""

def inner_size(w, h, trim=0.0):
    """返回 (内口宽, 内口高, 留边)；内口宽或高 <= 0 抛 ValueError。"""
    w, h, trim = float(w), float(h), float(trim or 0.0)
    inner_w = w - 2.0 * trim
    inner_h = h - 2.0 * trim
    if inner_w <= 0.0 or inner_h <= 0.0:
        raise ValueError(f"opening inner size must be positive, got {inner_w} x {inner_h}")
    return inner_w, inner_h, trim

def deduct_area(w, h, trim=0.0):
    """单洞扣除面积 = 内口宽 × 内口高。"""
    inner_w, inner_h, _ = inner_size(w, h, trim)
    return inner_w * inner_h
