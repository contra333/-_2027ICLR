# 0628 논문 뼈대 초안

이 폴더는 ICLR 2027 제출 준비용 초안을 ICLR 2026 공식 LaTeX 양식으로 작성하기 위한 작업 공간입니다.

## 빠른 컴파일

```bash
cd $REPO_ROOT
make
```

생성 결과는 `main.pdf`입니다.

Overleaf처럼 파일을 저장할 때마다 자동 컴파일하려면:

```bash
make watch
```

보조 파일만 정리하려면:

```bash
make clean
```

PDF까지 포함해 완전히 정리하려면:

```bash
make cleanall
```

## 주요 파일

- `main.tex`: 논문의 진입점입니다. 제목, 익명 제출 설정, 섹션 순서를 관리합니다.
- `sections/`: abstract, introduction, method, experiments 등을 나눠 작성합니다.
- `tables/`: 표 LaTeX 파일을 둡니다.
- `figures/`: 논문에 포함할 생성된 그림 파일을 둡니다. 실험 plot은 PDF 벡터 출력을 기본으로 합니다.
- `scripts/`: `results/processed/`의 CSV/JSON을 읽어 `figures/*.pdf`를 생성하는 재현 가능한 Python 스크립트를 둡니다.
- `results/raw/`: 원본 실험 패키지, seed별 로그, metadata를 보존합니다.
- `results/processed/`: 논문 table/figure에 바로 쓰는 정리된 CSV/JSON을 둡니다.
- `references.bib`: 본인 논문 참고문헌을 넣는 BibTeX 파일입니다.
- `iclr2026_conference.sty`: ICLR 2026 공식 스타일 파일입니다. 수정하지 않는 것이 좋습니다.
- `iclr2026_conference.bst`: ICLR 2026 공식 bibliography 스타일입니다.

## 작성 순서 추천

1. `main.tex`의 `\title{...}`를 임시 논문 제목으로 바꿉니다.
2. `sections/00_abstract.tex`에 한 문단짜리 가설과 결과 요약을 씁니다.
3. `sections/01_introduction.tex`의 contribution bullet을 실제 주장으로 바꿉니다.
4. `sections/03_method.tex`에서 방법의 핵심 수식 또는 알고리즘을 정합니다.
5. 원본 실험 결과는 `results/raw/`에 보존하고, 논문용 요약 CSV/JSON은 `results/processed/`에 둡니다.
6. `scripts/`의 Python 스크립트로 `results/processed/`를 읽어 `figures/*.pdf`를 생성합니다.
7. `sections/04_experiments.tex`와 `tables/main_results_plan.tex`에 필요한 실험, figure, table 계획을 적습니다.
8. 관련 논문은 `references.bib`에 추가하고 본문에서 `\citep{key}` 또는 `\citet{key}`로 인용합니다.

## 제출 양식 주의

- 현재는 제출 초안 기준이므로 `main.tex`의 `\iclrfinalcopy`는 주석 처리된 상태로 둡니다.
- ICLR 2026 초기 제출 기준 main text page limit은 9 pages였습니다. 2027 제출 전에는 반드시 ICLR 2027 Author Guide에서 최신 style file과 page limit을 다시 확인해야 합니다.
- Double-blind 제출을 위해 PDF에 저자 정보가 보이지 않게 유지합니다.
- 공식 스타일 파일(`.sty`, `.bst`)은 임의로 수정하지 않습니다.

공식 참고 경로:

- ICLR 2026 Author Guide: https://iclr.cc/Conferences/2026/AuthorGuide
- ICLR Master Template GitHub: https://github.com/ICLR/Master-Template
