import json
from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self): return settings.get_map(self._c)
    def set_opening_trim(self, opening_id, trim):
        trim = float(trim)
        if trim < 0: raise ValueError("trim must be >= 0")
        if not openings.set_trim(self._c, opening_id, trim): return None
        return openings.get(self._c, opening_id)
    def _parse_run(self, row):
        row = dict(row)
        row["input"] = json.loads(row.pop("input_json") or "{}")
        row["result"] = json.loads(row.pop("result_json") or "{}")
        return row
    def history(self, limit=50):
        return [self._parse_run(r) for r in runs.list_recent(self._c, limit)]
    def run_detail(self, run_id):
        r = runs.get(self._c, run_id)
        return self._parse_run(r) if r else None
    def estimate(self, room_id, persist, coats=None, coverage=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings.coverage_coats(self._c)
        cov = float(coverage or cov)
        ct = int(coats or ct)
        ops = [{"id": o["id"], "kind": o["kind"], "w": o["w"], "h": o["h"], "trim": o.get("trim") or 0}
               for o in detail["openings"]]
        # 内口宽高 <= 0 时引擎抛 ValueError：整单拒绝，不写任何记录
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct)
        # 钉选：洞口快照（含留边）随输入入档，各洞扣除面积/净面积/升数随结果入档
        payload = {"room_id": room_id, "coats": ct, "coverage": cov, "openings": ops}
        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
