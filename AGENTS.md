# Project Instructions

이 저장소는 Ubuntu 로컬 환경에서 ICLR 형식의 LaTeX 논문 초안을 편집하는 작업 공간이다. 사용자는 웹사이트 GPT를 논문 설계와 논리 검토를 위한 "두뇌"로 사용하고, Codex는 이 로컬 폴더에서 실제 편집과 실행을 담당한다.

## Current Project Context

- 작업 폴더: `$REPO_ROOT`
- 논문 진입점: `main.tex`
- 본문 섹션: `sections/*.tex`
- 표 위치: `tables/`
- 그림 위치: `figures/`
- figure 생성 스크립트 위치: `scripts/`
- 원본 실험 결과 위치: `results/raw/`
- 논문용 가공 결과 위치: `results/processed/`
- 참고문헌: `references.bib`
- 컴파일 기본 명령: `make`
- 결과 PDF: `main.pdf`

이 프로젝트는 현재 논문 뼈대 초안 단계다. 글의 논리 구조, contribution, 실험 구성, table/figure 설계는 계속 바뀔 수 있다.

## Collaboration Model

웹사이트 GPT의 주 역할은 논문의 전략적 판단이다.

- 문제정의, 핵심 주장, contribution 정리
- abstract/introduction/method/experiments/discussion의 논리 흐름 설계
- 실험 결과 해석과 추가 실험 제안
- 어떤 table과 figure가 필요한지 제안
- caption 방향, ablation 구성, baseline/metric/dataset 구성 제안
- 리뷰어 관점의 약점, 반박, 보강 포인트 제안

Codex의 주 역할은 로컬 실행이다.

- GPT 또는 사용자가 준 논문 설계안을 실제 LaTeX 파일에 반영
- `sections/*.tex`, `tables/*.tex`, `figures/*`, `references.bib` 편집
- LaTeX table 작성 및 정리
- `results/processed/*.csv` 등 정리된 실험 결과를 읽는 재현 가능한 Python 스크립트 작성
- matplotlib, seaborn, pandas, numpy 등을 활용한 학술용 figure 생성
- 이 작업공간에는 figure 생성용 가상환경 `${HOME}/envs/research`가 이미 있으며, `matplotlib`, `pandas`, `numpy`가 설치되어 있다. 패키지 설치를 시도하기 전에 `$RESEARCH_PYTHON` 또는 `${HOME}/envs/research/bin/python`을 우선 사용하고, Matplotlib 실행 시 필요하면 `MPLCONFIGDIR=/tmp/matplotlib-cache`처럼 쓰기 가능한 캐시 경로를 지정한다.
- 생성 스크립트는 `scripts/`에 두고, 논문에 포함할 산출물은 `figures/`에 저장
- 기본 산출물은 벡터 형식 PDF로 저장하고, SVG는 필요할 때 보조 산출물로 유지하며, PNG/JPG는 실제 raster 이미지가 필요한 경우에만 사용
- LaTeX 컴파일, BibTeX, package, syntax, cross-reference 에러 해결
- `make` 또는 필요한 LaTeX 명령으로 결과 확인

## How To Use GPT Output

사용자가 웹사이트 GPT의 제안을 붙여넣으면, 그것을 단순 명령으로만 보지 말고 논문 설계 메모로 해석한다.

- 제안이 현재 파일 구조와 맞는지 먼저 확인한다.
- 내용이 모호하면 합리적인 기본값으로 구체화하되, 논문 주장이나 실험 결과를 지어내지 않는다.
- GPT 제안이 LaTeX 형식, 파일 구조, 실제 데이터와 충돌하면 Codex가 실무적으로 조정한다.
- 논리적으로 약하거나 과장된 주장은 그대로 쓰지 말고 더 방어 가능한 표현으로 바꾼다.
- 사용자가 명시적으로 원하지 않는 한 공식 스타일 파일(`iclr2026_conference.sty`, `.bst`, vendored style files)은 수정하지 않는다.

## Writing And Editing Principles

- 논문은 ICLR-style ML 논문을 기준으로 학술적이고 간결한 문체를 유지한다.
- 각 섹션은 "무엇을 주장하는가"와 "어떤 증거가 뒷받침하는가"가 분명해야 한다.
- 실험 결과, 수치, citation, dataset, baseline은 사용자가 제공한 정보나 로컬 파일에 있는 정보만 사용한다.
- 아직 검증되지 않은 내용은 단정하지 말고 placeholder, TODO, or cautious wording으로 둔다.
- double-blind 제출 맥락을 유지한다. 저자 정보나 식별 가능한 표현을 임의로 추가하지 않는다.
- 기존 섹션 분할과 LaTeX 스타일을 우선 따른다.

## Figures And Tables

- Figure는 논문 주장을 보강하는 목적이 분명해야 한다.
- 실험 기반 figure는 `results/raw/`의 원본 로그를 직접 건드리지 말고, `results/processed/`의 정리된 CSV/JSON을 입력으로 삼는다.
- Figure 생성은 Python `matplotlib`/`seaborn` + `pandas` 기반 스크립트를 기본 방식으로 한다.
- 각 figure에는 재실행 가능한 생성 스크립트를 `scripts/` 아래에 남기고, 스크립트 안에는 입력 데이터 경로와 출력 figure 경로를 명시한다.
- 선 그래프, bar plot, ablation plot, scatter plot, metric trade-off plot 등 실험 figure는 기본적으로 `figures/*.pdf` 벡터 산출물로 저장한다.
- SVG는 PDF 변환 품질 확인이나 편집 가능한 보조 산출물이 필요한 경우에 함께 저장할 수 있다.
- PNG/JPG는 예시 이미지, qualitative grid 등 원래 raster 데이터가 필요한 경우에만 사용한다.
- PGFPlots/TikZ는 수식 중심의 단순 conceptual plot이나 LaTeX-native schematic에만 제한적으로 사용하고, CSV 기반 ML 실험 figure에는 Python 스크립트를 우선한다.
- `plt.style.use(...)`, `.mplstyle`, `rcParams`, 또는 `seaborn.set_theme(..., context="paper")`를 사용해 figure 간 font size, line width, marker size, color palette를 일관되게 유지한다.
- Matplotlib의 `usetex`/PGF backend는 LaTeX 폰트와 수식 일관성이 꼭 필요한 경우에만 사용한다. 일반 실험 plot은 PDF 출력으로 충분하면 과도하게 복잡하게 만들지 않는다.
- GUI 도구로 수동 보정한 내용은 최종 상태가 다시 코드로 재현될 수 있어야 한다.
- Figure 작성 규칙은 `docs/figure_guidelines.md`를 따른다.
- 그림 내부에 큰 제목을 넣지 말고, 핵심 메시지는 LaTeX caption에서 설명한다.
- 그림 내부 텍스트는 최종 출력 기준 최소 7 pt를 유지하고, 보통 label/tick/legend는 7--8 pt, 짧은 panel heading은 8--9 pt를 목표로 한다.
- 색상만으로 의미를 전달하지 말고 marker, line style, label, grouping 등으로 같은 정보를 중복 표현한다.
- drop shadow, gradient, 3D 효과, 장식적 투명도는 사용하지 않는다.
- Table은 `booktabs` 스타일을 사용하고, 과도한 세로선이나 복잡한 장식은 피한다.
- caption은 단순 설명이 아니라 해당 figure/table이 뒷받침하는 핵심 메시지를 드러내야 한다.

## Verification

- LaTeX 관련 변경 후에는 가능한 한 `make`로 컴파일을 확인한다.
- figure/table을 추가하면 `main.pdf`에 정상적으로 포함되는지 확인한다.
- 컴파일이 실패하면 에러 로그를 읽고 원인을 좁힌 뒤 수정한다.
- 실행하지 못한 검증은 최종 응답에 명확히 말한다.

## Flexibility

이 파일은 품질을 높이기 위한 프로젝트 맥락이다. 사용자의 최신 지시와 실제 논문 품질 판단이 우선한다. 여기의 지침 때문에 더 좋은 논리 구조, 더 적절한 실험 설계, 더 명확한 표현을 포기하지 않는다.
