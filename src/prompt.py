system_instruction = "You are the best transcription master in the world. This time, watch the YouTube video and write down the content according to the prompt."

prompt = """Watch the YouTube video and answer the following questions:
- The above YouTube video is about teaching English.
- The video contains several example sentences in English, and the speaker provides Korean translations and additional explanations for those sentences.
- Watch the video and write down the English sentences explained in the video along with their Korean translations (write the Korean translations exactly as explained in the video).
- Also, write down the additional explanations mentioned in the video for each English sentence.
- The additional explanations should be written exactly as explained in the video
- The additional explanations must be written in Korean.
- Also, write down the timestamp when the additional explanation for the English sentence starts in the video.
- There are parts where the sentences are repeated without explanation, but do not set the timeline for those parts. Set the timeline from the start of the explanation for each sentence.
- Summarize only the important parts of the explanation for each sentence.
- The answer should be written in Markdown format.
- The answer must include the timestamp, sentence, transcription, and explanation.
- Below is an example answer:
```markdown

## Full Sentence

> I'm going to move in July next year. because that's when my contract on this place expires. Actually, I've already started looking for a new place. I've narrowed my options down to about 3, but I'm really going to take my time before I decide because I want to make sure (that) I make the best decision

---

## Detailed Explanation

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
Please include the timestamp, sentence, transcription, and explanation in your answer as shown in the example above.
If the answer is not written correctly, it will not be graded.
Only submit the Markdown answer. No other explanations are needed.
"""