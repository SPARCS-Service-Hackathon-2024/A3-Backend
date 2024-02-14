## TODO

### Day 1

- 와이어프레임
- API 명세서
    - Path, Query, Body
    - post 로그인: 이름, 생년월일
    - get 질문
        - path parameter: 질문 번호
        - body: 질문
    - post 답변
        - path parameter: 질문 번호
        - body: 유저 번호, 답변
    - 배송: 배송주소, 휴대폰 번호
- ERD
    - User
        - 이름, 생년월일, 배송주소, 휴대폰 번호, 마지막으로 답변한 문항
        - 유저 번호(이름과 생년월일의 조합)
    - Question
    - Answer 
- FastAPI로 서버 구축
- NGROK로 임시 도메인 생성
- CI/CD 구축
    - GitHub Actions
    - Docker Hub
    - Kakao Cloud
- HTTPS 설정
- GPT
    - GPT 4.0
    - Whispher
- S3 Bucket
    - 이미지 및 음성 업로드 및 다운로드
- Prompt Engineering
    - 간단한 인적사항
        - 생년월일, 고향
    - 어렸을 때 기억에 남는 에피소드
    - 그 일이 성인이 되었을 때 어떻게 영향을 미쳤는지?
    - 100문 100답 느낌으로?
    - 인생의 좌우명

### Day 2



### Day 3