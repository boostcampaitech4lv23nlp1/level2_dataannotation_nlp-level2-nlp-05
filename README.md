# Relation Extraction Data Making

## Table of Content

* [🪐 Work Description](#Work)
* [💾 Dataset Description](#dataset)
* [🗄 Annotation Procedure](#-annotation-procedure-)
* [⚙️ Model & Train](#%EF%B8%8F-model--train)
* [💻 Result](#Result)

</br>

## 🪐 Work Description <a name='Work'></a>

관계 추출(Relation Extraction)은 문장의 단어(Entity)에 대한 속성과 관계를 예측하는 문제입니다. <br>
이번 작업은 관계 추출 데이터 세트를 직접 만들어 보는 작업이며 대상이 되는 주제는 **"태양계 형성과 진화"** 입니다.

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
  - `PERSON(PER)` 
    - 사람을 의미한다. 본 과제에서는 사람 이름과 신 이름으로 제한한다.
  - `CELESTIAL OBJECT(CLO)`
    - 천체를 의미한다. https://ko.wikipedia.org/wiki/천체의 천체, 가스 행성,떠돌이 별, 붙박이별
  - `CONCEPT(CPT)`
    - 법칙, 이론, 개념을 의미한다. 이때 책 이름과 같이 특정 개념을 나타내는 것이 아닌 경우는 제외한다. 또한 위키피디아에 문서로 등장하지 않는 경우 제외한다.
  - `DATE(DAT)`
    - 시기를 의미한다. “1920년”, “19세기” 등 특정 시점이나 “45년 전”과 같이 특정 시기를 의미하는 단어로 제한한다.
  - `ELEMENT(ELM)` 
    - 원소, 물, 암석 등의 물질을 의미한다. 대기와 같이 영역은 제외한다.
  - `METRIC(MET)` 
    - 온도, 무게, 밀도, 자전주기 등 한 물체의 수치적인 특성을 의미한다. 숫자와 단위가 동시에 들어간 경우로 제한한다. 상대적인 수치는 제외한다.
 
 * 정의된 관계(Relation)
    - `no_relation`
      - no_relation
    - `clo:revolves`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-CLO>`
      - `<SUBJ-CLO>`가 `<OBJ-CLO>`를 공전할 때 또는 <SUBJ-CLO>가 <OBJ-CLO>의 위성 혹은 행성일 때 태깅. 
      - <OBJ-CLO: 토성> 주위를 불규칙하게 도는 <SUBJ-CLO: 히페리온>이나 ..
  
    - `clo:exists_in`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-CLO>`
      - `<SUBJ-CLO>`가 `<OBJ-CLO>`에 위치하는 경우 태깅 (물리적 위치 기준)
      - <SUBJ-CLO: 명왕성>은 <OBJ-CLO: 카이퍼 대>에 있는 왜행성이다.
  
    - `clo:contains`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-CLO>`
      - `<SUBJ-CLO>`의 개념이 `<OBJ-CLO>`의 개념을 포함하는 경우 태깅 (OBJ는 SUBJ이다 -> SUBJ는 OBJ이다는 아님)
      - <SUBJ-CLO: 성운>의 예는 <OBJ-CLO: 장미 성운> 또는 펠리칸 성운이다.

    - `clo:turn_into`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-CLO>`
      - `<SUBJ-CLO>`가 `<OBJ-CLO>`로 변화했을 경우 태깅 (SUBJ가 과거, OBJ가 미래)
      - <OBJ-CLO: 항성>은 수소 및 헬륨, 기타 중원소로 이루어진 <SUBJ-CLO: 성간 구름>이 붕괴하면서 탄생한다.

    - `clo:alias_of`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-CLO>`
      - `<SUBJ-CLO>`가 `<OBJ-CLO>`의 별칭일 경우 태깅 (OBJ는 SUBJ이다, SUBJ는 OBJ이다 둘 다 성립해야 함)
      - 또한 <SUBJ-CLO:토성>은 <OBJ-CLO: "Jewel of the Solar System"(태양계의 보석)>이라는 별명도 가지고 있다.
  
    - `clo:composed_of`
      - Entity :  `<SUBJ-CLO>` - `<OBJ-ELM>`
      - `<SUBJ-CLO>`가 `<OBJ-ELM>`로 이루어졌을 때(구성되었을 때) 태깅
      - <SUBJ-CLO:태양>과 가스 행성(목성, 토성, 천왕성, 해왕성) 들도 <OBJ-ELM: 수소>와 헬륨이 전체의 대부분을 차지하고 있다.
  
    - `met:feature_of`
      - Entity :  `<SUBJ-MET>` - `<OBJ-CLO>`
      - `<SUBJ-MET>`가 `<OBJ-CLO>`의 수치적 특성일 때(크기, 온도, 속도, 밀도 등) 태깅
      - <OBJ-CLO:수성> 평균 온도는 <SUBJ-MET:452.5K>이다.
  
    - `per:propose`
      - Entity :  `<SUB-PER>` - `<OBJ-CON>`
      - 어떤 사람(PER)이 개념, 이론, 법칙, 현상 등을 제안/제시했을 때 태깅
      - 1915년, <SUBJ-PER:알베르트 아인슈타인>이 <OBJ-CON:일반상대론>을 고안하여 …
 
    - `dat:date_of_discovery`
      - Entity :  `<SUBJ-DAT>` - `<OBJ-CLO>`
      - `<SUBJ-DAT>`가 `<OBJ-CLO>`의 발견 날짜일 때(년도, 세기, 연월일, ~년 전 등) 태깅
      - <SUBJ-DAT: 964년>에는 페르시아 천문학자 알 수피가 <OBJ-CLO: 안드로메다>를 발견하였다.</br></br>
      
  - Dataset

| Relation Class            | train(ratio)                    |valid(ratio)    | test(ratio) |
| ------------------ | ----------------------- |-------|--------------- |
| no:relation | 316(0.38)|39(0.39 |39(0.39) |
| clo:composed_of |127(0.15) |15(0.15) |15(0.15) |
| clo:contains | 80(0.09)|10(0.10) |10(0.10) |
| clo:exists_in |66(0.08) |8(0.08) |8(0.08) |
| clo:revolves |53(0.06) |7(0.07)|7(0.07)|
| clo:turn_into |29(0.03) |3(0.03)|4(0.04)|
| clo:alias_of | 17(0.02)|2(0.02)|2(0.02)|
| met:feature_of | 70(0.08)|8(0.08)|8(0.08)|
| per:propose |37(0.04) |5(0.05) |4(0.04)|
| per:origin_of | 10(0.01)|1(0.01)|1(0.01)|
| dat:date_of_discovery | 15(0.01)|2(0.02)|2(0.02)|
| **Total**|**820**|**100**|**100**|

  details : [관계 추출 태스크 가이드라인](https://github.com/boostcampaitech4lv23nlp1/level2_dataannotation_nlp-level2-nlp-05/blob/main/files/NLP-05%EC%A1%B0%20KLUE-RE%20%EA%B4%80%EA%B3%84%20%EC%B6%94%EC%B6%9C%20%ED%83%9C%EC%8A%A4%ED%81%AC%20%EA%B0%80%EC%9D%B4%EB%93%9C%EB%9D%BC%EC%9D%B8.docx.pdf)
<br><br>

## 🗄 Annotation Procedure <a name='Procedure'></a>
  - 데이터 전처리(애매모호한 문장 삭제 및 수정)
  - Pilot tagging(tagging 결과 피드백 반영)
  - tagtog과 google spread sheet를 활용하여 tagging 실행
  - IAA Score 산출 : **Fleiss` Kappa = 0.85**
<br>

## ⚙️ Model & Train<a name='Model'></a>

  - Klue/Roberta-large로 해당 데이터 학습
  
  | model            | f1-micro                   |auprc    |
| ------------------ | ----------------------- |-------|
| klue/roberta-small 5 epoch| 61.78 | 63.99 |
| klue/roberta-small 9 epoch | 74.07 | 63.05 |
| klue/roberta-large 5 epoch| 69.92 | 68.88 |
| klue/roberta-large 10 epoch| 66.15 | 58.52 |


## 💻 Report <a name='Result'></a>

  제출 리포트 : [링크](https://github.com/boostcampaitech4lv23nlp1/level2_dataannotation_nlp-level2-nlp-05/blob/main/guideline/%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%A0%9C%EC%9E%91_NLP_%ED%8C%80%20%EB%A6%AC%ED%8F%AC%ED%8A%B8_5%EC%A1%B0.pdf)
<br><br>
