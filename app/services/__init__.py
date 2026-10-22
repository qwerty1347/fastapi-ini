"""화면·기능 단위 로직. crud 로 테이블을 읽고, 계산·조립해서 응답 스키마로 만든다.

    from app.services import item as item_service

라우트 → services → crud → DB 순서로 부른다.
트랜잭션(commit)과 업무 에러(AppError)는 여기서 정한다.
"""
