#!/usr/bin/env python3
"""Trích xuất 67 tệp .docx trong thư mục "Cơ Chế" thành Markdown có cấu trúc.

Chạy:  python3 scripts/trich_xuat.py

Sinh ra:
  noi-dung/<slug>.md          nguồn Markdown cho từng chất (sửa tay được)
  docs/hinh/<slug>.png        hình nhúng trong tài liệu gốc
  ra-soat/nhat-ky-hieu-dinh.md  nhật ký mọi chỗ đã sửa so với bản gốc

Tệp .docx gốc KHÔNG bị thay đổi.
"""

import json
import os
import re
import sys
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

GOC = os.path.join(os.path.dirname(__file__), "..")
THU_MUC_DOCX = os.path.join(GOC, "Cơ Chế")
THU_MUC_MD = os.path.join(GOC, "noi-dung")
THU_MUC_HINH = os.path.join(GOC, "docs", "hinh")
NHAT_KY = os.path.join(GOC, "ra-soat", "nhat-ky-hieu-dinh.md")

# Ký hiệu Wingdings trong bản Word, chuyển về mũi tên Unicode.
KY_HIEU = {
    ("Wingdings", "F0E0"): "→",
    ("Wingdings 3", "F0DA"): "→",
    ("Wingdings 3", "00DA"): "→",
    ("Wingdings 3", "F021"): "←",
    ("Wingdings 3", "F022"): "→",
}

# ---------------------------------------------------------------- sửa lỗi

# Nhóm A và B: sửa theo từng tệp. Khóa là tên tệp .docx (không đuôi).
# Mỗi mục: (chữ gốc, chữ sửa, mã mục trong danh-sach-sua-loi.md)
SUA_THEO_TEP = {
    "PHENYTOIN": [
        ("Tỉ lệ nồng độ Olanzapine trong máu tim", "Tỉ lệ nồng độ Phenytoin trong máu tim", "A1"),
    ],
    "SILDENAFIL": [
        ("Tỉ lệ nồng độ Caffeine trong máu tim", "Tỉ lệ nồng độ Sildenafil trong máu tim", "A2"),
    ],
    "WARFARIN": [
        ("II, VII, Ĩ, X", "II, VII, IX, X", "A3"),
    ],
    "DEXTROMETHORPHAN": [
        ("ức thụ thể σ-opioid", "ức chế thụ thể σ-opioid", "B3"),
    ],
    "TETRAHYDROCANNABINOL": [
        ("nồng dộ trong máu", "nồng độ trong máu", "B4"),
        ("ghi nhận một hôn mê, vã mồ hôi", "ghi nhận một trường hợp hôn mê, vã mồ hôi", "B4"),
    ],
    "FLUCONAZOLE": [
        ("thuộc học CYP450", "thuộc họ CYP450", "B5"),
        ("Diflucan (fluconazale)", "Diflucan (fluconazole)", "B6"),
    ],
    "ACETAMINOPHEN": [
        ("chất ô xi hóa mạnh", "chất oxy hóa mạnh", "B8"),
        ("Ngưỡng hôn mê – tử vong: trong máu:", "Ngưỡng hôn mê – tử vong trong máu:", "C7"),
    ],
    "PARAQUAT": [
        ("cơ thể lấy Oxi", "cơ thể lấy oxy", "B9"),
    ],
    "STRYCHNINE": [
        ("Strychnine là 1 alkaloid", "Strychnine là một alkaloid", "B10"),
    ],
    "PROFENOFOS": [
        ("nhóm photpho hữu cơ", "nhóm phospho hữu cơ", "B11"),
    ],
    "TERPIN": [
        ("thuốc long đàm", "thuốc long đờm", "B12"),
    ],
    "PROPRANOLOL": [
        ("Ngưỡng hôn mê – tử vong: trong máu:", "Ngưỡng hôn mê – tử vong trong máu:", "C7"),
    ],
    "AMITRIPTYLINE": [
        ("0.05-0.3 mg/L", "0,05 – 0,3 mg/L", "C4"),
        ("0.5 – 0.6 mg/L", "0,5 – 0,6 mg/L", "C4"),
        ("1.5 – 2 mg/L", "1,5 – 2 mg/L", "C4"),
    ],
}

# C2: dòng trong thân bài thực ra là tài liệu tham khảo nhưng bản gốc không
# ghi nhãn "TLTK". Dòng bắt đầu bằng các chuỗi dưới đây được chuyển xuống mục
# tài liệu tham khảo.
DONG_LA_TLTK = {
    "LIDOCAINE": ("Goldfrank",),
}

# Nhóm B và C: sửa trên mọi tệp.
SUA_TOAN_BO = [
    ("synape", "synap", "B2"),
    ("Krirger", "Krieger", "B7"),
]


class NhatKy:
    def __init__(self):
        self.dong = []

    def ghi(self, tep, ma, goc, moi, so_lan=1):
        self.dong.append((tep, ma, goc, moi, so_lan))

    def xuat(self, duong_dan):
        self.dong.sort(key=lambda d: (d[0], d[1]))
        out = [
            "# Nhật ký hiệu đính",
            "",
            "Tệp này do `scripts/trich_xuat.py` sinh tự động. Không sửa tay.",
            "",
            "Mỗi dòng ghi lại một chỗ khác biệt giữa bản Markdown dùng cho app và tệp"
            " `.docx` gốc của ThS.BS. Âu Dương Quốc Uy. Cột **Mã** trỏ tới mục tương ứng"
            " trong `danh-sach-sua-loi.md`.",
            "",
            "| Tệp gốc | Mã | Bản gốc ghi | Đã sửa thành | Số lần |",
            "|---|---|---|---|---|",
        ]
        for tep, ma, goc, moi, so_lan in self.dong:
            g = goc.replace("|", "\\|")
            m = moi.replace("|", "\\|")
            out.append(f"| {tep} | {ma} | {g} | {m} | {so_lan} |")
        out += ["", f"Tổng: {len(self.dong)} chỗ sửa.", ""]
        with open(duong_dan, "w", encoding="utf-8") as f:
            f.write("\n".join(out))


# ---------------------------------------------------------------- đọc docx


def chu_trong_the(el):
    ra = []
    for n in el.iter():
        if n.tag == W + "t":
            ra.append(n.text or "")
        elif n.tag == W + "tab":
            ra.append("\t")
        elif n.tag == W + "br":
            ra.append("\n")
        elif n.tag == W + "sym":
            khoa = (n.get(W + "font"), n.get(W + "char"))
            ra.append(KY_HIEU.get(khoa, ""))
        elif n.tag == W + "drawing" or n.tag.endswith("}pict"):
            ra.append("\x00HINH\x00")
    return "".join(ra)


def doc_docx(duong_dan):
    """Trả về danh sách phần tử: ('p', chữ, cấp) | ('tbl', các hàng) | ('hinh',)"""
    goc = ET.fromstring(zipfile.ZipFile(duong_dan).read("word/document.xml"))
    than = goc.find(W + "body")
    ket_qua = []
    for el in than:
        if el.tag == W + "p":
            chu = chu_trong_the(el)
            cap = 0
            ppr = el.find(W + "pPr")
            if ppr is not None:
                npr = ppr.find(W + "numPr")
                if npr is not None:
                    ilvl = npr.find(W + "ilvl")
                    cap = int(ilvl.get(W + "val")) if ilvl is not None else 0
            if "\x00HINH\x00" in chu:
                ket_qua.append(("hinh",))
                chu = chu.replace("\x00HINH\x00", "").strip()
                if not chu:
                    continue
            ket_qua.append(("p", chu, cap))
        elif el.tag == W + "tbl":
            hang = []
            for tr in el.iter(W + "tr"):
                o = []
                for tc in tr.findall(W + "tc"):
                    # mỗi đoạn trong một ô là một dòng riêng, không dính liền nhau
                    doan = [chu_trong_the(p).strip() for p in tc.findall(W + "p")]
                    o.append("\n".join(d for d in doan if d))
                hang.append(o)
            ket_qua.append(("tbl", hang))
    return ket_qua


# ---------------------------------------------------------------- chuẩn hóa


def chuan_hoa(chu):
    """C1, C6: mũi tên thống nhất, bỏ tab và khoảng trắng thừa.

    Trả về (cấp thụt đầu dòng, chữ đã chuẩn hóa). Bản Word dùng ký tự tab ở
    đầu dòng để thể hiện mục con, nên phải đếm tab trước khi bỏ.
    """
    chu = unicodedata.normalize("NFC", chu)
    cap = 0
    m = re.match(r"^[  ]*((?:\t[  ]*)*)", chu)
    if m:
        cap = m.group(1).count("\t")
    chu = chu.replace("\t", " ")
    chu = chu.replace("=>", "→").replace("->", "→")
    chu = re.sub(r"\s*→\s*", " → ", chu)
    chu = re.sub(r"[  ]{2,}", " ", chu)
    return max(0, cap - 1), chu.strip()


def chuan_hoa_khoang(chu):
    """C5: trong trị số ngưỡng, thống nhất gạch dài có khoảng trắng hai bên."""
    return re.sub(r"(?<=[\d,\.])\s*[-–]\s*(?=\d)", " – ", chu)


def ky_hieu_hoa_hoc(chu):
    """C10: khôi phục chỉ số trên/dưới đã mất khi chuyển từ Word."""
    chu = re.sub(r"\bGABAA\b", "GABA<sub>A</sub>", chu)
    chu = re.sub(r"\bCa2\+", "Ca<sup>2+</sup>", chu)
    chu = re.sub(r"\bCl-(?![a-zA-ZÀ-ỹ])", "Cl<sup>−</sup>", chu)
    chu = re.sub(r"\bNa\+", "Na<sup>+</sup>", chu)
    chu = re.sub(r"\bK\+", "K<sup>+</sup>", chu)
    chu = re.sub(r"\bNa<sup>\+</sup>/K<sup>\+</sup>", "Na<sup>+</sup>/K<sup>+</sup>", chu)
    return chu


def bo_so_chu_thich(chu, ma_tep):
    """C8: bỏ số chú thích chân trang bị dính vào cuối câu."""
    if ma_tep not in ("OMEPRAZOLE", "CERITIZIN final"):
        return chu, 0
    moi, n = re.subn(r"(?<=[a-zA-ZÀ-ỹ\)\.\d])\.(\d(?:,\d)*)(?=\s|$)", ".", chu)
    moi2, n2 = re.subn(r"(?<=mg/L)\.(\d(?:,\d)*)(?=\s|$)", ".", moi)
    return moi2, n + n2


# ---------------------------------------------------------------- phân loại

RE_NGUONG = re.compile(
    r"^(Ngưỡng|Nồng độ)\s+([^:]*?)\s*:\s*(.+?)\s*$", re.IGNORECASE
)
RE_LIEU = re.compile(r"^(Liều|LD50|LD\s*50)\b", re.IGNORECASE)
RE_TLTK = re.compile(
    r"^(TLTK|Tài liệu tham khảo|TÀI LIỆU THAM KHẢO|Reference|References)\s*:?\s*(.*)$",
    re.IGNORECASE,
)


def loai_nguong(nhan):
    n = nhan.lower()
    co_hon_me = "hôn mê" in n or "tử vong" in n
    co_doc = "độc" in n
    if "điều trị" in n:
        return "dieuTri"
    if co_hon_me and co_doc:
        return "docVaTuVong"
    if co_hon_me:
        return "tuVong"
    if co_doc:
        return "doc"
    return None


def doan_don_vi(cac_nguong, ma_tep):
    if ma_tep == "ETHANOL":
        return "mg/100 mL"
    if ma_tep == "CO":
        return "% COHb"
    for g in cac_nguong.values():
        m = re.search(r"(mg/L|mg/100\s*mL|mg/dL|ng/mL|µg/L|mcg/L)", g["giaTri"])
        if m:
            return m.group(1).replace("  ", " ")
    return ""


# ---------------------------------------------------------------- tạo slug


def tao_slug(ten):
    s = unicodedata.normalize("NFD", ten.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------- xuất YAML


def yaml_chuoi(gia_tri):
    if gia_tri is None or gia_tri == "":
        return '""'
    g = str(gia_tri)
    if re.search(r'[:#\[\]{}>|*&!%@`"\']', g) or g != g.strip():
        return '"' + g.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return g


def viet_md(chat, duong_dan):
    d = ["---"]
    d.append(f"ten: {yaml_chuoi(chat['ten'])}")
    d.append(f"tenGoc: {yaml_chuoi(chat['tenGoc'])}")
    d.append(f"slug: {chat['slug']}")
    d.append(f"nhom: {yaml_chuoi(chat['nhom'])}")
    d.append("nhan:" + (" []" if not chat["nhan"] else ""))
    for n in chat["nhan"]:
        d.append(f"  - {yaml_chuoi(n)}")
    d.append("tenKhac:" + (" []" if not chat["tenKhac"] else ""))
    for n in chat["tenKhac"]:
        d.append(f"  - {yaml_chuoi(n)}")
    d.append(f"donVi: {yaml_chuoi(chat['donVi'])}")
    for khoa in ("dieuTri", "doc", "tuVong", "docVaTuVong"):
        g = chat["nguong"].get(khoa)
        if g:
            d.append(f"{khoa}:")
            d.append(f"  nhan: {yaml_chuoi(g['nhan'])}")
            d.append(f"  giaTri: {yaml_chuoi(g['giaTri'])}")
    if chat.get("hinh"):
        d.append(f"hinh: {chat['hinh']}")
    if chat.get("ghiChu"):
        d.append(f"ghiChu: {yaml_chuoi(chat['ghiChu'])}")
    d.append(f"tepGoc: {yaml_chuoi(chat['tepGoc'])}")
    d.append("---")
    d.append("")
    d.append(f"# {chat['ten']}")
    d.append("")

    if chat["noiDung"]:
        d.append("## Nội dung")
        d.append("")
        d += chat["noiDung"]
        d.append("")
    if chat["lieu"]:
        d.append("## Liều")
        d.append("")
        d += [f"- {x}" for x in chat["lieu"]]
        d.append("")
    if chat["bang"]:
        d.append("## Bảng")
        d.append("")
        for b in chat["bang"]:
            d += b
            d.append("")
    if chat.get("hinh"):
        d.append("## Hình")
        d.append("")
        d.append(f"![{chat['ten']}](../docs/hinh/{chat['hinh']})")
        d.append("")
    if chat["tltk"]:
        d.append("## Tài liệu tham khảo")
        d.append("")
        d += [f"- {x}" for x in chat["tltk"]]
        d.append("")

    with open(duong_dan, "w", encoding="utf-8") as f:
        f.write("\n".join(d))


# ---------------------------------------------------------------- xử lý 1 tệp


def xu_ly(ma_tep, meta, nhat_ky):
    duong_dan = os.path.join(THU_MUC_DOCX, ma_tep + ".docx")
    phan_tu = doc_docx(duong_dan)

    # gom thành danh sách dòng chữ, nhớ vị trí bảng và hình
    dong = []
    for pt in phan_tu:
        if pt[0] == "p":
            cap_tab, chu = chuan_hoa(pt[1])
            if chu:
                dong.append(("chu", chu, max(pt[2], cap_tab)))
        elif pt[0] == "tbl":
            dong.append(("bang", pt[1], 0))
        elif pt[0] == "hinh":
            dong.append(("hinh", None, 0))

    # áp dụng sửa lỗi
    cac_sua = SUA_THEO_TEP.get(ma_tep, []) + SUA_TOAN_BO
    dem = {}
    for i, (loai, noi, cap) in enumerate(dong):
        if loai != "chu":
            continue
        moi = noi
        for goc, thay, ma in cac_sua:
            if goc in moi:
                so = moi.count(goc)
                moi = moi.replace(goc, thay)
                khoa = (ma, goc, thay)
                dem[khoa] = dem.get(khoa, 0) + so
        moi, n_ct = bo_so_chu_thich(moi, ma_tep)
        if n_ct:
            khoa = ("C8", "số chú thích dính vào cuối câu", "(đã bỏ)")
            dem[khoa] = dem.get(khoa, 0) + n_ct
        dong[i] = ("chu", moi, cap)
    for (ma, goc, thay), so in dem.items():
        nhat_ky.ghi(ma_tep + ".docx", ma, goc, thay, so)

    # tách phần tài liệu tham khảo
    than, tltk = [], []
    trong_tltk = False
    for loai, noi, cap in dong:
        if loai == "chu":
            m = RE_TLTK.match(noi)
            if m:
                trong_tltk = True
                con_lai = m.group(2).strip(" .:")
                if con_lai:
                    tltk.append(con_lai)
                continue
        if trong_tltk:
            if loai == "chu":
                noi = re.sub(r"^\d+\.\s*", "", noi).strip()
                if noi:
                    tltk.append(noi)
            continue
        than.append((loai, noi, cap))

    # bỏ dòng tiêu đề trùng tên chất ở đầu tệp
    if than and than[0][0] == "chu":
        dau = than[0][1].strip().rstrip(":").upper()
        ung_vien = [meta["ten"].upper().split(" (")[0],
                    ma_tep.upper().replace(" FINAL", "")]
        trung = any(
            (dau.startswith(t) or t.startswith(dau))
            and abs(len(dau) - len(t)) < 30
            for t in ung_vien
        )
        if trung:
            than = than[1:]

    noi_dung, lieu, bang, nguong = [], [], [], {}
    hinh = None
    for loai, noi, cap in than:
        if loai == "bang":
            hang = noi
            if not hang:
                continue
            rong = max(len(h) for h in hang)
            md = ["| " + " | ".join(x or "" for x in (hang[0] + [""] * rong)[:rong]) + " |"]
            md.append("|" + "---|" * rong)
            for h in hang[1:]:
                o = [(x or "").replace("\n", "<br>") for x in (h + [""] * rong)[:rong]]
                md.append("| " + " | ".join(o) + " |")
            bang.append(md)
            continue
        if loai == "hinh":
            hinh = f"{tao_slug(meta['ten'])}.png"
            continue

        if noi.startswith(DONG_LA_TLTK.get(ma_tep, ())):
            tltk.append(noi)
            nhat_ky.ghi(ma_tep + ".docx", "C2", noi[:46] + "…",
                        "chuyển xuống mục Tài liệu tham khảo", 1)
            continue

        m = RE_NGUONG.match(noi)
        if m:
            khoa = loai_nguong(m.group(2))
            if khoa and khoa not in nguong:
                nguong[khoa] = {
                    "nhan": (m.group(1) + " " + m.group(2)).strip(),
                    "giaTri": chuan_hoa_khoang(m.group(3).rstrip(".")),
                }
                continue
        if RE_LIEU.match(noi):
            lieu.append(ky_hieu_hoa_hoc(noi))
            continue
        tien_to = "  " * cap + "- " if cap is not None else "- "
        noi_dung.append(tien_to + ky_hieu_hoa_hoc(noi))

    ten = meta["ten"]
    return {
        "ten": ten,
        "tenGoc": meta.get("tenGoc", ten),
        "slug": tao_slug(ten),
        "nhom": meta["nhom"],
        "nhan": meta.get("nhan", []),
        "tenKhac": meta.get("tenKhac", []),
        "donVi": doan_don_vi(nguong, ma_tep),
        "nguong": nguong,
        "noiDung": noi_dung,
        "lieu": lieu,
        "bang": bang,
        "tltk": tltk,
        "hinh": hinh,
        "ghiChu": meta.get("ghiChu"),
        "tepGoc": ma_tep + ".docx",
    }


def tach_morphine_codeine(nhat_ky, md):
    """Tệp MORPHINE, CODEINE.docx chứa hai chất, tách thành hai tệp."""
    ma_tep = "MORPHINE, CODEINE"
    phan_tu = doc_docx(os.path.join(THU_MUC_DOCX, ma_tep + ".docx"))
    dong = [chuan_hoa(p[1])[1] for p in phan_tu if p[0] == "p"]
    dong = [d for d in dong if d]
    cat = next(i for i, d in enumerate(dong) if d.strip().upper() == "CODEINE")
    ket_qua = []
    for ten, phan in (("Morphine", dong[:cat]), ("Codeine", dong[cat:])):
        meta = md["chat"][ten.upper()]
        than, tltk, trong = [], [], False
        for d in phan:
            m = RE_TLTK.match(d)
            if m:
                trong = True
                if m.group(2).strip(" .:"):
                    tltk.append(m.group(2).strip(" .:"))
                continue
            (tltk if trong else than).append(d)
        if than and than[0].strip().upper() == ten.upper():
            than = than[1:]
        noi_dung, nguong = [], {}
        for d in than:
            m = RE_NGUONG.match(d)
            if m:
                khoa = loai_nguong(m.group(2))
                if khoa and khoa not in nguong:
                    nguong[khoa] = {
                        "nhan": (m.group(1) + " " + m.group(2)).strip(),
                        "giaTri": chuan_hoa_khoang(m.group(3).rstrip(".")),
                    }
                    continue
            noi_dung.append("- " + ky_hieu_hoa_hoc(d))
        ket_qua.append({
            "ten": ten,
            "tenGoc": ten,
            "slug": tao_slug(ten),
            "nhom": meta["nhom"],
            "nhan": meta.get("nhan", []),
            "tenKhac": meta.get("tenKhac", []),
            "donVi": doan_don_vi(nguong, ten.upper()),
            "nguong": nguong,
            "noiDung": noi_dung,
            "lieu": [],
            "bang": [],
            "tltk": tltk,
            "hinh": None,
            "ghiChu": None,
            "tepGoc": ma_tep + ".docx",
        })
    nhat_ky.ghi(ma_tep + ".docx", "C3",
                "một tệp chứa hai chất", "tách thành Morphine và Codeine", 1)
    return ket_qua


def trich_hinh():
    for ma_tep, ten in (("LIDOCAINE", "Lidocaine"),
                        ("TETRAHYDROCANNABINOL", "Tetrahydrocannabinol")):
        z = zipfile.ZipFile(os.path.join(THU_MUC_DOCX, ma_tep + ".docx"))
        for ten_tep in z.namelist():
            if ten_tep.startswith("word/media/"):
                dich = os.path.join(THU_MUC_HINH, tao_slug(ten) + ".png")
                with open(dich, "wb") as f:
                    f.write(z.read(ten_tep))
                break


def main():
    with open(os.path.join(os.path.dirname(__file__), "metadata.json"),
              encoding="utf-8") as f:
        md = json.load(f)

    os.makedirs(THU_MUC_MD, exist_ok=True)
    os.makedirs(THU_MUC_HINH, exist_ok=True)
    nhat_ky = NhatKy()

    tep_docx = sorted(
        t[:-5] for t in os.listdir(THU_MUC_DOCX) if t.endswith(".docx")
    )
    thieu = [t for t in tep_docx
             if t not in md["chat"] and t != "MORPHINE, CODEINE"]
    if thieu:
        print("Thiếu metadata cho:", thieu, file=sys.stderr)
        return 1

    cac_chat = []
    for ma_tep in tep_docx:
        if ma_tep == "MORPHINE, CODEINE":
            cac_chat += tach_morphine_codeine(nhat_ky, md)
            continue
        cac_chat.append(xu_ly(ma_tep, md["chat"][ma_tep], nhat_ky))

    # ghi nhật ký đổi tên hiển thị (B1)
    for ma_tep, m in md["chat"].items():
        if ma_tep in ("MORPHINE", "CODEINE"):
            continue
        if m["ten"].upper() != ma_tep.upper().replace(" FINAL", ""):
            nhat_ky.ghi(ma_tep + ".docx", "B1", ma_tep, m["ten"], 1)

    for c in cac_chat:
        viet_md(c, os.path.join(THU_MUC_MD, c["slug"] + ".md"))

    trich_hinh()
    nhat_ky.xuat(NHAT_KY)

    print(f"Đã sinh {len(cac_chat)} tệp Markdown trong noi-dung/")
    print(f"Nhật ký hiệu đính: {len(nhat_ky.dong)} dòng")
    co_nguong = sum(1 for c in cac_chat if c["nguong"])
    print(f"Có ngưỡng nồng độ: {co_nguong}/{len(cac_chat)} chất")
    return 0


if __name__ == "__main__":
    sys.exit(main())
