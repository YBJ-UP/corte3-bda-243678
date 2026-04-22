from fastapi import APIRouter


class router[T]:
    def __init__(self, table: str) -> None:
        self.router = APIRouter()
        self.router.add_api_route(path=f"/test/{table}", endpoint=self.__getAll, methods=["GET"])

    def __getAll(self):
        return 1