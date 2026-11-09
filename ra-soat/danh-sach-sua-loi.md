# Danh sách rà soát trước khi đưa vào app

Dự án: **Sổ tay Độc chất học trong Giám định pháp y**
Tác giả nội dung: ThS.BS. Âu Dương Quốc Uy
Nguồn: 67 tệp `.docx` trong thư mục `Cơ Chế` (68 chất, vì tệp `MORPHINE, CODEINE.docx` chứa 2 chất)
Ngày rà soát: 09/11/2026

**Cách duyệt:** mỗi mục có ô `[ ]`. Bạn đánh `[x]` vào mục đồng ý sửa, gạch bỏ hoặc ghi chú vào mục không đồng ý. Những mục nhóm D là **câu hỏi chuyên môn**, mình không tự sửa, chờ bác sĩ Uy quyết định.

Nguyên tắc chung: mọi chỗ sửa đều được ghi lại chữ gốc trong tệp `nhat-ky-hieu-dinh.md`, app có thể hiện "bản gốc ghi là …" nếu bạn muốn.

---

## A. Lỗi chép nhầm tên chất (ưu tiên cao)

Đây là lỗi copy-paste giữa các tệp, làm sai nội dung chuyên môn.

- [x] **A1 — PHENYTOIN.docx**: dòng tỉ lệ máu tim/máu đùi đang ghi tên chất là *Olanzapine*. Đề xuất sửa thành *Phenytoin*.
- [x] **A2 — SILDENAFIL.docx**: dòng tỉ lệ máu tim/máu đùi đang ghi tên chất là *Caffeine* (và trị số trùng khớp với tệp CAFFEINE.docx). Đề xuất sửa thành *Sildenafil*, **nhưng cần bác sĩ Uy xác nhận lại trị số**, vì có thể trị số cũng bị chép nhầm theo. Nếu không có số liệu riêng cho Sildenafil thì nên xóa hẳn dòng này.
- [x] **A3 — WARFARIN.docx**: liệt kê yếu tố đông máu là "II, VII, Ĩ, X". Chữ "Ĩ" là lỗi gõ của số La Mã **IX**. Đề xuất sửa thành "II, VII, IX, X".

## B. Lỗi chính tả và từ ngữ

- [x] **B1 — Tên tệp và tên chất chưa khớp.** Đề xuất đổi *tên hiển thị trong app* (tên tệp gốc giữ nguyên, không đụng tới):
  - `KETAMIN.docx` → hiển thị **KETAMINE** (trong tệp đã ghi là KETAMINE)
  - `CERITIZIN final.docx` → hiển thị **CETIRIZINE** (trong tệp ghi "CETIRIZIN"; tên dược chất chuẩn là cetirizine)
  - `VENFALAXINE.docx` → hiển thị **VENLAFAXINE** (trong tệp đã ghi đúng)
  - `METRONIDAZOL.docx` → hiển thị **METRONIDAZOLE** (trong tệp đã ghi đúng)
  - `THEOPHYLLIN.docx` → hiển thị **THEOPHYLLINE**
  - `TERPIN.docx` → hiển thị **TERPIN HYDRAT**? (chờ xác nhận, xem D5)
- [x] **B2 — "synape" → "synap"** (5 tệp: CARBAMAZEPINE, CATHINONE, METHAMPHETAMINE, STRYCHNINE, TETRAHYDROCANNABINOL). Các tệp khác đã dùng "synap".
- [x] **B3 — DEXTROMETHORPHAN**: "ức thụ thể σ-opioid" thiếu chữ, đề xuất "**ức chế** thụ thể σ-opioid".
- [x] **B4 — TETRAHYDROCANNABINOL**: "nồng **dộ** trong máu" → "nồng **độ**"; "ghi nhận **một hôn mê**, vã mồ hôi" → "ghi nhận **một trường hợp** hôn mê, vã mồ hôi".
- [x] **B5 — FLUCONAZOLE**: "enzyme lanosterol 14-α-demethylase thuộc **học** CYP450" → "thuộc **họ** CYP450".
- [x] **B6 — FLUCONAZOLE (tài liệu tham khảo)**: "Diflucan (**fluconazale**) tablets label" → "(**fluconazole**)".
- [x] **B7 — Tên tác giả sách Hayes' Handbook of Pesticide Toxicology**: 6 tệp ghi "**Krirger**, Robert" (2,4-D, CYPERMETHRIN, FENOBUCARB, METOLACHLOR, PARAQUAT, PROFENOFOS). Tên đúng là "**Krieger**, Robert".
- [x] **B8 — ACETAMINOPHEN**: "chất **ô xi** hóa mạnh" → "chất **oxy** hóa mạnh".
- [x] **B9 — PARAQUAT**: "Paraquat đi vào cơ thể lấy **Oxi**" → "lấy **oxy**" (thống nhất với các tệp khác dùng "Oxy").
- [x] **B10 — STRYCHNINE**: "Strychnine là **1** alkaloid" → "là **một** alkaloid".
- [x] **B11 — Thống nhất "photpho hữu cơ" / "phospho hữu cơ"**: PROFENOFOS dùng "photpho", SULFOTEP dùng "phospho". Đề xuất dùng **"phospho hữu cơ"** cho cả hai (chờ bạn chọn).
- [ ] **B13 — CETIRIZIN (mới, phát hiện khi dựng app)**: câu "không có tác dụng đến các thụ thể khác **NHƯ** acetylcholin và serotonin" có chữ "NHƯ" viết hoa giữa câu. Đề xuất sửa thành chữ thường "như". Mình chưa sửa, chờ bạn duyệt.
- [x] **B12 — Thống nhất "long đờm" / "long đàm"**: GUAIFENESIN dùng "long đờm", TERPIN dùng "long đàm". Đề xuất dùng **"long đờm"**.

## C. Lỗi định dạng và trình bày (không đổi nội dung)

Những mục này mình xử lý tự động khi sinh dữ liệu cho app, chỉ cần bạn gật đầu một lần.

- [x] **C1 — Thống nhất mũi tên.** 9 tệp dùng `=>` thay cho `→` (ALPRAZOLAM, CETIRIZIN, IBUPROFEN, OMEPRAZOLE, PRAZEPAM, PYRIDABEN, QUETIAPINE, THIAMETHOXAM, TRIMETHOPRIM). Đề xuất đổi hết thành `→`.
- [x] **C2 — Thống nhất nhãn tài liệu tham khảo.** Hiện có 6 kiểu: "TLTK", "TLTK:", "Reference", "TÀI LIỆU THAM KHẢO", "Tài liệu tham khảo:" và bản có dấu tab ở đầu. Đề xuất trong app hiển thị thống nhất là **"Tài liệu tham khảo"**.
- [x] **C3 — Thống nhất tên các mục ngưỡng.** Bản gốc có 11 cách gọi khác nhau. Đề xuất quy về 3 mục cố định để app hiển thị và so sánh được:
  - **Ngưỡng điều trị** (gồm: "Ngưỡng điều trị trong máu", "Ngưỡng điều trị (máu)", "Nồng độ điều trị trong máu")
  - **Ngưỡng độc** (gồm: "Ngưỡng độc", "Ngưỡng độc trong máu", "Ngưỡng gây độc trong máu", "Nồng độ gây độc trong máu")
  - **Ngưỡng hôn mê – tử vong** (gồm các biến thể "Ngưỡng hôn mê – tử vong", "Ngưỡng gây hôn mê – tử vong trong máu", "Ngưỡng gây độc, hôn mê – tử vong trong máu")

  Lưu ý: với MORPHINE và CODEINE, bản gốc gộp chung thành một mục "Ngưỡng gây độc, hôn mê – tử vong". App sẽ hiển thị đúng như gốc chứ không tách đôi.
- [x] **C4 — AMITRIPTYLINE**: các trị số dùng dấu chấm thập phân kiểu Anh (0.05-0.3). Đề xuất đổi sang dấu phẩy cho thống nhất với 66 tệp còn lại (0,05-0,3).
- [x] **C5 — Dấu gạch trong khoảng trị số**: chỗ dùng gạch ngắn `-`, chỗ dùng gạch dài `–`. Đề xuất thống nhất dùng `–`.
- [x] **C6 — Xóa dấu tab thừa ở đầu dòng** (CHLORPHENIRAMINE, OLANZAPINE, METOLACHLOR, PYRIDABEN) và khoảng trắng đôi rải rác.
- [x] **C7 — ACETAMINOPHEN, PROPRANOLOL**: thừa dấu hai chấm — "Ngưỡng hôn mê – tử vong**:** trong máu: > 200 mg/L". Đề xuất bỏ dấu hai chấm thứ nhất.
- [x] **C8 — Số chú thích dính vào chữ.** OMEPRAZOLE và CETIRIZIN có số chú thích chân trang bị dính liền vào câu ("ức chế bơm proton.**1**", "0,1-0,6 mg/L.**3**"). Đề xuất bỏ các số này, vì danh sách tài liệu tham khảo vẫn còn đủ.
- [x] **C9 — IBUPROFEN**: tài liệu tham khảo đánh số 1 rồi nhảy sang 3, thiếu số 2. Đề xuất đánh số lại liên tục.
- [x] **C10 — Ký hiệu hóa học mất định dạng chỉ số.** Trong bản Word, `Cl-`, `Na+`, `Ca2+`, `GABAA` vốn có chỉ số trên/dưới. Đề xuất app hiển thị đúng dạng Cl⁻, Na⁺, Ca²⁺, GABA<sub>A</sub>.
- [x] **C11 — Hai hình trong tài liệu**: biểu đồ triệu chứng theo nồng độ Lidocaine và sơ đồ chuyển hóa THC. Đề xuất giữ nguyên hình, hiển thị trong app, phóng to được khi bấm vào.
- [x] **C12 — Thống nhất "Tỉ lệ" / "Tỷ lệ"**: hiện 16 tệp đều dùng "Tỉ lệ", đã thống nhất, **không cần sửa**. Ghi ở đây để bạn biết là đã kiểm tra.

## D. Câu hỏi chuyên môn — chờ bác sĩ Uy quyết định

Những mục này mình **không tự sửa**.

- [ ] **D1 — PYRIDABEN** đang được xếp vào "nhóm clo hữu cơ". Theo phân loại thông dụng, pyridaben là thuốc trừ nhện nhóm pyridazinone, cơ chế ức chế Complex I ở ty thể — và phần cơ chế trong tệp mô tả đúng như vậy, không giống cơ chế clo hữu cơ. Nhờ bác sĩ xem lại chữ "nhóm clo hữu cơ".
- [ ] **D2 — CHLORPHENIRAMINE**: phần cơ chế chỉ mô tả tác dụng kháng muscarinic, chưa nhắc tác dụng đối kháng thụ thể H1 là tác dụng chính của thuốc kháng histamine thế hệ 1. Có muốn bổ sung không, hay giữ nguyên như tài liệu?
- [ ] **D3 — MDMA**: tên hóa học đang ghi "N-Methyl-3,4-methylenedioxyamphetamine". Tên theo danh pháp thường gặp là "3,4-methylenedioxy-N-methylamphetamine". Có sửa không?
- [ ] **D4 — AMITRIPTYLINE**: tài liệu tham khảo ghi nguồn Schulz & Schmoldt 2020 đăng trên tạp chí *Pharmazie*, trong khi 40+ tệp khác dẫn cùng nhóm tác giả, cùng năm nhưng trên *Critical Care* 24(1):195. Nhờ bác sĩ xác nhận đây là một nguồn hay hai nguồn khác nhau.
- [ ] **D5 — TERPIN**: tên dược chất thường dùng là terpin hydrat. Có đổi tên hiển thị không?
- [ ] **D6 — Năm xuất bản Dược thư Quốc gia Việt Nam không thống nhất** giữa các tệp: phần lớn ghi "2nd ed., 2018", nhưng KETAMINE ghi "lần thứ 2 năm 2015", MIDAZOLAM ghi "2015", OMEPRAZOLE ghi "2022", METRONIDAZOLE ghi "2016". Nhờ bác sĩ cho biết nên thống nhất về năm nào, hay giữ nguyên từng tệp.
- [ ] **D7 — KETAMINE** dẫn Nghị định 73/2018/NĐ-CP về danh mục chất ma túy. Nghị định này đã được sửa đổi, bổ sung bởi văn bản ban hành sau. Có cập nhật căn cứ pháp lý không, hay giữ đúng như tài liệu?
- [ ] **D8 — Đơn vị nồng độ không thống nhất.** Phần lớn dùng mg/L, nhưng:
  - ETHANOL dùng mg/100 mL (giữ nguyên theo yêu cầu của bạn)
  - METHANOL dùng cả mg/dL và mg/100 mL trong cùng một tệp
  - CHLORFENAPYR dùng ng/mL
  - CO dùng % bão hòa COHb

  Đề xuất: app hiển thị **đúng đơn vị của bản gốc**, và ghi chú nhỏ quy đổi bên cạnh ở riêng tệp METHANOL (vì hai đơn vị trong cùng một tệp dễ gây nhầm). Bạn thấy có nên không?
- [ ] **D9 — CO và ETHANOL không có tên chất ở đầu tệp theo cùng kiểu các tệp khác.** ETHANOL mở đầu luôn bằng tiêu đề bảng. Đề xuất đặt tên hiển thị là **ETHANOL** và **CARBON MONOXIDE (CO)**.
- [ ] **D10 — Các chất không có ngưỡng nồng độ**: CYPERMETHRIN, FENOBUCARB, SULFOTEP, PROFENOFOS, TERPIN, ABAMECTIN, EMAMECTIN, METOLACHLOR, THIAMETHOXAM, PYRIDABEN, CHLORFENAPYR, TETRAHYDROPALMATINE, METHADONE. Trong app, mục ngưỡng sẽ hiển thị "Tài liệu không ghi nhận" thay vì để trống. Bạn đồng ý cách ghi này chứ?

---

## Thống kê

| Nhóm | Số mục |
|---|---|
| A. Chép nhầm tên chất | 3 |
| B. Chính tả, từ ngữ | 12 |
| C. Định dạng, trình bày | 12 |
| D. Câu hỏi chuyên môn | 10 |

Tổng: 37 mục cần duyệt.
