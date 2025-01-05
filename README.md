# FastAPI Note Service

노트 작성 및 관리를 위한 RESTful API 서비스입니다.

## 주요 기능
- 사용자 관리
- 회원가입/로그인
- 사용자 정보 조회/수정/삭제
- JWT 기반 인증
- 노트 관리
- 노트 작성/조회/수정/삭제
- 태그 기능
- 페이지네이션 지원


## 기술 스택
- FastAPI
- SQLAlchemy (PostgreSQL)
- Pydantic
- JWT (인증)
- Argon2 (비밀번호 암호화)


## API 엔드포인트
### 사용자 API
```
POST /users/login - 로그인
GET /users/me - 현재 사용자 정보 조회
POST /users - 회원가입
GET /users - 사용자 목록 조회
GET /users/{user_id} - 특정 사용자 조회
PATCH /users/{user_id} - 사용자 정보 수정
DELETE /users/{user_id} - 회원 탈퇴
```

### 노트 API
```
POST /notes - 노트 작성
GET /notes - 노트 목록 조회
GET /notes/{id} - 특정 노트 조회
PUT /notes/{id} - 노트 수정
DELETE /notes/{id} - 노트 삭제
```


## 보안 기능
- Argon2 기반 비밀번호 암호화
- JWT 기반 인증
