#!/usr/bin/env python3
"""Sinh dữ liệu cho web app từ các tệp Markdown trong noi-dung/.

Chạy:  python3 scripts/build_data.py

Đọc:   noi-dung/*.md          (nguồn, sửa tay được)
       scripts/metadata.json  (thứ tự nhóm)
Sinh:  docs/data/doc-chat.json
"""

import hashlib
import json
import os
import re
import sys
import unicodedata

GOC = os.path.join(os.path.dirname(__file__), "..")
THU_MUC_MD = os.path.join(GOC, "noi-dung")
DICH = os.path.join(GOC, "docs", "data", "doc-chat.json")

KHOA_NGUONG = ("dieuTri", "doc", "tuVong", "docVaTuVong")


def bo_dau(chu):
    """Chuyển về chữ không dấu, chữ thường, để tìm kiếm."""
    s = unicodedata.normalize("NFD", chu.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d")


def go_nhay(g):
    g = g.strip()
    if len(g) >= 2 and g[0] == g[-1] == '"':
        return g[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return g


def doc_front_matter(dong):
    """Đọc phần YAML đơn giản ở đầu tệp. Trả về (dict, chỉ số dòng kế tiếp)."""
    if not dong or dong[0].strip() != "---":
        return {}, 0
    ket = {}
    khoa_hien = None
    i = 1
    while i < len(dong) and dong[i].strip() != "---":
        d = dong[i].rstrip("\n")
        if d.startswith("  - "):
            ket.setdefault(khoa_hien, []).append(go_nhay(d[4:]))
        elif d.startswith("  ") and ":" in d:
            k, v = d.strip().split(":", 1)
            if isinstance(ket.get(khoa_hien), dict):
                ket[khoa_hien][k.strip()] = go_nhay(v)
        elif ":" in d:
            k, v = d.split(":", 1)
            khoa_hien = k.strip()
            v = v.strip()
            if v == "":
                ket[khoa_hien] = {} if khoa_hien in KHOA_NGUONG else []
            elif v == "[]":
                ket[khoa_hien] = []
            else:
                ket[khoa_hien] = go_nhay(v)
        i += 1
    return ket, i + 1


def doc_than(dong):
    """Tách phần thân thành các mục theo tiêu đề ## ."""
    muc = {}
    ten = None
    for d in dong:
        d = d.rstrip("\n")
        if d.startswith("## "):
            ten = d[3:].strip()
            muc[ten] = []
        elif d.startswith("# "):
            ten = None
        elif ten is not None:
            muc[ten].append(d)
    return {k: [x for x in v] for k, v in muc.items()}


def tach_muc_long_nhau(dong):
    """Chuyển danh sách gạch đầu dòng thành cây hai cấp."""
    ra = []
    for d in dong:
        if not d.strip():
            continue
        m = re.match(r"^(\s*)-\s+(.*)$", d)
        if not m:
            ra.append({"chu": d.strip(), "con": []})
            continue
        cap = len(m.group(1)) // 2
        muc = {"chu": m.group(2).strip(), "con": []}
        if cap > 0 and ra:
            ra[-1]["con"].append(muc)
        else:
            ra.append(muc)
    return ra


def doc_bang(dong):
    """Đọc các bảng Markdown liên tiếp."""
    bang, hien = [], None
    for d in dong:
        d = d.strip()
        if d.startswith("|"):
            o = [x.strip() for x in d.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", x) for x in o):
                continue
            if hien is None:
                hien = {"dau": o, "hang": []}
            else:
                hien["hang"].append(o)
        elif hien is not None:
            bang.append(hien)
            hien = None
    if hien is not None:
        bang.append(hien)
    return bang


def doc_mot_chat(duong_dan):
    with open(duong_dan, encoding="utf-8") as f:
        dong = f.read().split("\n")
    fm, i = doc_front_matter(dong)
    than = doc_than(dong[i:])

    nguong = {}
    for k in KHOA_NGUONG:
        g = fm.get(k)
        if isinstance(g, dict) and g.get("giaTri"):
            nguong[k] = {"nhan": g.get("nhan", ""), "giaTri": g["giaTri"]}

    chat = {
        "slug": fm.get("slug", ""),
        "ten": fm.get("ten", ""),
        "nhom": fm.get("nhom", ""),
        "nhan": fm.get("nhan") or [],
        "tenKhac": fm.get("tenKhac") or [],
        "donVi": fm.get("donVi", ""),
        "nguong": nguong,
        "noiDung": tach_muc_long_nhau(than.get("Nội dung", [])),
        "lieu": [x.strip()[2:].strip() for x in than.get("Liều", []) if x.strip()],
        "bang": doc_bang(than.get("Bảng", [])),
        "tltk": [x.strip()[2:].strip() for x in than.get("Tài liệu tham khảo", [])
                 if x.strip()],
        "tepGoc": fm.get("tepGoc", ""),
    }
    if fm.get("hinh"):
        chat["hinh"] = fm["hinh"]
    if fm.get("ghiChu"):
        chat["ghiChu"] = fm["ghiChu"]

    # chuỗi dùng để tìm kiếm không dấu
    kho = [chat["ten"], chat["nhom"]] + chat["nhan"] + chat["tenKhac"]
    kho += [m["chu"] for m in chat["noiDung"]]
    kho += [c["chu"] for m in chat["noiDung"] for c in m["con"]]
    kho += chat["lieu"]
    kho += [g["nhan"] + " " + g["giaTri"] for g in nguong.values()]
    chat["timKiem"] = bo_dau(" ".join(kho))
    chat["timTen"] = bo_dau(" ".join([chat["ten"]] + chat["tenKhac"]))
    return chat


def main():
    with open(os.path.join(os.path.dirname(__file__), "metadata.json"),
              encoding="utf-8") as f:
        meta = json.load(f)

    tep = sorted(t for t in os.listdir(THU_MUC_MD) if t.endswith(".md"))
    cac_chat = [doc_mot_chat(os.path.join(THU_MUC_MD, t)) for t in tep]

    thu_tu = {n: i for i, n in enumerate(meta["nhomTheoThuTu"])}
    la = [c for c in cac_chat if c["nhom"] not in thu_tu]
    if la:
        print("Nhóm lạ:", {c["ten"]: c["nhom"] for c in la}, file=sys.stderr)
        return 1
    cac_chat.sort(key=lambda c: (thu_tu[c["nhom"]], bo_dau(c["ten"])))

    nhan = sorted({n for c in cac_chat for n in c["nhan"]}, key=bo_dau)
    du_lieu = {
        "tieuDe": "Sổ tay Độc chất học trong Giám định pháp y",
        "tacGia": "ThS.BS. Âu Dương Quốc Uy",
        "soChat": len(cac_chat),
        "nhom": [n for n in meta["nhomTheoThuTu"]
                 if any(c["nhom"] == n for c in cac_chat)],
        "nhan": nhan,
        "chat": cac_chat,
    }
    noi_dung = json.dumps(du_lieu, ensure_ascii=False, separators=(",", ":"))
    du_lieu["phienBan"] = hashlib.sha1(noi_dung.encode()).hexdigest()[:10]

    os.makedirs(os.path.dirname(DICH), exist_ok=True)
    with open(DICH, "w", encoding="utf-8") as f:
        json.dump(du_lieu, f, ensure_ascii=False, separators=(",", ":"))

    # cập nhật mã phiên bản trong service worker để máy người dùng tải bản mới
    sw = os.path.join(GOC, "docs", "sw.js")
    if os.path.exists(sw):
        with open(sw, encoding="utf-8") as f:
            noi = f.read()
        noi = re.sub(r'const PHIEN_BAN = "[^"]*"',
                     f'const PHIEN_BAN = "{du_lieu["phienBan"]}"', noi)
        with open(sw, "w", encoding="utf-8") as f:
            f.write(noi)

    kb = os.path.getsize(DICH) / 1024
    print(f"Đã sinh {DICH} — {len(cac_chat)} chất, {kb:.0f} KB, "
          f"phiên bản {du_lieu['phienBan']}")
    print(f"{len(du_lieu['nhom'])} nhóm, {len(nhan)} nhãn")
    return 0


if __name__ == "__main__":
    sys.exit(main())
