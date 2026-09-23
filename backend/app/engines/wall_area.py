from app.modules.opening_trim import inner_size

def wall_area(length: float, width: float, height: float, openings: list[dict]) -> dict:
    walls = 2 * (float(length) + float(width)) * float(height)
    items = []
    hole = 0.0
    for o in openings:
        inner_w, inner_h, trim = inner_size(o["w"], o["h"], o.get("trim"))
        deduct = inner_w * inner_h
        hole += deduct
        items.append({
            "id": o.get("id"),
            "kind": o.get("kind"),
            "w": round(float(o["w"]), 3),
            "h": round(float(o["h"]), 3),
            "trim": round(trim, 3),
            "inner_w": round(inner_w, 3),
            "inner_h": round(inner_h, 3),
            "deduct_m2": round(deduct, 2),
        })
    net = max(0.0, walls - hole)
    return {"gross_m2": round(walls, 2), "openings_m2": round(hole, 2),
            "net_m2": round(net, 2), "opening_items": items}
