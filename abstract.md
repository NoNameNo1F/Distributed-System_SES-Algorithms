Hệ Thống quản lý tập tin - File Manager System

I. Giới thiệu - Introduction

- Thiết kế 5 máy (1 cmd = 1 system) - Design for N-process
- Mỗi máy có 1 thư mục (folder) - cho phép các máy khác có thể mount()

II. Ideas

- 5 Máy - Mỗi máy có 1 folder(Dir1,Dir2,...) là các thư mục chính của mỗi máy
- Trong đó, DirA của máy A có thể tạo các thư mục để chia sẻ và các máy có thể
  mount được
- Example:

  1.  - A tạo folder PeerA để chia sẻ cho máy khác
      - A có thể tạo folder PeerB, PeerC,... để lưu thư mục/file mà được mount
        từ mỗi máy cụ thể.
      - A tạo FileA bên trong folder PeerA - cho phép các máy khác cùng truy cập
        và đọc/ghi cùng lúc.
  2.  - Sau khi các máy đều bật lên thì các máy lần lượt mount hết các thư mục
        chia sẻ từ các máy còn lại.

  3.  - (prio) Phải đảm bảo tính nhất quán, Tuy nhiên mỗi máy chỉ phải quản lý 1
        file duy nhất.
      - Các lệnh đọc/ghi sủ dụng SES multicast để quản lý thứ tự thực hiện.
      - Mỗi lệnh ghi chỉ ghi vài ký tự nên dữ liệu ghi chỉ trong 1 lệnh duy nhất
      - Khi YFS hoàn thành lệnh ghi thì: (i) => báo cho threads ghi khi xong.
        (ii) => cập nhật nội dung mới của tập tin cho các threads đang đọc.

      - Giao thức sắp xếp message, không đảm bảo tính đồng bộ - TUY NHIÊN thứ tự
        yêu cầu đọc/ghi được quản lý, mỗi lúc chỉ cho phép 1 thread được ghi

III. Demo + Simple deme: => thực thi đọc file |$cmd> Read FileA| => hiển thị nội
dung FileA lên console => thực thi ghi file | $cmd> Write FileA hahaha| => ghi
hahaha vào fileA

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

II. Các hoạt động 1. Gửi Message - Write(Message m, timestamp tm, VectorClock
V_P) - (P2, tm) không được gửi. Các message có (P2_tm) trong VP_1 chỉ được
chuyển đến P2 khi mà tm < tP2 2. Điều kiện chuyển giao msg - V_M không chứa (P2,
tm) thì có thể chuyển nhận gói tin này. (P2, t) exists if tm > tP2, buffer the
message

Abstract

Architecture: Client/Server or Peer - Peer Distributed Methods: open() read()
write() close() mkdir()

1. Vector Time
2. Process
3. Message 4....

https://docs.python.org/3/library/socket.html#socket.socket.recvfrom

SYNTAX: recv(bufsize[, flags]) recv: nhận giá trị trả về là bytes object từ
nowhere gửi đến (1024, 2048): số bytes nhận

SYNTAX: recvfrom(bufsize[, flags]) recvfrom: nhận giá trị trả về là cặp (bytes,
address), bytes data nhận và địa chỉ mà data được gửi

SYNTAX: recvmsg(bufsize[, ancbufsize[, flags]]) recvmsg: nhận data, và data phụ
trợ từ socket. nếu ancillary data =0 thì ko có data phụ

SYNTAX: recvfrom_into(buffer[, nbytes[, flags]]) recvfrom_into: nhận data và ghi
vào trong buffer thay vì tạo 1 chuỗi bytes. Giá trị trả về là (nbyte, address)

SYNTAX: recv_into(buffer[, nbytes[, flags]]) recv_into: nhận nbyte trên tổng số
bytes nhận được

############################################## Khởi tạo site, site gọi hàm
send_mount_message(receiver, message_type, message)

SES: Schiper-Eggli-Sandoz Algorithm. Không cần broadcast message. £ Mỗi process
lưu 1 vector V_P kích thước N - 1, N số lượng processes. £ Mỗi phần tử của V_P
chứa (P’,t): P’ là id của process đích và t là vector timestamp. £ tm: thời điểm
(logic) gửi m £ tPi: thời điểm (logic) hiện tại tại pi £ Ban đầu, V_P rỗng
############################################## Gửi Message: p Gửi message M,
time stamped tm, cùng với V_P1 đến P2. p Thêm (P2, tm) vào V_P1. Ghi chồng lên
(P2,t), nếu có. p (P2,tm) không đc gửi. Các message có (P2,tm) trong V_P1 chỉ đc
chuyển đến P2 khi mà tm < tP2. £ Chuyển giao message p If V_M (in the message)
không chứa (P2, t), thì có thể chuyển msg này. p /_ (P2, t) exists _/ If tm >
tP2, buffer the message. (Don’t deliver). p else (tm <= tP2) deliver it
############################################## Điều kiện t ≥ tP2 nói lên điều
gì? p t is message vector time stamp. p t > tP2 -> For all j, t[j] > tP2[j] p Có
tồn tại sự kiện trong process khác mà P2’s chưa cập nhật. Vì vậy P2 quyết định
buffer the message. £ Khi t < tP2, message đc chuyển & tP2 được cập nhật với
thông tin trong V_P2 (sau phép trộn).
