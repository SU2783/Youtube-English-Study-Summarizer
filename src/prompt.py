system_instruction = "당신은 이 세상 누구보다 받아쓰기를 잘하는 받아쓰기 마스터입니다. 이번에는 유튜브 영상을 보고 프롬프트에 맞게 내용을 적어주세요"

prompt = """유튜브를 보고 아래에 답하세요.
- 위의 유튜브 영상은 영어를 가르쳐주는 내용의 영상 입니다.
- 영상에는 영어로 된 여러 예시 문장들이 있고, 화자가 그 문장에 대한 한국어 해석과 부연 설명을 덧붙여 줍니다.
- 영상을 보고 영상에서 설명하는 영어 문장들과 그에 대한 한국어 번역을 적어주세요 (한국어 번역은 영상에서 설명한 한국어 번역 그대로 적어주세요).
- 그리고 각 영어 문장에 대해 영상에서 언급한 부연설명 그대로 적어주세요.
- 부연 설명에 대한 내용은 영상에서 설명하는 내용 그대로 적어주시면 됩니다.
- 세부 설명은 말 그대로 '세부' 설명이기 때문에 문장 
- 그리고 설명하는 영어 문장에 대한 부연 설명이 시작 되는 영상의 타임 스탬프를 적어주세요.
- 답변은 마크다운 형식으로 작성해주세요.
- 답변은 timestamp, sentence, transcription, explanation에 대한 내용이 반드시 포함 되어야 합니다.
- 아래는 답변 예시 입니다
```markdown

## 전체 문장

> I'm going to move in July next year. because that's when my contract on this place expires. Actually, I've already started looking for a new place. I've narrowed my options down to about 3, but I'm really going to take my time before I decide because I want to make sure (that) I make the best decision

---

## 세부 설명

### I'm going to move in July next year.

<summary>0:44</summary>  

> 내년 7월에 이사할 거예요.
  
- 영어에서는 'in July next year' 와 같이 시간 순서를 뒤바꿔 말하는 경우도 흔하기 때문에 이런 표현도 익숙해져야 함.  
- 우리 말에서는 '7월에 내년에' 라고하지 않지만 영어에서는 일/월/년도 순으로 얘기 하는 경우가 많음. 물론 영어에서도 'next year, in July'라고 할 수는 있음

---


### because that's when my contract on this place expires

<summary>0:55</summary>  

> 왜냐면 그 때 이 곳 계약이 끝나거든요.

- that's when 은 이전에 언급된 어떤 시점이나 시간을 가리키는 지시어. '그 때가 ~할 때이다.' 라는 표현임.
- 영어에서는 시간이나 시점을 나타내는 when 을 that's when 처럼 that 절을 사용해서 좀 더 자연스럽게 표현하는 것이 일반적임.  
- 실제로 apartment, house, office 등을 'place' 라고 많이 표현함

---


### Actually, I've already started looking for a new place

<summary>1:50</summary>  

> 사실, 이미 새 집을 찾기 시작했어요.

- 영어에서는 I've already already started ~ing 와 같이 현재완료 진행형을 사용하여 어떤 일을 이미 시작했음을 나타내는 표현을 즐겨 사용함.
- look for something 은 무언가를 찾는 과정을 얘기하고, find는 찾은 순간을 의미함. 그래서 find를 하기 위해서 look for를 먼저 해야 함.
- 새로 살 집, 이사 갈 곳을 'New place' 라고 표현할 수 있음.

---


### I've narrowed my options down to about 3

<summary>3:37</summary>  

> 제 선택지를 약 3개로 줄였는데요

- narrow 는 형용사로 ‘좁은’ 이란 의미로 많이 사용하지만, 동사로 ‘좁히다’ 라는 의미로도 자주 사용됨.
- I've narrowed my options down to ~ 는 '나의 선택지를 ~로 좁혔다' 라는 의미로 문장 전체를 외워두면 좋음.

---


### but I'm really going to take my time before I decide

<summary>5:37</summary>  

> 결정하기 전에 시간을 충분히 가지고 고민을 할거에요.

- Please take your time 이라고 말하는 것처럼, Take one's time 이란 표현은 '천천히 무언가를 (여유 있게 충분히 시간을 두고) 한다.' 라는 표현.
- I've narrowed my options down to ~ 는 '나의 선택지를 ~로 좁혔다' 라는 의미로 문장 전체를 외워두면 좋음.

---


### because I want to make sure (that) I make the best decision

<summary>7:24</summary>  

> 가장 좋은 결정을 꼭 하고 싶거든요.

- I want to make sure (that) something은 '반드시 ~ 하고 싶다' 라는 의미임.

---

```
반드시 위 예시처럼 timestamp, sentence, transcription, explanation을 모두 포함해 답변을 작성해주세요. 답변이 올바르게 작성되지 않으면 채점이 되지 않습니다.
markdown 답변 이외의 다른 설명은 필요없습니다. markdown 답변만 제출해주세요.
"""