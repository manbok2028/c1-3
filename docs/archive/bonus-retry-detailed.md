# 보너스 2 – 실패 알림 및 재시도 전략

## 1. 과제 개요

체납상담 자동화 워크플로우 실행 중 오류가 발생했을 때 관리자가 이를 확인하고 대응할 수 있도록 다음 절차를 설계하고 검증하였다.

1. Zapier가 관리자 Gmail로 실패 알림을 전송한다.
2. 관리자가 Zap History에서 오류 단계와 원인을 확인한다.
3. 입력자료 또는 Zap 설정을 수정한다.
4. 수정 후 새로운 행을 추가하여 워크플로우를 재실행한다.
5. Zap History의 `Successful` 상태, Gmail 발송 및 Google Sheets 처리상태를 확인한다.
6. 향후 상위 요금제 적용 시 `Autoreplay`를 활성화하여 일시적인 오류를 자동 재시도한다.

정상 작동 중인 Zap을 고의로 다시 중단시키지 않고, 실제 구현 과정에서 발생했던 오류 기록과 실패 알림메일을 활용하여 과제를 수행하였다.

---

## 2. 대상 워크플로우

- Zap 이름: `BONUS_AI_체납접수자동화_Zapier`
- Trigger: Google Sheets – `New Spreadsheet Row`
- AI Action: AI by Zapier
- 분기: Paths by Zapier – 긴급사건·일반사건
- 알림: Gmail – `Send Email`
- 처리 결과: Google Sheets – `Lookup Spreadsheet Row` 및 `Update Spreadsheet Row`

---

## 3. 실제 발생한 오류

일반사건 경로에서 Gmail 발송 단계가 다음 오류로 중단되었다.

```text
Recipient address required
```

오류 발생 결과:

- 일반사건 Path 조건은 통과하였다.
- Gmail 발송 단계에서 실행이 중단되었다.
- Gmail 아래의 Google Sheets 행 검색 및 K열 처리상태 업데이트 단계는 실행되지 않았다.
- 고객에게 접수 이메일이 발송되지 않았다.
- K열에 `일반접수 알림완료`가 입력되지 않았다.

---

## 4. 실패 알림 확인

Zapier는 오류 발생 후 관리자 Gmail로 다음 제목의 알림메일을 전송하였다.

```text
[ALERT] Possible error on your BONUS_AI_체납접수자동화_Zapier Zap
```

알림메일을 통해 다음 사항을 확인할 수 있었다.

- 발신자: Zapier Alerts
- 오류가 발생한 Zap: `BONUS_AI_체납접수자동화_Zapier`
- 검토가 필요한 오류 1건 발생
- Zap History에서 오류 상세를 확인할 필요가 있음

이 기능을 통해 관리자가 Zapier 화면을 계속 확인하지 않더라도 Gmail로 실패 사실을 통보받을 수 있음을 검증하였다.

---

## 5. Zap History에서 오류 원인 확인

다음 순서로 오류 상세를 확인하였다.

1. Zapier의 `Zap History`를 열었다.
2. `BONUS_AI_체납접수자동화_Zapier`의 `Errored` 기록을 선택하였다.
3. 일반사건 경로의 `Gmail – Send Email` 단계를 클릭하였다.
4. Run details에서 `Recipient address required` 오류를 확인하였다.
5. `Data in`의 `To` 항목을 확인하였다.

분석 결과 Gmail의 수신자 주소가 유효한 이메일 형식으로 전달되지 않은 것이 원인이었다.

---

## 6. 오류 원인과 수정 내용

### 6.1 오류 원인

Google Sheets의 `고객이메일` 셀에 실제 이메일 주소가 아니라 다음과 같은 안내용 문구가 입력되어 있었다.

```text
실제 본인 Gmail 주소
```

이 값에는 `@`와 이메일 도메인이 없으므로 Gmail Action이 유효한 수신자 주소로 인식하지 못하였다.

### 6.2 수정 내용

- Google Sheets의 고객이메일에는 실제 수신 가능한 Gmail 주소를 입력하였다.
- Gmail의 `To`에는 고정 문구를 입력하지 않고 다음 동적 필드를 연결하였다.

```text
1. New Spreadsheet Row → 고객이메일
```

- 수정사항을 저장한 뒤 새 버전으로 Publish하였다.
- 기존 원본 Zap과 Make 시나리오는 중복 실행을 막기 위해 OFF로 유지하였다.
- `BONUS_AI_체납접수자동화_Zapier`만 ON으로 유지하였다.

---

## 7. Retest step과 전체 재실행의 차이

Gmail 단계의 `Retest step`은 Gmail Action 한 단계만 시험한다. 따라서 시험 이메일이 도착하더라도 아래의 Google Sheets 행 검색과 K열 업데이트 단계까지 자동으로 실행되는 것은 아니다.

전체 재실행 검증 시에는 다음 원칙을 적용하였다.

- 기존 실패 행을 수정하는 것만으로는 `New Spreadsheet Row` Trigger가 다시 실행되지 않는다.
- Google Sheets의 마지막 자료 바로 아래에 완전히 새로운 행을 추가해야 한다.
- K열 처리상태는 자동화가 작성하도록 비워둔다.
- `Retest step`이나 `Test run`을 누르지 않고 새 행 입력만으로 자동실행되도록 한다.

---

## 8. 수동 재실행 전략

본 과제에서 적용한 수동 재실행 절차는 다음과 같다.

1. Zapier Alerts 이메일로 실패 사실을 확인한다.
2. Zap History에서 `Errored` 실행기록을 연다.
3. 실패한 단계의 Run details와 `Data in`을 확인한다.
4. 입력자료 또는 Zap 설정을 수정한다.
5. 수정사항을 Publish한다.
6. Google Sheets 마지막 행 아래에 새로운 테스트 행을 추가한다.
7. Zap이 새 행을 자동 감지하도록 기다린다.
8. Gmail 수신 여부를 확인한다.
9. 같은 행의 K열 처리상태를 확인한다.
10. Zap History에서 최종 상태가 `Successful`인지 확인한다.

이 절차는 영구적인 입력 오류나 설정 오류처럼 단순 자동 재시도로 해결되지 않는 문제에 적합하다.

---

## 9. 수정 후 재실행 결과

오류를 수정한 후 새로운 일반사건 행을 추가하여 전체 자동화를 다시 실행하였다.

최종적으로 다음 결과를 확인하였다.

1. Google Sheets의 새 행이 Trigger에 의해 감지되었다.
2. AI by Zapier가 상담요약과 고객안내문을 생성하였다.
3. 일반사건 Path가 실행되었다.
4. Gmail 제목 `[일반 접수] 체납 상담이 접수되었습니다`가 정상적으로 도착하였다.
5. 이메일 본문에 접수정보와 AI 생성 결과가 포함되었다.
6. 대상 행의 K열에 `일반접수 알림완료`가 자동으로 입력되었다.
7. Zap History에서 수정 후 실행이 `Successful`로 확인되었다.

이를 통해 `실패 알림 → 오류 분석 → 원인 수정 → 새 행 재실행 → 성공 확인` 절차가 정상적으로 작동함을 검증하였다.

---

## 10. Autoreplay 검토 결과

Zap History의 `Autoreplay` 스위치를 클릭하여 자동 재시도 기능을 검토하였다. 그러나 현재 이용 중인 요금제에서는 다음 안내가 표시되었다.

```text
Autoreplay
Upgrade to Activate
```

따라서 본 과제에서는 별도의 요금제 업그레이드를 진행하지 않고 수동 재실행 전략을 적용하였다.

Autoreplay는 상위 요금제에서 사용할 수 있는 기능으로, 일시적인 API 장애나 외부 서비스 중단 등으로 실패한 실행을 자동으로 다시 시도하는 데 적합하다. 다만 `Recipient address required`처럼 입력자료가 잘못된 경우에는 동일한 자료를 자동 재시도해도 다시 실패할 수 있으므로 원인 수정이 먼저 필요하다.

참고:

- [Zapier 공식 Replay 안내](https://help.zapier.com/hc/en-us/articles/8496241726989-Replay-Zap-runs)
- [Zapier 공식 Replay 제한사항](https://help.zapier.com/hc/en-us/articles/19220226086797-What-is-replay)

---

## 11. 재시도 운영 기준

| 오류 유형 | 대응 방법 |
|---|---|
| 일시적인 API 장애 | 상위 요금제 적용 시 Autoreplay로 자동 재시도 |
| Gmail·Google Sheets 연결 끊김 | 계정을 다시 연결한 후 재실행 |
| 잘못된 이메일 주소 | 고객이메일 수정 후 새 행으로 재실행 |
| 필수 입력값 누락 | 누락값 보완 후 새 행으로 재실행 |
| Zap 설정 오류 | 설정 수정 및 Publish 후 새 행으로 재실행 |
| Zap 구조가 크게 변경된 경우 | 과거 Replay 대신 새로운 테스트 행으로 전체 재실행 |

---

## 12. 제출 증빙 이미지

| 번호 | 파일명 | 증빙 내용 |
|---|---|---|
| 1 | `01_보너스2_Zapier_실패알림메일.png` | Zapier Alerts가 Gmail로 전송한 실패 알림 |
| 2 | `02_보너스2_오류원인_실행상세.png` | `Recipient address required` 오류 상세 |
| 3 | `03_보너스2_오류수정후_재실행성공.png` | 오류 수정 후 Zap History의 `Successful` 기록 |
| 4 | `04_보너스2_재시도전략_설계.png` | `Autoreplay – Upgrade to Activate` 검토 화면(선택 증빙) |

제출용 이미지에 실제 이메일 주소 등 개인정보가 표시되면 일부를 가린 후 사용한다.

---

## 13. 최종 재시도 전략

> Zap 실행 중 오류가 발생하면 Zapier Alerts가 관리자 Gmail로 실패 알림을 전송한다. 관리자는 Zap History에서 실패 단계와 오류 원인을 확인한다. 입력자료나 설정 오류를 수정한 후 Google Sheets에 새로운 재실행 행을 추가하여 워크플로우를 다시 실행하고, Zap History의 Successful 상태와 Gmail 발송 및 K열 처리상태를 확인한다. 상위 요금제 적용 시 Autoreplay를 활성화하여 일시적인 API 장애와 네트워크 오류를 자동 재시도하도록 확장한다.

---

## 14. 결론

본 보너스 과제에서는 실제로 발생한 Gmail 수신자 주소 오류를 기반으로 실패 알림과 복구 절차를 검증하였다.

Zapier Alerts를 통해 관리자에게 오류가 통보되었고, Zap History에서 오류 원인을 확인한 후 입력자료와 Gmail 매핑을 수정하였다. 이후 새로운 행으로 전체 워크플로우를 재실행하여 Gmail 발송, K열 처리상태 업데이트 및 `Successful` 실행기록을 확인하였다.

현재 요금제에서는 Autoreplay가 제한되어 수동 재실행 방식을 적용하였지만, 향후 상위 요금제에서는 일시적 장애에 대한 자동 재시도 기능을 추가할 수 있도록 운영 전략을 설계하였다.
