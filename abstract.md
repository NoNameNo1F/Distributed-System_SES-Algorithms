Hệ Thống quản lý tập tin - File Manager System

I. Giới thiệu - Introduction

- Thiết kế 5 máy (1 cmd = 1 system) - Design for N-process
- Mỗi máy có 1 thư mục (folder) - cho phép các máy khác có thể mount()

II. Ideas

- 5 Máy - Mỗi máy có 1 folder(Dir1,Dir2,...) là các thư mục chính của mỗi máy
- Trong đó, DirA của máy A có thể tạo các thư mục để chia sẻ và các máy có thể mount được
- Example:

  1.  - A tạo folder PeerA để chia sẻ cho máy khác
      - A có thể tạo folder PeerB, PeerC,... để lưu thư mục/file mà được mount từ mỗi máy cụ thể.
      - A tạo FileA bên trong folder PeerA - cho phép các máy khác cùng truy cập và đọc/ghi cùng lúc.
  2.  - Sau khi các máy đều bật lên thì các máy lần lượt mount hết các thư mục chia sẻ từ các máy còn lại.

  3.  - (prio) Phải đảm bảo tính nhất quán, Tuy nhiên mỗi máy chỉ phải quản lý 1 file duy nhất.
      - Các lệnh đọc/ghi sủ dụng SES multicast để quản lý thứ tự thực hiện.
      - Mỗi lệnh ghi chỉ ghi vài ký tự nên dữ liệu ghi chỉ trong 1 lệnh duy nhất
      - Khi YFS hoàn thành lệnh ghi thì:
        (i) => báo cho threads ghi khi xong.
        (ii) => cập nhật nội dung mới của tập tin cho các threads đang đọc.

      - Giao thức sắp xếp message, không đảm bảo tính đồng bộ - TUY NHIÊN thứ tự yêu cầu đọc/ghi được quản lý, mỗi lúc chỉ cho phép 1 thread được ghi

III. Demo + Simple deme:
=> thực thi đọc file |$cmd> Read FileA| => hiển thị nội dung FileA lên console
=> thực thi ghi file | $cmd> Write FileA hahaha| => ghi hahaha vào fileA

    + Demo 5cmd - đại diện cho 5 sites:
        ++ Mỗi sites chia sẻ 1 file - Mỗi file sẽ được truy cập bởi các site còn lại.

        ++ Mỗi site sẽ thực hiện 30 lệnh (12 ghi + 18 đọc).
        ++ Log sẽ ghi:
            ~ Tất cả các lệnh(đọc , ghi)
            ~ Vector thời gian của lệnh đó
            ~ Kết quả của lệnh.

        ++ Log file của việc ghi:
            + Ghi các thông-điệp-báo-tập-tin(chắc là tên file) bị thay đổi
            + nội-dung sau-khi thay đổi.

---

I. Tổng quát

- Mỗi 1 Site lưu 1 vector V_P có N-1 (là số mảng con của VectorClock)
- Mỗi phần tử của V_P chứa (P', t):
  - P': là id của Site đích.
  - t : vector timeStamp
- tm: là thời điểm(logic) gửi message(m)
- tPi: là thời điểm(logic) hiện tại tại Site_i

- Init thì V_P của các Site rỗng

II. Các hoạt động 1. Gửi Message - Write(Message m, timestamp tm, VectorClock V_P) - (P2, tm) không được gửi. Các message có (P2_tm) trong VP_1 chỉ được chuyển đến P2 khi mà tm < tP2 2. Điều kiện chuyển giao msg - V_M không chứa (P2, tm) thì có thể chuyển nhận gói tin này.
(P2, t) exists if tm > tP2, buffer the message

Abstract

Architecture: Client/Server or Peer - Peer Distributed
Methods:
open()
read()
write()
close()
mkdir()

1. Vector Time
2. Process
3. Message
4....
