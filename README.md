# Codyssey C1-3 · 노코드 자동화

체납상담 업무를 Make와 Zapier로 자동화하고, 동일 워크플로우 비교와 운영 확장안을 기록하는 1년 유지보수 프로젝트입니다.

## 현재 상태

| 범위 | 상태 | 근거 |
|---|---|---|
| 프로젝트 1 · Make/Zapier 비교 구현 | 완료 | 두 도구의 전체 구성, 분기별 실행, History, 이메일·Sheets 결과 |
| 프로젝트 2 · 상태 전환 자동화 | 설계 완료 / 구현 증빙 필요 | 설계 문서는 있으나 실제 실행 캡처가 없음 |
| 보너스 1 · AI Action | 완료 | AI 생성, 이메일, Sheets, History 증빙 |
| 보너스 2 · 실패 알림·재시도 | 완료 | 실패 알림, 원인, 복구 성공, 재시도 전략 증빙 |

상세 판정은 [미션 적합성 표](docs/mission/compliance.md)를 확인하세요. 프로젝트 2 증빙이 추가되기 전에는 전체 미션을 `완료`로 표시하지 않습니다.

## 저장소 구조

```text
.
├─ docs/                 # 미션 판정, 운영 문서, 과거 상세 보고서
├─ evidence/             # 제출 증빙 이미지와 매니페스트
├─ src/codyssey_c1_3/    # 증빙 무결성 검사 도구
├─ tests/                # 표준 라이브러리 기반 테스트
├─ .github/workflows/    # 지속적 품질 검사
├─ pyproject.toml
└─ README.md
```

구조 원칙은 [저장소 운영 규약](docs/architecture/repository.md)에 정의되어 있습니다.

## 로컬 검증

Python 3.11 이상에서 외부 패키지 없이 실행됩니다.

```bash
python -m codyssey_c1_3 validate
python -m unittest discover -s tests -v
```

소스 레이아웃을 직접 실행할 때는 PowerShell에서 다음처럼 설정합니다.

```powershell
$env:PYTHONPATH = "src"
python -m codyssey_c1_3 validate
python -m unittest discover -s tests -v
```

`validate`는 매니페스트에 등록된 증빙 파일의 존재 여부와 미션 상태의 일관성을 검사합니다.

## 다음 완료 조건

프로젝트 2의 실제 Make 시나리오와 다음 실행 결과를 추가해야 합니다.

- 전체 시나리오
- 신규접수, 자료보완 대기, 담당자 지정완료, 상담종결 분기
- 중복 발송 차단
- Gmail 결과와 Sheets 최종 상태

추가 후 `evidence/manifest.toml`의 프로젝트 2 항목을 갱신하고 검증 명령을 통과시킵니다.
