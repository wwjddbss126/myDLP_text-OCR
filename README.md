# myDLP_text-based
made by BoB 10th 디지털포렌식트랙 `강정윤`, `박준성` 교육생

# Overview
해당 프로그램의 로직은 다음과 같다.
1. 선택한 파일이 pdf 파일인지 시그니처 기반으로 검사
2. 맞을 시, 이메일 전송 또는 USB로의 이동/복사할 경우 선택한 pdf 파일 내에 개인 정보가 있는지 text- based 검사 실행
3. text-based 검사 결과 검출되지 않았을 경우, image-based 검사 실행
4. 모든 행위에 대한 검사 결과는 `myDLP_Log.txt`에 저장됨
![image](https://user-images.githubusercontent.com/49504937/126845346-3b48accd-46aa-4361-b99d-c924bb265738.png)

# 사용한 정규 표현식

`\b(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}\b`
주민등록번호 형식의 정규표현식

`^b\'%PDF\'$`
확장자가 아닌 시그니처 기반의 PDF 파일 업로드 검사

`\s+`
OCR 탐지 결과에서 공백을 제거하기 위한 정규표현식

# Usage
## 1. Set Target PDF
### 1.1 if not PDF
![image](https://user-images.githubusercontent.com/49504937/126535301-56333d34-0c26-44de-abea-ed5a286f842a.png)
![image](https://user-images.githubusercontent.com/49504937/126535325-88276c54-a268-421a-bbe5-eec2f34a16b3.png)

## 2-1. open log file
코드가 실행되는 디렉터리 내에 `myDLP_Log.txt`라는 이름의 로그 파일이 저장되고, `Open Log File` 버튼을 클릭하면 해당 파일이 열린다.

![KakaoTalk_20210724_200446900](https://user-images.githubusercontent.com/56073938/126867725-75e3dfb7-bbba-4fb7-8547-fdf72bbb709f.png)
## 2-2. Send e-mail
PDF 파일 선택 후, 이메일을 보낼 `송신 주소`, `제목`, `본문`을 입력하고 `Send e-mail` 버튼을 클릭하면, 입력한 정보로 PDF 파일이 첨부된 메일이 보내진다. 이 때, 선택한 PDF 파일 내에 개인 정보 (주민번호)가 포함되어 있으면 알림을 띄운다.
![KakaoTalk_20210724_200557919](https://user-images.githubusercontent.com/56073938/126867758-191eeb4f-741f-4045-bedb-5b9b8071520a.png)
![KakaoTalk_20210724_202034902](https://user-images.githubusercontent.com/56073938/126867803-d871d127-ee5a-4811-9c9e-cfd897202dd0.jpg)
## 2-3. check PDF signeture 
![KakaoTalk_20210724_201436832](https://user-images.githubusercontent.com/56073938/126867828-6bb82176-c7eb-42f1-96d9-574fe7237477.png)
# Result
# Detected with Text
![KakaoTalk_20210724_200704598](https://user-images.githubusercontent.com/56073938/126867764-0bb969fc-4acb-4a86-b0b4-f9682384b958.png)
# Detected with OCR
![KakaoTalk_20210724_200958522](https://user-images.githubusercontent.com/56073938/126867772-aab8527d-42d3-4ce7-a97d-731aa1c06bf2.png)
# Detected Nothing
![KakaoTalk_20210724_201124419](https://user-images.githubusercontent.com/56073938/126867780-b2016530-0171-4a46-a888-aac9ae6c48ff.png)
