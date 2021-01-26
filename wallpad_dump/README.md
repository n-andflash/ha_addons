# 월패드 RS485 패킷 덤프 애드온

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

* [소개](#소개)
    + [지원 장치](#지원-장치)
* [설치](#설치)
    + [1. 준비 사항](#1-준비-사항)
* [설정](#설정)
* [지원](#지원)

## 소개

* [버전별 변경 사항](https://github.com/n-andflash/ha_addons/raw/master/wallpad_dump/LCHANGELOG.md)

* HA 환경에서 serial(USB to RS485 등)이나 socket(EW11 등) 방식으로 RS485 패킷을 확인할 수 있는 애드온입니다.
* HA 머신에 USB to RS485가 연결되어 있을 때 SerialPortMon을 사용하기 어려운 점을 개선하고자 만들었습니다.
* 언젠가는 분석 편의를 위해 주요 월패드 제조사별로 패킷을 정리 (쉼표, 줄바꿈 등) 하려고 합니다.
    * SDS의 경우에는 이 애드온 대신 SDS 월패드 애드온의 dump\_time 옵션을 쓰시면 해당 기능이 구현되어 있습니다.

## 설치

* 환경 구성에 지식이 있다면 애드온이 아닌 standalone으로도 사용하실 수 있도록 준비해 두었습니다.
    * 이 경우 run\_standalone.sh 를 한번 실행해서 options\_standalone.json 을 생성한 뒤, 적절히 수정하고 다시 run\_standalone.sh 를 실행하시면 됩니다.

### 1. 애드온 설치, 실행

1. 홈어시스턴트의 Supervisor --> Add-on store에서 우상단 메뉴( ⋮ ) 를 누른 후 "repositories" 선택합니다.
2. "Add repository" 영역에 아래 주소를 입력 후 ADD 를 누릅니다.
    1. 애드온 개발자 개인 저장소: https://github.com/n-andflash/ha_addons
3. 하단에 나타난 "Wallpad RS485 Packet Dump" 을 선택합니다.
4. "INSTALL" 버튼을 누른 후 "START" 가 나타날 때까지 기다립니다. (수 분 이상 걸릴 수 있습니다)
    1. 설치 중 오류가 발생하면 Supervisor -> System 의 System log 최하단을 확인해봐야 합니다.
5. "START" 가 보이면, 시작하기 전에 "Configuration" 페이지에서 아래 설정을 구성 후 "SAVE" 를 누릅니다.
    1. serial\_mode (EW11 사용시 socket, 그 외의 경우 serial)
    2. serial/port 혹은 socket/address
6. "Info" 페이지로 돌아와서 "START" 로 시작합니다.
    1. 첫 시작 시 회전 애니메이션이 사라질 때까지 기다려주세요.
7. "Log" 페이지에서 정상 동작하는지 확인합니다.
8. Log 페이지의 내용은 /share/wallpad_dump.log 파일에도 기록됩니다.

## 설정

### mode:
#### `serial_mode` (serial / socket)
* serial: USB to RS485 혹은 TTL to RS485를 이용하는 경우
* socket: EW11을 이용하는 경우

### serial: (serial\_mode 가 serial 인 경우)

#### `port`
* Supervisor -> System -> HARDWARE 버튼을 눌러 serial에 적혀있는 장치 이름을 확인해서 적어주세요.
* USB to RS485를 쓰신다면 /dev/ttyUSB0, TTL to RS485를 쓰신다면 /dev/ttyAMA0 일 가능성이 높습니다.
* 단, 윈도우 환경이면 COM6 과 같은 형태의 이름을 가지고 있습니다.

#### baudrate, bytesize, parity, stopbits (기본값 9600, 8, N, 1)
* 국내 대부분 월패드는 9600 8N1을 사용하며, 삼성SDS의 경우 9600 8E1을 사용합니다.
* 사용 가능한 parity: E, O, N, M, S (Even, Odd, None, Mark, Space)

### socket: (serial\_mode 가 socket 인 경우)

#### `address`
* EW11의 IP를 적어주세요.

#### port (기본값: 8899)
* EW11의 포트 번호를 변경하셨다면 변경한 포트 번호를 적어주세요.

### log:
#### to\_file (true / false)
* false로 설정하면 로그를 파일로 남기지 않습니다.
* 로그는 매번 실행시 새 파일로 저장되며, 기존 로그는 파일명에 숫자를 붙여 100개까지 보관됩니다.

#### filename (기본값: /share/wallpad\_dump.log)
* 로그를 남길 경로와 파일 이름을 지정합니다.

## 지원

* 정확한 지원을 위해서, 글을 쓰실 때 아래 사항들을 포함해 주세요.
    * 실행 로그 (HA의 share 폴더에 최신 로그 파일 (숫자가 붙지 않은 wallpad\_dump.log 파일) 이 있습니다)
    * Configuration 페이지 내용

[HomeAssistant 네이버 카페 (질문, 수정 제안 등)](https://cafe.naver.com/koreassistant)

[Github issue 페이지 (버그 신고, 수정 제안 등)](https://github.com/n-andflash/ha_addons/issues)

## 면책조항 (Disclaimer)

* 이 애드온은 무상으로 제공되므로 정확성이나 안정성 등 어떠한 보증도 제공하지 않습니다.
* 이 애드온은 오픈소스로 실행 코드와 함께 배포되므로 코드 및 동작에 대한 확인 책임은 사용자에게 있습니다.
* 기타 사항은 GPLv3를 따릅니다. [전문보기](https://github.com/n-andflash/ha_addons/raw/master/sds_wallpad/LICENSE)

---

![카카오톡 후원 QR코드](https://github.com/n-andflash/ha_addons/raw/master/sds_wallpad/images/donation_kakao.png)
* 카카오톡 후원 코드: https://qr.kakaopay.com/281006011000008548744237 (모바일에서만 가능)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
