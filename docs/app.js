/* Sổ tay Độc chất học trong Giám định pháp y
   Nội dung chuyên môn: ThS.BS. Âu Dương Quốc Uy */

(function () {
  "use strict";

  var DL = null;
  var trangThai = {
    q: "", nhom: "", nhan: "", chiCoNguong: false,
    sapXep: "nhom", chon: null, soSanh: []
  };
  var ketQua = [];

  var $ = function (id) { return document.getElementById(id); };

  // ------------------------------------------------------------ tiện ích

  function boDau(chu) {
    return chu
      .toLowerCase()
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .replace(/đ/g, "d");
  }

  function thoat(chu) {
    return String(chu)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  /* Nội dung gốc chỉ chứa <sub> và <sup> do script sinh ra (mục C10).
     Thoát mọi thẻ khác rồi mở lại đúng hai thẻ này. */
  function chuCoChiSo(chu) {
    return thoat(chu).replace(/&lt;(\/?)(sub|sup)&gt;/g, "<$1$2>");
  }

  function boThe(chu) {
    return String(chu).replace(/<\/?(sub|sup)>/g, "");
  }

  function tachTuKhoa(q) {
    return boDau(q).split(/\s+/).filter(function (t) { return t.length > 0; });
  }

  // ------------------------------------------------------------ tìm kiếm

  function loc() {
    var tu = tachTuKhoa(trangThai.q);
    ketQua = DL.chat.filter(function (c) {
      if (trangThai.nhom && c.nhom !== trangThai.nhom) return false;
      if (trangThai.nhan && c.nhan.indexOf(trangThai.nhan) < 0) return false;
      if (trangThai.chiCoNguong && !coNguong(c)) return false;
      return tu.every(function (t) { return c.timKiem.indexOf(t) >= 0; });
    });
    /* Xếp hạng khi tìm kiếm: khớp nguyên cụm ở tên đứng trước, rồi khớp rời
       ở tên, rồi khớp nguyên cụm trong nội dung, cuối cùng là khớp rời. */
    var cum = tu.join(" ");
    ketQua.forEach(function (c) {
      if (!tu.length) c._diem = 0;
      else if (c.timTen.indexOf(cum) >= 0) c._diem = 0;
      else if (tu.every(function (t) { return c.timTen.indexOf(t) >= 0; })) c._diem = 1;
      else if (c.timKiem.indexOf(cum) >= 0) c._diem = 2;
      else c._diem = 3;
    });

    if (trangThai.sapXep === "ten") {
      ketQua.sort(function (a, b) { return a.ten.localeCompare(b.ten, "vi"); });
    } else if (tu.length) {
      ketQua.sort(function (a, b) {
        if (a._diem !== b._diem) return a._diem - b._diem;
        return DL.chat.indexOf(a) - DL.chat.indexOf(b);
      });
    }
  }

  function coNguong(c) {
    return Object.keys(c.nguong).length > 0;
  }

  function danhDau(ten) {
    var tu = tachTuKhoa(trangThai.q);
    if (!tu.length) return thoat(ten);
    var khong = boDau(ten);
    var cho = [];
    tu.forEach(function (t) {
      var i = khong.indexOf(t);
      while (i >= 0) {
        cho.push([i, i + t.length]);
        i = khong.indexOf(t, i + 1);
      }
    });
    if (!cho.length) return thoat(ten);
    cho.sort(function (a, b) { return a[0] - b[0]; });
    var gop = [cho[0]];
    for (var k = 1; k < cho.length; k++) {
      var cuoi = gop[gop.length - 1];
      if (cho[k][0] <= cuoi[1]) cuoi[1] = Math.max(cuoi[1], cho[k][1]);
      else gop.push(cho[k]);
    }
    var ra = "", vt = 0;
    gop.forEach(function (d) {
      ra += thoat(ten.slice(vt, d[0])) + "<mark>" + thoat(ten.slice(d[0], d[1])) + "</mark>";
      vt = d[1];
    });
    return ra + thoat(ten.slice(vt));
  }

  // ------------------------------------------------------- vẽ danh sách

  function veDanhSach() {
    var hop = $("danh-sach");
    var dem = $("dem-ket-qua");
    var tongCong = DL.chat.length;

    if (!ketQua.length) {
      dem.textContent = "";
      hop.innerHTML =
        '<p class="trong">Không tìm thấy chất nào khớp. Thử bỏ bớt từ khóa hoặc bỏ bộ lọc.</p>';
      return;
    }
    dem.textContent =
      ketQua.length === tongCong
        ? tongCong + " chất"
        : ketQua.length + " / " + tongCong + " chất";

    var html = "";
    var dauMucTruoc = null;
    var coTim = trangThai.q.trim().length > 0;
    var theoTen = trangThai.sapXep === "ten";

    ketQua.forEach(function (c) {
      /* Xếp theo nhóm: tiêu đề là tên nhóm. Xếp theo tên: tiêu đề là chữ cái
         đầu. Khi đang tìm kiếm và xếp theo nhóm thì bỏ tiêu đề, vì kết quả
         đã xếp theo mức độ khớp. */
      var dauMuc = theoTen ? boDau(c.ten).charAt(0).toUpperCase()
        : (coTim ? null : c.nhom);
      if (dauMuc && dauMuc !== dauMucTruoc) {
        dauMucTruoc = dauMuc;
        html += '<p class="ten-nhom">' + thoat(dauMuc) + "</p>";
      }
      var phu = coTim && c._diem >= 2
        ? "khớp trong nội dung"
        : c.tenKhac.slice(0, 3).join(", ");
      html +=
        '<button type="button" class="muc-chat" data-slug="' + c.slug + '"' +
        (trangThai.chon === c.slug ? ' aria-current="true"' : "") + ">" +
        danhDau(c.ten) +
        (phu ? '<span class="phu">' + thoat(phu) + "</span>" : "") +
        "</button>";
    });
    hop.innerHTML = html;

    var cot = document.querySelector(".cot-danh-sach");
    var dangChon = hop.querySelector('[aria-current="true"]');
    if (dangChon && cot && cot.scrollHeight > cot.clientHeight + 4) {
      var tren = dangChon.getBoundingClientRect().top -
        cot.getBoundingClientRect().top + cot.scrollTop;
      if (tren < cot.scrollTop || tren > cot.scrollTop + cot.clientHeight - 70) {
        cot.scrollTop = Math.max(0, tren - cot.clientHeight / 3);
      }
    }
  }

  // -------------------------------------------------------- vẽ chi tiết

  function veDaiNguong(c) {
    var n = c.nguong;
    var o = [];
    if (n.dieuTri) o.push({ lop: "dieu-tri", nhan: "Điều trị", g: n.dieuTri });
    if (n.doc) o.push({ lop: "doc", nhan: "Độc", g: n.doc });
    if (n.tuVong) o.push({ lop: "tu-vong", nhan: "Hôn mê – tử vong", g: n.tuVong });
    if (n.docVaTuVong) {
      o.push({ lop: "tu-vong", nhan: "Độc, hôn mê – tử vong", g: n.docVaTuVong });
    }
    if (!o.length) {
      return (
        '<p class="khong-co-nguong">Tài liệu không ghi nhận ngưỡng nồng độ trong máu' +
        (c.lieu.length ? " (xem phần Liều bên dưới)." : ".") +
        "</p>"
      );
    }
    var tren = o.map(function (x) {
      return '<div class="o-nguong ' + x.lop + '">' + thoat(boDonVi(x.g.giaTri, c.donVi)) + "</div>";
    }).join("");
    var duoi = o.map(function (x) {
      return "<span>" + thoat(x.nhan) + "</span>";
    }).join("");
    return (
      '<div class="dai-nguong">' + tren + "</div>" +
      '<div class="chu-thich-nguong">' + duoi + "</div>" +
      (c.donVi ? '<p class="don-vi-nguong">Đơn vị: ' + thoat(c.donVi) +
        ". Ghi theo đúng đơn vị của tài liệu gốc.</p>" : "")
    );
  }

  function boDonVi(giaTri, donVi) {
    if (!donVi) return giaTri;
    return giaTri.replace(new RegExp("\\s*" + donVi.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\s*$"), "");
  }

  function veDanhSachCay(muc) {
    if (!muc.length) return "";
    return "<ul>" + muc.map(function (m) {
      return "<li>" + chuCoChiSo(m.chu) +
        (m.con && m.con.length ? veDanhSachCay(m.con) : "") + "</li>";
    }).join("") + "</ul>";
  }

  function veBang(b) {
    var th = b.dau.map(function (x) { return "<th>" + chuCoChiSo(x) + "</th>"; }).join("");
    var tr = b.hang.map(function (h) {
      return "<tr>" + h.map(function (x) {
        return "<td>" + chuCoChiSo(x).replace(/&lt;br&gt;/g, "<br>") + "</td>";
      }).join("") + "</tr>";
    }).join("");
    return '<div class="bang-cuon"><table class="bang-noi-dung"><thead><tr>' +
      th + "</tr></thead><tbody>" + tr + "</tbody></table></div>";
  }

  function veChiTiet(slug) {
    var c = timChat(slug);
    var hop = $("chi-tiet");
    if (!c) { veTrangChao(); return; }

    var daChon = trangThai.soSanh.indexOf(slug) >= 0;
    var h = '<article class="the">';

    h += '<div class="chi-tiet-dau"><div>';
    h += "<h2>" + thoat(c.ten) + "</h2>";
    if (c.tenKhac.length) {
      h += '<p class="ten-khac">Tên gọi khác: ' + thoat(c.tenKhac.join(", ")) +
        " <span title=\"Do người làm app bổ sung để tra cứu, không thuộc tài liệu gốc\">ⓘ</span></p>";
    }
    h += "</div>";
    h += '<div class="nut-chi-tiet">';
    h += '<button type="button" id="nut-chep">Sao chép</button>';
    h += '<button type="button" id="nut-them-so-sanh">' +
      (daChon ? "Bỏ khỏi so sánh" : "Thêm vào so sánh") + "</button>";
    h += "</div></div>";

    h += '<div class="hang-nhan"><span class="vien-nhan nhom">' + thoat(c.nhom) + "</span>";
    c.nhan.forEach(function (n) { h += '<span class="vien-nhan">' + thoat(n) + "</span>"; });
    h += "</div>";

    h += '<h3 class="de-muc">Ngưỡng nồng độ trong máu</h3>';
    h += veDaiNguong(c);

    if (c.noiDung.length) {
      h += '<h3 class="de-muc">Nội dung</h3>';
      h += '<div class="van-ban">' + veDanhSachCay(c.noiDung) + "</div>";
    }
    if (c.lieu.length) {
      h += '<h3 class="de-muc">Liều</h3>';
      h += '<div class="van-ban"><ul>' + c.lieu.map(function (x) {
        return "<li>" + chuCoChiSo(x) + "</li>";
      }).join("") + "</ul></div>";
    }
    if (c.bang && c.bang.length) {
      h += '<h3 class="de-muc">Bảng</h3>';
      c.bang.forEach(function (b) { h += veBang(b); });
    }
    if (c.hinh) {
      h += '<h3 class="de-muc">Hình</h3>';
      h += '<img class="hinh-minh-hoa" src="hinh/' + thoat(c.hinh) +
        '" alt="Hình minh họa trong tài liệu gốc về ' + thoat(c.ten) + '">';
    }
    if (c.ghiChu) {
      h += '<p class="nguon-goc">Lưu ý: ' + thoat(c.ghiChu) + "</p>";
    }
    if (c.tltk.length) {
      h += '<h3 class="de-muc">Tài liệu tham khảo</h3>';
      h += '<ol class="tltk">' + c.tltk.map(function (x) {
        return "<li>" + thoat(x) + "</li>";
      }).join("") + "</ol>";
    }
    h += '<p class="nguon-goc">Nguồn: ' + thoat(c.tepGoc) +
      " — ThS.BS. Âu Dương Quốc Uy.</p>";
    h += "</article>";

    hop.innerHTML = h;

    $("nut-chep").addEventListener("click", function () { chepChat(c, this); });
    $("nut-them-so-sanh").addEventListener("click", function () { doiSoSanh(slug); });
    var hinh = hop.querySelector(".hinh-minh-hoa");
    if (hinh) hinh.addEventListener("click", function () { phongTo(hinh.src, hinh.alt); });
    hop.scrollIntoView({ block: "nearest" });
  }

  function timChat(slug) {
    for (var i = 0; i < DL.chat.length; i++) {
      if (DL.chat[i].slug === slug) return DL.chat[i];
    }
    return null;
  }

  // ------------------------------------------------------------ chép

  function vanBanChat(c) {
    /* Không chép tên gọi khác và nhãn: đó là phần do app bổ sung.
       Chỉ chép nội dung đúng như tài liệu gốc. */
    var d = [c.ten.toUpperCase(), ""];
    c.noiDung.forEach(function (m) {
      d.push("- " + boThe(m.chu));
      (m.con || []).forEach(function (x) { d.push("    + " + boThe(x.chu)); });
    });
    var n = c.nguong;
    ["dieuTri", "doc", "tuVong", "docVaTuVong"].forEach(function (k) {
      if (n[k]) d.push("- " + n[k].nhan + ": " + n[k].giaTri + ".");
    });
    c.lieu.forEach(function (x) { d.push("- " + boThe(x)); });
    (c.bang || []).forEach(function (b) {
      d.push("");
      d.push(b.dau.join(" | "));
      b.hang.forEach(function (h) {
        d.push(h.map(function (x) { return boThe(x).replace(/<br>/g, "; "); }).join(" | "));
      });
    });
    if (c.tltk.length) {
      d.push("", "Tài liệu tham khảo:");
      c.tltk.forEach(function (x, i) { d.push((i + 1) + ". " + x); });
    }
    d.push("", "Nguồn: Sổ tay Độc chất học trong Giám định pháp y — ThS.BS. Âu Dương Quốc Uy.");
    return d.join("\n");
  }

  function chepChat(c, nut) {
    var chu = vanBanChat(c);
    var xong = function () {
      var cu = nut.textContent;
      nut.textContent = "Đã chép";
      setTimeout(function () { nut.textContent = cu; }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(chu).then(xong, function () { chepDuPhong(chu, xong); });
    } else {
      chepDuPhong(chu, xong);
    }
  }

  function chepDuPhong(chu, xong) {
    var o = document.createElement("textarea");
    o.value = chu;
    o.setAttribute("readonly", "");
    o.style.position = "fixed";
    o.style.left = "-9999px";
    document.body.appendChild(o);
    o.select();
    try { document.execCommand("copy"); xong(); } catch (e) { /* bỏ qua */ }
    document.body.removeChild(o);
  }

  // ---------------------------------------------------------- so sánh

  function doiSoSanh(slug) {
    var i = trangThai.soSanh.indexOf(slug);
    if (i >= 0) trangThai.soSanh.splice(i, 1);
    else if (trangThai.soSanh.length < 6) trangThai.soSanh.push(slug);
    else { alert("So sánh tối đa 6 chất một lần."); return; }
    luuSoSanh();
    veKhay();
    if (location.hash === "#/so-sanh") veBangSoSanh();
    else if (trangThai.chon) veChiTiet(trangThai.chon);
  }

  function veKhay() {
    var khay = $("khay-so-sanh");
    if (!trangThai.soSanh.length) { khay.hidden = true; return; }
    khay.hidden = false;
    $("khay-the").innerHTML = trangThai.soSanh.map(function (s) {
      var c = timChat(s);
      return '<span class="the-chon">' + thoat(c ? c.ten : s) +
        '<button type="button" data-bo="' + s + '" aria-label="Bỏ ' +
        thoat(c ? c.ten : s) + '">×</button></span>';
    }).join("");
  }

  function veBangSoSanh() {
    var hop = $("chi-tiet");
    var ds = trangThai.soSanh.map(timChat).filter(Boolean);
    if (ds.length < 2) {
      hop.innerHTML = '<div class="the"><h2>So sánh</h2><p class="trong">' +
        "Chọn ít nhất hai chất. Mở một chất rồi bấm “Thêm vào so sánh”.</p></div>";
      return;
    }
    var hang = [
      ["Nhóm", function (c) { return thoat(c.nhom); }, ""],
      ["Ngưỡng điều trị", function (c) {
        return c.nguong.dieuTri ? thoat(c.nguong.dieuTri.giaTri) : "—";
      }, "dieu-tri"],
      ["Ngưỡng độc", function (c) {
        return c.nguong.doc ? thoat(c.nguong.doc.giaTri)
          : (c.nguong.docVaTuVong ? thoat(c.nguong.docVaTuVong.giaTri) : "—");
      }, "doc"],
      ["Hôn mê – tử vong", function (c) {
        return c.nguong.tuVong ? thoat(c.nguong.tuVong.giaTri)
          : (c.nguong.docVaTuVong ? thoat(c.nguong.docVaTuVong.giaTri) : "—");
      }, "tu-vong"],
      ["Cơ chế", function (c) {
        var m = c.noiDung.filter(function (x) { return /^Cơ chế/i.test(x.chu); })[0];
        if (!m) m = c.noiDung[0];
        var con = m && m.con && m.con.length
          ? "<ul>" + m.con.map(function (x) { return "<li>" + chuCoChiSo(x.chu) + "</li>"; }).join("") + "</ul>"
          : "";
        return m ? chuCoChiSo(m.chu) + con : "—";
      }, ""],
      ["Tài liệu gốc", function (c) { return thoat(c.tepGoc); }, ""]
    ];

    var h = '<article class="the"><div class="chi-tiet-dau"><div><h2>So sánh ' +
      ds.length + " chất</h2></div>" +
      '<div class="nut-chi-tiet"><button type="button" id="nut-chep-so-sanh">Sao chép bảng</button></div>' +
      '</div><div class="bang-cuon" style="margin-top:20px"><table class="bang-so-sanh"><thead><tr><th></th>' +
      ds.map(function (c) { return "<th>" + thoat(c.ten) + "</th>"; }).join("") +
      "</tr></thead><tbody>";
    hang.forEach(function (r) {
      h += "<tr><th>" + r[0] + "</th>" + ds.map(function (c) {
        var v = r[1](c);
        return '<td class="' + (v === "—" ? "" : r[2]) + '">' + v + "</td>";
      }).join("") + "</tr>";
    });
    h += "</tbody></table></div></article>";
    hop.innerHTML = h;

    $("nut-chep-so-sanh").addEventListener("click", function () {
      var d = ["So sánh: " + ds.map(function (c) { return c.ten; }).join(", "), ""];
      hang.forEach(function (r) {
        d.push(r[0] + ": " + ds.map(function (c) {
          return c.ten + " " + boThe(r[1](c)).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
        }).join(" | "));
      });
      d.push("", "Nguồn: Sổ tay Độc chất học trong Giám định pháp y — ThS.BS. Âu Dương Quốc Uy.");
      chepDuPhong(d.join("\n"), function () {
        var n = $("nut-chep-so-sanh");
        n.textContent = "Đã chép";
        setTimeout(function () { n.textContent = "Sao chép bảng"; }, 1600);
      });
    });
  }

  function luuSoSanh() {
    try { localStorage.setItem("doc-chat-so-sanh", JSON.stringify(trangThai.soSanh)); }
    catch (e) { /* bỏ qua */ }
  }

  // -------------------------------------------------------- trang chào

  function veTrangChao() {
    var demNhom = {};
    DL.chat.forEach(function (c) { demNhom[c.nhom] = (demNhom[c.nhom] || 0) + 1; });
    var h = '<div class="trang-chao"><h2>' + DL.soChat + " chất thường gặp trong giám định pháp y</h2>";
    h += "<p>Gõ vào ô tìm kiếm ở trên để tra theo tên chất, tên biệt dược, tên gọi thường dùng, " +
      "hoặc theo một từ trong phần cơ chế. Gõ có dấu hay không dấu đều được. " +
      "Hoặc chọn một nhóm bên dưới.</p>";
    h += '<div class="luoi-nhom">';
    DL.nhom.forEach(function (n) {
      h += '<button type="button" class="the-nhom" data-nhom="' + thoat(n) + '">' +
        thoat(n) + '<span class="dem">' + demNhom[n] + " chất</span></button>";
    });
    h += "</div></div>";
    $("chi-tiet").innerHTML = h;
  }

  // ------------------------------------------------------- phóng to hình

  function phongTo(src, alt) {
    var lop = document.createElement("div");
    lop.className = "lop-phong";
    lop.innerHTML = '<img src="' + thoat(src) + '" alt="' + thoat(alt) + '">' +
      '<button type="button" aria-label="Đóng">Đóng</button>';
    lop.addEventListener("click", function () { lop.remove(); });
    document.addEventListener("keydown", function dong(e) {
      if (e.key === "Escape") { lop.remove(); document.removeEventListener("keydown", dong); }
    });
    document.body.appendChild(lop);
  }

  // ------------------------------------------------------------ định tuyến

  function doiHash() {
    var h = location.hash;
    var m = /^#\/chat\/(.+)$/.exec(h);
    if (m) {
      trangThai.chon = decodeURIComponent(m[1]);
      veChiTiet(trangThai.chon);
      if (window.innerWidth <= 860) {
        document.querySelector(".cot-danh-sach").dataset.an = "1";
      }
    } else if (h === "#/so-sanh") {
      trangThai.chon = null;
      veBangSoSanh();
    } else {
      trangThai.chon = null;
      veTrangChao();
      document.querySelector(".cot-danh-sach").dataset.an = "";
    }
    veDanhSach();
  }

  // --------------------------------------------------------------- nền

  function datNen(gt) {
    document.documentElement.dataset.nen = gt;
    $("nut-giao-dien").textContent = gt === "toi" ? "Sáng" : "Tối";
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", gt === "toi" ? "#1a1816" : "#f7f4ee");
    try { localStorage.setItem("doc-chat-nen", gt); } catch (e) { /* bỏ qua */ }
  }

  // ------------------------------------------------------------- khởi động

  function gan() {
    var oTim = $("o-tim");
    var hen = null;
    oTim.addEventListener("input", function () {
      $("xoa-tim").hidden = !oTim.value;
      clearTimeout(hen);
      hen = setTimeout(function () {
        trangThai.q = oTim.value;
        loc();
        veDanhSach();
      }, 110);
    });
    $("xoa-tim").addEventListener("click", function () {
      oTim.value = ""; trangThai.q = ""; $("xoa-tim").hidden = true;
      loc(); veDanhSach(); oTim.focus();
    });

    $("loc-nhom").addEventListener("change", function () {
      trangThai.nhom = this.value; loc(); veDanhSach();
    });
    $("loc-nhan").addEventListener("change", function () {
      trangThai.nhan = this.value; loc(); veDanhSach();
    });
    $("loc-nguong").addEventListener("change", function () {
      trangThai.chiCoNguong = this.checked; loc(); veDanhSach();
    });
    $("sap-xep").addEventListener("change", function () {
      trangThai.sapXep = this.value;
      try { localStorage.setItem("doc-chat-sap-xep", this.value); }
      catch (e) { /* bỏ qua */ }
      loc(); veDanhSach();
    });

    $("danh-sach").addEventListener("click", function (e) {
      var n = e.target.closest(".muc-chat");
      if (n) location.hash = "#/chat/" + n.dataset.slug;
    });

    $("chi-tiet").addEventListener("click", function (e) {
      var n = e.target.closest(".the-nhom");
      if (n) {
        $("loc-nhom").value = n.dataset.nhom;
        trangThai.nhom = n.dataset.nhom;
        loc(); veDanhSach();
        document.querySelector(".cot-danh-sach").scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });

    $("khay-the").addEventListener("click", function (e) {
      var n = e.target.closest("[data-bo]");
      if (n) doiSoSanh(n.dataset.bo);
    });
    $("nut-so-sanh").addEventListener("click", function () { location.hash = "#/so-sanh"; });
    $("nut-xoa-so-sanh").addEventListener("click", function () {
      trangThai.soSanh = [];
      luuSoSanh(); veKhay();
      if (location.hash === "#/so-sanh") veBangSoSanh();
      else if (trangThai.chon) veChiTiet(trangThai.chon);
    });

    $("nut-giao-dien").addEventListener("click", function () {
      datNen(document.documentElement.dataset.nen === "toi" ? "sang" : "toi");
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "/" && document.activeElement !== oTim) {
        e.preventDefault(); oTim.focus(); oTim.select();
      }
    });

    window.addEventListener("hashchange", doiHash);
  }

  function khoiDong(dl) {
    DL = dl;
    document.title = dl.tieuDe;

    var sNhom = $("loc-nhom");
    dl.nhom.forEach(function (n) {
      var o = document.createElement("option");
      o.value = n; o.textContent = n;
      sNhom.appendChild(o);
    });
    var sNhan = $("loc-nhan");
    dl.nhan.forEach(function (n) {
      var o = document.createElement("option");
      o.value = n; o.textContent = n;
      sNhan.appendChild(o);
    });
    $("thong-tin-phien-ban").textContent =
      "Bản dữ liệu " + (dl.phienBan || "") + ", " + dl.soChat + " chất.";

    try {
      var sx = localStorage.getItem("doc-chat-sap-xep");
      if (sx === "ten" || sx === "nhom") {
        trangThai.sapXep = sx;
        $("sap-xep").value = sx;
      }
    } catch (e) { /* bỏ qua */ }

    try {
      var ss = JSON.parse(localStorage.getItem("doc-chat-so-sanh") || "[]");
      if (Array.isArray(ss)) trangThai.soSanh = ss.filter(function (s) { return timChat(s); });
    } catch (e) { /* bỏ qua */ }

    gan();
    loc();
    veKhay();
    doiHash();

    if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
      navigator.serviceWorker.register("sw.js").catch(function () { /* bỏ qua */ });
    }
  }

  // nền: nhớ lựa chọn, mặc định sáng (kiểu sổ tay in)
  var nenLuu = null;
  try { nenLuu = localStorage.getItem("doc-chat-nen"); } catch (e) { /* bỏ qua */ }
  document.documentElement.dataset.nen = nenLuu === "toi" ? "toi" : "sang";
  document.addEventListener("DOMContentLoaded", function () {
    $("nut-giao-dien").textContent =
      document.documentElement.dataset.nen === "toi" ? "Sáng" : "Tối";

    if (window.DU_LIEU_NHUNG) { khoiDong(window.DU_LIEU_NHUNG); return; }
    fetch("data/doc-chat.json")
      .then(function (r) { return r.json(); })
      .then(khoiDong)
      .catch(function () {
        $("chi-tiet").innerHTML =
          '<div class="the"><h2>Không tải được dữ liệu</h2>' +
          "<p>Nếu đang mở trực tiếp tệp index.html trên máy, hãy dùng bản một tệp " +
          "<code>So-tay-doc-chat.html</code>, hoặc chạy một máy chủ cục bộ.</p></div>";
      });
  });
})();
