# Relation Extraction Data Making

## Table of Content

* [🪐 Work Description](#Work)
* [💾 Dataset Description](#dataset)
* [🗄 Procedure](#Procedure)
* [⚙️ Model](#Model)
* [💻 Result](#Result)

</br>

## 🪐 Work Description <a name='Work'></a>

관계 추출(Relation Extraction)은 문장의 단어(Entity)에 대한 속성과 관계를 예측하는 문제입니다. <br>
이번 작업은 관계 추출 데이터 세트를 직접 만들어 보는 작업이며 대상이 되는 주제는 **"태양계"** 입니다.

</br>

## 💾 Dataset Description <a name='dataset'></a>
데이터 제작의 재료가 되는 원천 데이터는 한국어 위키피디아에서 크롤링을 실시하였고 '.'를 기준으로 문장을 구분함. <br>

* 대상 리스트(아래의 단어로 검색하면 나오는 위키피디아 문서 전문을 크롤링)
<pre><code>
과학/금성/달/명왕성/목성/물리학/블랙홀/성운/소행성
수성/수소/온도/왜성/위성/은하/중력/지구/천문학/천왕성/초신성
태양/태양계/토성/항성/해왕성/핵융합/행성/헬륨/화성
</code></pre>

* 정의된 개체(Entity)
  - `PERSON` - 사람 이름 <PER>
  - `LC_SPACE` - [https://ko.wikipedia.org/wiki/천체](https://ko.wikipedia.org/wiki/%EC%B2%9C%EC%B2%B4)의 천체, 가스 행성,떠돌이 별, 붙박이별  <SPC>
  - `CONCEPT` - 법칙, 이론, 명칭, (책은 제외)
  - `DATE`  - 1920년, 19세기  등 특정 시점?시기? (490년 전 은 안됨) <DAT>
  - `ELEMENT` - 원소, 물, 암석 등 물질적인 것 <ELM>
  - `TEMPERTURE` - 온도 <TMP>
  - `SIZE` - 크기 <SIZ>
  - `SHAPE` - 모양 <SHP>
 
 * 정의된 관계(Relation)
    - `no_relation`
      - no_relation
    - `PERSON` - `CONCEPT`
        - propose(제안하다):  뉴턴 - 중력 이론, 아인슈타인 - 상대성이론
            - <PER>이 <THR>을 제안/제시한 경우 태깅
            - `1915년, <알베르트 아인슈타인>이 <일반상대론>을 고안하여 중력이 빛의 운동에 영향을 미침을 보였다.`
    - `LC_SPACE` - `LC_SPACE`
        - revolves(공전하다): 지구 - 태양, 태양 - 은하, 위성 - 목성
            - <OBJ-SPC>가 <SUBJ-SPC>을/를 공전하는 또는 위성인 경우 태깅 # 순서 주의
            - `<토성> 주위를 불규칙하게 도는 <히페리온>이나, 행성의 가장 바깥 궤도를 도는 토성의 포에베 등이 예외에 속한다.`
        - contains(물리적 포함): 은하 - 항성, 태양계 - 소행성
            - <SUBJ-SPC>가 <OBJ-SPC>을/를 위치하는 경우 태깅 (물리적 위치 기준)
            - `행성 외에도 <태양계>의 구성 천체로는 <소천체>로 이루어진 띠도 있다.`
            - `카이퍼 대애 명왕성이 위치한다`
        - hierarchy(개념적 포함): 항성 - 태양, 행성 - 지구 , 소행성대 - 소행성
            - <SUBJ-SPC>가 <OBJ-SPC>을/를 포함하는 경우 태깅 (A는 B이다)
            - `성운의 예는 장미 성운 또는 펠리칸 성운이다.`
            - `처음으로 발견된 소행성은 세레스이며,`
        - turn_into(바뀌다, 변화하다):  항성 - 성간 구름
            - `<항성>은 수소 및 헬륨, 기타 중원소로 이루어진 <성간 구름>이 붕괴하면서 탄생한다.`
            - `가스로 된 코마나 꼬리가 없다는 점에서 혜성과 구분되지만, 일부 <소행성>은 과거에 <혜성>이었다.`
            - `<블랙홀>은 <항성>이 진화의 최종단계에서 폭발후 수축되어 생성된 것으로 추측되는,`
        - alias(별칭): 토성 - 태양계의 보석
            - 또한 토성은 "Jewel of the Solar System"(태양계의 보석)이라는 별명도 가지고 있다.
    - `LC_SPACE` - `ELEMENT`
        - composed_of(구성되다): 성운 - 수소, 목성의 대기 - 메테인
            - <SPC>이 <ELM>로 구성되어 있는 경우 태깅
            - `<태양>과 가스 행성(목성, 토성, 천왕성, 해왕성) 들도 <수소>와 헬륨이 전체의 대부분을 차지하고 있다.`
    - `LC_SPACE` - `METRIC`
        - size_of(~의 크기): 수성 - 2439.7km, 베토벤 분지 - 625km, 우리 은하 - 15kpc, 수성 - 452.5K, 중성자 핵 - 1천억 켈빈
            - <SPC>의 크기가 <MTR>인 경우 태깅
            - `<베토벤 분지>는 분출물 덮개와 비슷한 크기이며, 폭은 <625km>이다.`
    - `LC_SPACE` - `DATE`
        - date_of_discovery(발견한 날짜)
            - <SPC>가 <DAT>에 발견된 경우 태깅
            - `<964년>에는 페르시아 천문학자 알 수피가 <안드로메다>를 발견하였다.`
    - `LC_SPACE` - `PER`
        - originate(유래하다)
            - <SUB-SPC>가 <OBJ-PER>에서 유래한 경우 태깅 (PER은 사람 또는 신 이름)

  <br>

| Dataset            | train                    | test |
| ------------------ | ----------------------- |--------------- |
| **문장 수**        | 32470      |     7765   |
| **비율**        | 80      |     20 |


## 🗄 Procedure <a name='Procedure'></a>

## ⚙️ Model <a name='Model'></a>

  Klue/Roberta-large로 해당 데이터 학습

## 💻 Result <a name='Result'></a>
