# Sổ tay Độc chất học trong Giám định pháp y

Web app tra cứu cơ chế gây độc và ngưỡng nồng độ trong máu của **68 chất** thường gặp trong giám định pháp y.

Nội dung chuyên môn: **ThS.BS. Âu Dương Quốc Uy**.

Dùng được trên máy tính và điện thoại, kể cả khi không có mạng. Có thể "Thêm vào màn hình chính" để dùng như một ứng dụng.

## Tính năng

- **Tra cứu**: gõ có dấu hoặc không dấu. Tìm theo tên chất, tên biệt dược, tên thường gọi (ví dụ "ma túy đá", "Seduxen"), tên nhóm, hoặc một từ trong phần cơ chế (ví dụ "GABA", "xoắn đỉnh"). Kết quả khớp tên xếp trước, khớp nội dung xếp sau và ghi rõ lý do.
- **Lọc** theo nhóm chất, theo nhãn (chất ma túy, thuốc bảo vệ thực vật, phân loại độc tính WHO, biểu hiện gây tử vong…), hoặc chỉ hiện chất có ngưỡng nồng độ.
- **Dải ba ngưỡng**: ngưỡng điều trị, ngưỡng độc và ngưỡng hôn mê – tử vong xếp liền nhau thành một thanh ngang, nhìn một cái là thấy nồng độ đo được rơi vào vùng nào. Chất nào tài liệu không ghi ngưỡng thì ghi rõ "Tài liệu không ghi nhận".
- **So sánh** tối đa 6 chất cạnh nhau: nhóm, ba ngưỡng và cơ chế.
- **Sao chép** nội dung một chất kèm tài liệu tham khảo, để dán vào bản kết luận giám định. Phần tên gọi khác và nhãn **không** được chép theo, vì đó là phần do app bổ sung.
- **Nền sáng và nền tối**, mặc định nền sáng kiểu sổ tay in.
- **In** một chất ra giấy: bản in tự bỏ các thanh điều khiển.

## Nguồn dữ liệu và nguyên tắc

Nguồn chuẩn là **67 tệp `.docx` trong thư mục `Cơ Chế`** (68 chất, vì tệp `MORPHINE, CODEINE.docx` chứa hai chất). Các tệp gốc không bị sửa.

App chỉ trình bày đúng những gì tài liệu có. Không bổ sung nội dung chuyên môn mới.

Hai thứ do người làm app thêm vào để tiện tra cứu, và được ghi rõ trong app là phần bổ sung:

- **Phân nhóm** (17 nhóm) và **nhãn phụ**
- **Tên gọi khác** (tên biệt dược, tên thường gọi, tên viết tắt), lưu ở một trường riêng, tách hẳn khỏi nội dung chuyên môn

Mọi chỗ khác biệt giữa bản dùng cho app và tệp `.docx` gốc đều được ghi lại trong [`ra-soat/nhat-ky-hieu-dinh.md`](ra-soat/nhat-ky-hieu-dinh.md), kèm mã trỏ tới mục tương ứng trong [`ra-soat/danh-sach-sua-loi.md`](ra-soat/danh-sach-sua-loi.md).

## Cấu trúc thư mục

```
Cơ Chế/                      67 tệp .docx gốc — nguồn chuẩn, không sửa
noi-dung/                    68 tệp .md sinh từ .docx, sửa tay được
ra-soat/
  danh-sach-sua-loi.md       các chỗ cần sửa, có ô duyệt
  phan-nhom-va-ten-goi-khac.md  phân nhóm và tên gọi khác, có ô duyệt
  nhat-ky-hieu-dinh.md       sinh tự động, không sửa tay
scripts/
  metadata.json              nhóm, nhãn, tên gọi khác của từng chất
  trich_xuat.py              .docx  →  noi-dung/*.md + docs/hinh/*.png
  build_data.py              noi-dung/*.md  →  docs/data/doc-chat.json
  dong_goi.py                docs/  →  So-tay-Doc-chat.html (một tệp)
docs/                        web app (GitHub Pages phục vụ thư mục này)
So-tay-Doc-chat.html         bản một tệp, dùng offline
```

## Cập nhật nội dung

**Khi bác sĩ Uy sửa tệp `.docx`:**

```bash
python3 scripts/trich_xuat.py && python3 scripts/build_data.py && python3 scripts/dong_goi.py
```

Lệnh này sinh lại toàn bộ `noi-dung/`, ghi đè mọi sửa tay trong đó.

**Khi chỉ sửa chữ trong `noi-dung/*.md`** (không đụng tới `.docx`):

```bash
python3 scripts/build_data.py && python3 scripts/dong_goi.py
```

Sau đó commit và push lên GitHub. Trang tự cập nhật sau 1–2 phút; điện thoại đã cài app cũng tự tải bản mới vì mã phiên bản trong `sw.js` đã đổi.

**Khi đổi nhóm hoặc thêm tên gọi khác:** sửa `scripts/metadata.json` rồi chạy lại cả ba lệnh.

## Chạy thử trên máy

```bash
python3 -m http.server 8766 --directory docs
```

rồi mở http://localhost:8766

Hoặc mở thẳng tệp `So-tay-Doc-chat.html` bằng trình duyệt, không cần máy chủ.

## Thống kê lượt truy cập

Dùng [GoatCounter](https://www.goatcounter.com/), không cookie, không theo dõi cá nhân, không bán dữ liệu. Bảng số liệu ở `https://sotaydocchat.goatcounter.com/`.

Tệp đếm `docs/count.js` **đặt ngay trên trang này**, không tải từ `gc.zgo.at` như hướng dẫn mặc định của GoatCounter. Lý do: `gc.zgo.at` là tên miền dùng chung cho mọi khách hàng nên nằm trong danh sách chặn của nhiều trình chặn quảng cáo, khiến không đếm được lượt nào. Tải từ chính tên miền của trang thì không bị chặn.

Khi GoatCounter ra bản mới, tải lại tệp gốc đè lên `docs/count.js`:

```bash
curl -o docs/count.js https://raw.githubusercontent.com/arp242/goatcounter/master/public/count.js
```

rồi chép lại khối chú thích năm dòng ở đầu tệp cũ vào đầu tệp mới.

Ghi nhận hai thứ:

- **Tổng lượt mở trang**, do thẻ script trong `docs/index.html` tự đếm
- **Tên chất được mở**, do hàm `ghiNhan()` trong `docs/app.js` gửi riêng, mỗi chất tính một lần cho mỗi lượt mở trang, hiện trong bảng số liệu dưới dạng `chat/<tên-chất>`

**Không** ghi nhận từ khóa gõ vào ô tìm kiếm. Từ khóa chỉ nằm trong bộ nhớ trình duyệt, không bao giờ xuất hiện trên địa chỉ URL, nên không có đường nào rời khỏi máy người dùng. GoatCounter cũng không gửi phần sau dấu `#` của địa chỉ.

Bản một tệp `So-tay-Doc-chat.html` **không có** phần thống kê: `scripts/dong_goi.py` gỡ thẻ script ra khi đóng gói, để bản offline không gọi ra ngoài.

Máy nào bật Do Not Track thì GoatCounter tự bỏ qua.

## Lưu ý

Công cụ hỗ trợ tra cứu, không thay thế tài liệu gốc và không thay thế kết luận giám định. Khi kết luận cần đối chiếu tài liệu gốc và y văn.
