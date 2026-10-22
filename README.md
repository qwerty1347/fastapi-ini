# fastapi-starter

새 FastAPI 프로젝트를 시작할 때 복사해서 쓰는 뼈대예요. claude-admin 백엔드 구조를 바탕으로 만들었어요.

- FastAPI, SQLAlchemy 2를 써요. API는 비동기(aiomysql), Alembic·시드는 동기(pymysql)예요.
- MySQL을 쓰고 시각은 KST로 저장해요.
- 패키지는 uv로 관리하고, Docker는 dev와 prod 이미지를 따로 만들어요.
- `items`는 예제 도메인이에요. 새 기능은 이 파일들을 복사해서 만들어요.

## 구조
```
.
├─ app/
│  ├─ main.py              # FastAPI 앱, lifespan(종료 시 DB 풀 정리), CORS, 예외 핸들러 등록
│  ├─ utils.py             # 두 곳 이상에서 쓰는 순수 함수
│  ├─ core/                # 앱 기반 기능
│  │  ├─ config.py         #   설정 (.env → Settings), database_url_sync
│  │  ├─ clock.py          #   현재 시각은 여기서만 (now: KST, utcnow: 외부 연동)
│  │  ├─ db.py             #   Base(제약조건 이름 규칙), KSTDateTime, 비동기·동기 엔진/세션
│  │  └─ errors.py         #   AppError, 모든 실패를 ApiError 형식으로, error_responses()
│  ├─ api/
│  │  ├─ deps.py           #   AsyncSessionDep, SessionDep
│  │  ├─ main.py           #   /api 라우터 (공통 500 문서화)
│  │  └─ v1/routes/        #   버전별 라우트. 요청을 받고 services 를 부르기만 함
│  ├─ schemas/             # 요청·응답 (Pydantic). JSON 은 camelCase
│  │  └─ common.py         #   CamelModel, ApiResponse[T], ApiError, FieldError
│  ├─ models/              # DB 테이블 (SQLAlchemy). __init__.py 에 전부 import (Alembic 용)
│  ├─ crud/                # 테이블 단위 쿼리. commit 하지 않음
│  ├─ services/            # 기능 단위 로직: crud 조합, 계산, commit, AppError
│  └─ seeds/               # 개발·데모용 더미 데이터 (python -m app.seeds). 운영에서 실행 금지
├─ alembic/                # 마이그레이션 (env.py 가 settings 와 app.models 를 읽음)
├─ tests/                  # DB 없이 도는 공통 테스트 (에러 형식, OpenAPI, 시각, utils)
├─ .docker/                # Dockerfile(dev/prod), entrypoint.sh(SERVICE_TYPE 으로 실행 명령 선택)
├─ compose.yaml            # 공통 (fastapi + mysql)
├─ compose.override.yaml   # 개발: 자동 합쳐짐. 소스 마운트, hot reload, 포트
└─ compose.prod.yaml       # 배포
```

## 요청 흐름
```
라우트 (api/v1/routes/items.py)    요청 검증, 응답 감싸기 ApiResponse(data=...)
  → 서비스 (services/item.py)      crud 조합, commit, 없으면 AppError(404, "ITEM_NOT_FOUND")
    → crud (crud/item.py)          select / add / flush
      → 모델 (models/item.py)      테이블
```

## 응답 형식
```json
// 성공
{ "statusCode": 200, "code": "OK", "data": { ... } }
// 실패 (어떤 에러든 이 모양)
{ "statusCode": 404, "code": "ITEM_NOT_FOUND", "message": "상품을 찾을 수 없어요", "errors": [] }
// 입력 오류
{ "statusCode": 422, "code": "VALIDATION_ERROR", "message": "입력값을 확인해 주세요",
  "errors": [{ "field": "body.name", "message": "..." }] }
```
- 업무 에러는 `raise AppError(status.HTTP_409_CONFLICT, "CODE", "메시지")`로 던져요. 라우트에서 try/except를 쓰지 않아요.
- 실제로 낼 수 있는 에러만 `responses=error_responses(status.HTTP_404_NOT_FOUND, ...)`로 `/docs`에 표시해요.

## 시작하기
1. 폴더를 복사하고 이름을 바꿔요.
2. 프로젝트 이름에 맞게 고쳐요.
   - `pyproject.toml`: `name`
   - `app/core/config.py`: `PROJECT_NAME`, `FRONTEND_HOST`
   - `compose.yaml`: `container_name` (`myapp-fastapi`, `myapp-mysql`)
   - `compose.override.yaml`, `compose.prod.yaml`: 포트
3. `.env.example`을 `.env`로 복사해요. DB 이름과 비밀번호를 고쳐요.
4. 패키지를 설치해요: `uv sync`. 버전을 올리려면 먼저 `uv lock --upgrade`를 해요.
5. 실행
   ```
   docker compose up -d --build                             # 개발 (http://localhost:8000/docs)
   docker compose exec fastapi uv run alembic revision --autogenerate -m "create items"
   docker compose exec fastapi uv run alembic upgrade head
   docker compose exec fastapi uv run python -m app.seeds   # 더미 데이터 (선택)
   ```
   로컬에서 바로 실행할 때는 `uv run fastapi dev`를 써요. 이때 DB는 `.env`의 `DATABASE_URL`(127.0.0.1:3306)을 써요.
6. 확인
   ```
   uv run pytest
   uv run ruff check . && uv run ruff format --check .
   uv run ty check
   ```

## 새 기능 추가 순서 (items 를 복사)
1. `models/<이름>.py`를 만들고 `models/__init__.py`에 import해요.
2. `alembic revision --autogenerate`로 리비전을 만들고, 생성된 파일을 검토한 뒤 `upgrade head`해요.
3. `schemas/<이름>.py`에 Create와 Public 스키마를 만들고 `schemas/__init__.py`에서 내보내요.
4. `crud/<이름>.py`에 쿼리를 만들어요.
5. `services/<이름>.py`에 로직, commit, `AppError`를 넣어요.
6. `api/v1/routes/<이름>.py`에 라우트를 만들고 `api/v1/__init__.py`에 `include_router`해요.

## 규칙 메모
- **시각**
  - `datetime.now()`를 직접 쓰지 않고 `clock.now()`를 써요.
  - DB에는 KST로 저장해요. `KSTDateTime` 컬럼은 `+09:00`이 붙은 값으로 읽혀요.
  - 시간대가 없는(naive) 값은 저장할 때 에러가 나요.
- **세션**
  - `async def` 라우트에서는 `AsyncSessionDep`을 써요.
  - 동기 세션은 Alembic, 시드, 스크립트에서만 써요.
  - 관계(`relationship`)는 `lazy="raise"`로 두고 `selectinload`/`joinedload`로 불러와요. N+1과 비동기 지연 로딩 에러를 막으려는 거예요.
- **생성 후 `session.refresh()`**: `DATETIME`은 초 단위라서, DB에 저장된 값을 다시 읽어야 응답과 저장값이 같아요.
- **상태 코드**
  - 앱 코드는 `fastapi.status` 상수를 써요.
  - 테스트는 실제로 응답에 나가는 값을 확인하는 거라 숫자로 써요.
- **상태 값**: DB ENUM 대신 `String` 컬럼과 Python `Literal`을 써요.
- **마이그레이션**
  - `--autogenerate`는 개발 DB에서만 해요.
  - 운영에서는 `upgrade head`만 해요. entrypoint에서 자동으로 돌리지 않고 배포할 때 명시적으로 실행해요.
  - 공유한 리비전 파일은 고치지 않아요. 바꿀 게 있으면 새 리비전을 만들어요.
- **`alembic.ini`는 ASCII만 써요.** Windows에서 cp949로 읽혀서 한글이 들어가면 에러가 나요.
- **테스트 DB**: DB를 쓰는 테스트가 생기면 `<DB이름>_test`를 따로 만들어요. `conftest.py`에서 그 DB로 연결하고, 테이블 생성, 시드, 시각 고정을 해요.
