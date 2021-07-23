# myDLP_text-based

# Overview
![image](https://user-images.githubusercontent.com/49504937/126845346-3b48accd-46aa-4361-b99d-c924bb265738.png)
# Usage
## 1. Set Target PDF
### 1.1 if not PDF
![image](https://user-images.githubusercontent.com/49504937/126535301-56333d34-0c26-44de-abea-ed5a286f842a.png)
![image](https://user-images.githubusercontent.com/49504937/126535325-88276c54-a268-421a-bbe5-eec2f34a16b3.png)

## 2-1. Send e-mail

## 2-2. Move to USB

## 2-3. Copy to USB

# Result
# Detected with Text

# Detected with OCR

# Detected Nothing

# 사용한 정규 표현식

`\b(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}\b`
주민등록번호 형식의 정규표현식

`^b\'%PDF\'$`
확장자가 아닌 시그니처 기반의 PDF 파일 업로드 검사
