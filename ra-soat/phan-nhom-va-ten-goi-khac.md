# Đề xuất phân nhóm và tên gọi khác

Dự án: **Sổ tay Độc chất học trong Giám định pháp y**
Ngày: 09/11/2026

---

## Phần 1 — Phân nhóm

### Cách làm

Mỗi chất có **một nhóm chính** (dùng để sắp xếp mục lục, mỗi chất chỉ nằm ở một chỗ) và có thể có thêm **nhãn phụ** (dùng để lọc, một chất có thể mang nhiều nhãn).

Ví dụ: Morphine có nhóm chính là "Opioid", nhãn phụ là "Chất ma túy". Phenobarbital có nhóm chính là "An thần, gây ngủ", nhãn phụ là "Chống động kinh".

Nhóm chính và nhãn phụ đều do mình đặt thêm, **không có trong tài liệu gốc**. Trong app sẽ ghi rõ ở phần giới thiệu: phân nhóm là do người làm app thêm vào để tiện tra cứu.

### 16 nhóm chính đề xuất

| # | Nhóm chính | Số chất | Các chất |
|---|---|---|---|
| 1 | Chất ma túy và chất gây ảo giác | 5 | Methamphetamine, MDMA, Cathinone, Ketamine, Tetrahydrocannabinol |
| 2 | Opioid | 5 | Morphine, Codeine, Methadone, Tramadol, Meperidine |
| 3 | An thần, giải lo âu, gây ngủ | 6 | Diazepam, Alprazolam, Bromazepam, Midazolam, Prazepam, Phenobarbital |
| 4 | Chống loạn thần | 4 | Clozapine, Olanzapine, Quetiapine, Risperidone |
| 5 | Chống trầm cảm | 4 | Amitriptyline, Sertraline, Trazodone, Venlafaxine |
| 6 | Chống động kinh | 3 | Carbamazepine, Phenytoin, Levetiracetam |
| 7 | Giảm đau, hạ sốt, kháng viêm | 2 | Acetaminophen, Ibuprofen |
| 8 | Tim mạch và huyết học | 5 | Metoprolol, Propranolol, Lidocaine, Sildenafil, Warfarin |
| 9 | Hô hấp, ho, long đờm | 4 | Theophylline, Dextromethorphan, Guaifenesin, Terpin |
| 10 | Kháng histamine | 2 | Chlorpheniramine, Cetirizine |
| 11 | Kháng sinh, kháng nấm | 5 | Clindamycin, Sulfamethoxazole, Trimethoprim, Metronidazole, Fluconazole |
| 12 | Tiêu hóa và chuyển hóa | 3 | Omeprazole, Metoclopramide, Metformin |
| 13 | Thuốc trừ sâu | 9 | Abamectin, Emamectin, Cypermethrin, Fenobucarb, Profenofos, Sulfotep, Thiamethoxam, Chlorfenapyr, Pyridaben |
| 14 | Thuốc diệt cỏ | 3 | Paraquat, 2,4-D, Metolachlor |
| 15 | Rượu và dung môi | 2 | Ethanol, Methanol |
| 16 | Khí độc và chất độc vô cơ | 2 | Carbon monoxide, Cyanide |
| 17 | Alkaloid thực vật và chất kích thích | 4 | Strychnine, Tetrahydropalmatine, Caffeine, Cotinine |

**Tổng: 68 chất, 17 nhóm.** (Đã tách nhóm 15 cũ thành hai nhóm riêng theo quyết định P4.)

### Nhãn phụ đề xuất

Dùng để lọc chéo, một chất có thể mang nhiều nhãn:

- **Chất ma túy** — Methamphetamine, MDMA, Cathinone, Ketamine, THC, Morphine, Codeine, Methadone
- **Thuốc bảo vệ thực vật** — 12 chất thuộc nhóm 13 và 14
- **Phân loại độc tính WHO** — các chất có ghi nhóm Ia / Ib / II / III trong tài liệu (Sulfotep Ia; Abamectin, Strychnine Ib; Cypermethrin, Fenobucarb, Profenofos, Thiamethoxam, Chlorfenapyr, Emamectin, Paraquat, 2,4-D II; Metolachlor, Pyridaben III)
- **Có ngưỡng nồng độ trong máu** / **Chưa có ngưỡng** — lọc nhanh khi cần đối chiếu kết quả xét nghiệm
- **Ức chế hô hấp**, **Loạn nhịp tim**, **Co giật**, **Hôn mê** — theo biểu hiện gây tử vong được mô tả trong phần cơ chế

### Quyết định (đã chốt 09/11/2026)

- [x] **P1** — Phenobarbital: nhóm **"An thần, giải lo âu, gây ngủ"**. Mang thêm nhãn phụ "Chống động kinh".
- [x] **P2** — Ketamine: nhóm **"Chất ma túy và chất gây ảo giác"**. Mang thêm nhãn phụ "Thuốc mê".
- [x] **P3** — Tetrahydropalmatine: nhóm **"Alkaloid thực vật và chất kích thích"**. Mang thêm nhãn phụ "An thần, gây ngủ".
- [x] **P4** — Tách riêng **"Khí độc và chất độc vô cơ"** (Carbon monoxide, Cyanide) khỏi **"Rượu và dung môi"** (Ethanol, Methanol). Tổng còn 17 nhóm.
- [x] **P5** — Tạm theo cách phân loại này. Có thể đổi tên nhóm về sau mà không phải làm lại dữ liệu.

---

## Phần 2 — Tên gọi khác

### Tên gọi khác nằm ở đâu

Mình đề xuất **không chèn vào nội dung** mà để riêng, vì bạn đã chốt là app chỉ trình bày đúng những gì tài liệu có.

Cụ thể:

1. **Trong tệp dữ liệu**, mỗi chất có một trường riêng tên là `tenKhac`, tách biệt hẳn với phần nội dung chuyên môn do bác sĩ Uy viết.
2. **Trên màn hình chi tiết của chất**, tên gọi khác hiện thành một dòng chữ nhỏ ngay dưới tên chất, có nhãn ghi rõ "Tên gọi khác (do người làm app bổ sung để tra cứu)". Phần nội dung cơ chế, ngưỡng, tài liệu tham khảo ở dưới vẫn **nguyên văn** tài liệu.
3. **Khi sao chép** nội dung một chất để dán vào bản giám định, phần tên gọi khác **không được chép theo**. Chỉ chép tên chất và nội dung gốc.

Nghĩa là tên gọi khác chỉ đóng vai trò giúp tìm ra chất, không trộn vào nội dung chuyên môn.

### Tìm kiếm như thế nào

Ô tìm kiếm tìm cùng lúc trên 4 vùng, theo thứ tự ưu tiên:

1. Tên chất — gõ `diaz` ra Diazepam
2. Tên gọi khác — gõ `seduxen` hoặc `ma túy đá` cũng ra đúng chất
3. Tên nhóm — gõ `trừ sâu` ra cả 9 chất trong nhóm
4. Nội dung cơ chế và triệu chứng — gõ `GABA` ra các benzodiazepine và barbiturate; gõ `xoắn đỉnh` ra Trazodone

Gõ có dấu hay không dấu đều được, giống app TT22. Gõ `co giat` cũng ra kết quả như `co giật`.

Kết quả nào khớp tên chất sẽ xếp trên, khớp nội dung xếp dưới, và có ghi rõ "khớp ở phần cơ chế" để bạn biết vì sao nó hiện ra.

### Danh sách tên gọi khác đề xuất

Gồm 3 loại: tên tiếng Việt thường dùng, tên biệt dược phổ biến ở Việt Nam, và tên viết tắt hoặc tên hóa học. Nhờ bạn và bác sĩ Uy duyệt, nhất là phần biệt dược, vì tên biệt dược thay đổi theo thời gian.

| Chất | Tên gọi khác đề xuất |
|---|---|
| Methamphetamine | ma túy đá, hàng đá, meth, ice |
| MDMA | thuốc lắc, ecstasy, kẹo |
| Cathinone | khat, muối tắm, lá khat |
| Ketamine | ke, thuốc mê ketamin |
| Tetrahydrocannabinol | THC, cần sa, bồ đà, tài mà, marijuana |
| Morphine | morphin |
| Codeine | codein |
| Methadone | methadon |
| Tramadol | tramadol, Ultracet |
| Meperidine | pethidine, pethidin, Dolargan |
| Diazepam | Seduxen, Valium, diazepam |
| Alprazolam | Xanax |
| Bromazepam | Lexomil, Lexotan |
| Midazolam | Dormicum, Hypnovel |
| Prazepam | Lysanxia |
| Phenobarbital | Gardenal, luminal, phenobarbital |
| Clozapine | Leponex |
| Olanzapine | Zyprexa |
| Quetiapine | Seroquel |
| Risperidone | Risperdal |
| Amitriptyline | Elavil, amitriptylin |
| Sertraline | Zoloft |
| Trazodone | Trittico |
| Venlafaxine | Effexor |
| Carbamazepine | Tegretol, carbamazepin |
| Phenytoin | Dilantin, phenytoin |
| Levetiracetam | Keppra |
| Acetaminophen | paracetamol, Panadol, Efferalgan, Hapacol |
| Ibuprofen | Brufen, Advil |
| Metoprolol | Betaloc, Egilok |
| Propranolol | Dorocardyl, Inderal |
| Lidocaine | lidocain, xylocaine, lignocaine |
| Sildenafil | Viagra |
| Warfarin | Coumadin, thuốc chống đông kháng vitamin K |
| Theophylline | theophyllin, Theostat |
| Dextromethorphan | DXM, Atussin, thuốc ho |
| Guaifenesin | guaifenesin, Terpin Codein |
| Terpin | terpin hydrat, Terpicod |
| Chlorpheniramine | chlorpheniramin, clorpheniramin |
| Cetirizine | cetirizin, Zyrtec |
| Clindamycin | Dalacin |
| Sulfamethoxazole | Bactrim, Biseptol, cotrimoxazol |
| Trimethoprim | Bactrim, Biseptol, cotrimoxazol |
| Metronidazole | metronidazol, Flagyl, Klion |
| Fluconazole | fluconazol, Diflucan |
| Omeprazole | omeprazol, Losec, Omez |
| Metoclopramide | metoclopramid, Primperan |
| Metformin | Glucophage, metformin |
| Abamectin | avermectin, thuốc trừ sâu sinh học |
| Emamectin | emamectin benzoate |
| Cypermethrin | cypermethrin, pyrethroid |
| Fenobucarb | BPMC, Bassa |
| Profenofos | Selecron |
| Sulfotep | TEDP |
| Thiamethoxam | Actara |
| Chlorfenapyr | Rampage, Secure |
| Pyridaben | Nexter |
| Paraquat | Gramoxone, thuốc diệt cỏ cháy |
| 2,4-D | 2,4-Dichlorophenoxyacetic acid, thuốc diệt cỏ 2,4-D |
| Metolachlor | Dual |
| Ethanol | rượu, cồn, ethyl alcohol, BAC, nồng độ cồn |
| Methanol | cồn công nghiệp, methyl alcohol, rượu methanol |
| Carbon monoxide | CO, khí than, khí CO, ngạt khí |
| Cyanide | xyanua, cyanua, CN, muối xyanua |
| Strychnine | mã tiền, hạt mã tiền, strychnin |
| Tetrahydropalmatine | THP, bình vôi, củ bình vôi, rotundin |
| Caffeine | cà phê, cafein |
| Cotinine | nicotine, thuốc lá, chất chuyển hóa nicotine |

### Quyết định (đã chốt 09/11/2026)

- [x] **T1** — **Giữ tên biệt dược.**
- [x] **T2** — **Giữ tên lóng** của ma túy.
- [x] **T3** — **Giữ nguyên**: Cotinine vẫn có tên gọi khác là "nicotine". App sẽ hiện ghi chú nhỏ "cotinine là chất chuyển hóa của nicotine, không phải nicotine" để tránh nhầm.
- [x] **T4** — **Đồng ý**: gõ "Bactrim" ra cả Sulfamethoxazole và Trimethoprim.
