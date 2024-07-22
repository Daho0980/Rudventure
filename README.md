# Rudventure
그저 평범하게 실행되는 걸 허락하지 않는 로그라이크 게임   
   
## 시작하기에 앞서   
   실행이 되지 않을 때는 파이썬 3.10.11이 설치되어 있는지 확인해주세요.

## 플레이 방법   
### Mac   
```
cd desktop; git clone https://github.com/Daho0980/Rudventure.git
```
을(를) 입력 후 'run_for_mac.command'를 클릭하여 실행   

### Windows   
```
지원 불가
```

## TODO   
- [x] curses 기반으로 겁나게 뜯어고치기   
    - 순수 curses에서 색을 다채롭게 넣는 게 엄청 귀찮고 어렵기 때문에 ansi escape code를 이해할 수 있는 모듈(cusser) 사용   
- [ ] npc 추가   
- [x] 가상환경 생성   
- [x] 각각 엔티티 마다 개별 스레드 적용   
- [ ] 더 많은 몬스터들   
- [x] 디버그 모드 제작   
- [ ] 미궁 데이터 구성 방식 변경   
- [x] 메뉴 제작   
- [x] 세이브 제작   
- [ ] 아이템 및 아이템 시스템 추가   
- [x] 인게임 로그   
- [x] 절차적 생성 방식 맵 인게임 적용 (알고리즘 : DungeonMaker.py)   