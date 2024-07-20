import json
import logging
import typing as ty

from .exceptions import *
from .library import Document, File
from .utils import get_session

logger = logging.getLogger(__name__)
session = get_session()


class KnopkaAdapter:
    """Request adapter for API"""

    BASE_DOMAIN: str = "https://p.knopka.com/restApi/dotnet/customerApi"

    def __init__(self, access_token: str) -> None:
        self._access_token: str = str(access_token).strip()

    def _sec_headers(self, **dictionary) -> ty.Dict[str, str]:
        """Function to hide the token in logs"""

        result: ty.Dict[str, str] = dict()
        for key, value in dictionary.items():
            if value.endswith(self._access_token):
                result[key] = value.replace(self._access_token, "***")
            else:
                result[key] = value

        return result

    def execute(
        self,
        method: str,
        path: str,
        body: ty.Optional[ty.Dict[str, ty.Any]] = None,
        query_params: ty.Optional[ty.Dict[str, ty.Any]] = None,
    ) -> ty.Dict[str, ty.Any]:
        """The general method of all requests"""

        is_download: bool = method.lower() == "get" and "downloadFile" in path

        kwargs: ty.Dict[str, ty.Any] = dict(
            method=method,
            url=self.BASE_DOMAIN + path,
            params=query_params,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "Authorization": f"Bearer {self._access_token}",
            },
            json=body,
        )

        logger.warning(
            f"{self.__class__.__name__} request: "
            f"method={method.upper()} "
            f"url={kwargs['url']} "
            f"params={json.dumps(kwargs['params'])} "
            f"headers={json.dumps(self._sec_headers(**kwargs['headers']))} "
            f"json={json.dumps(kwargs['json'], ensure_ascii=False)} "
        )

        res = session.request(**kwargs)  # type: ignore

        logger.warning(
            f"{self.__class__.__name__} response: "
            f"status_code={res.status_code} "
            f"headers={json.dumps(dict(res.headers))} "
            f"body={'<bytes_file>' if is_download else res.text}"
        )

        if res.status_code == 401:
            raise RequestAuthorizationException("Authorization token is incorrect.")
        elif res.status_code >= 500:
            raise RequestUnhandledException(f"Unknown error ({res.status_code}).")
        elif res.status_code != 200:
            raise RequestError(f"Error during request ({res.status_code}).")

        if method.lower() == "head":
            return dict(res.headers)
        elif is_download:
            result = dict(res.headers)
            result["body"] = res.content  # type: ignore[assignment]
            return result
        else:
            return res.json()

    def get_documents_from_ones(self, uid: int) -> ty.List[Document]:
        """Document package retrieval from 1C"""

        if not str(uid).isdigit():
            raise TypeError("Identifier `uid` is not an integer.")

        res: ty.Dict[str, ty.Any] = self.execute(
            method="GET",
            path="/getTaskInfo",
            query_params={"taskId": int(uid)},
        )

        if "error" in res["state"].lower():
            raise DocumentsNotFoundException(
                f"Documents with identifier {uid=!s} not found "
                f"(`{res.get('message', 'without-error-message').lower()}`)."
            )

        elif res["state"].lower() in {"new", "inpro"}:
            raise DocumentsInProcessException(
                "Documents are in the process of being prepared, please wait."
            )

        result: ty.List[Document] = list()
        for index, raw in enumerate(res["result"]):
            result.append(Document.from_response(raw=raw, file_url=res["links"][index]))

        return result

    def get_file(self, uid: int, **kwargs) -> File:
        """Retrieve full file"""

        if not str(uid).isdigit():
            raise TypeError("Identifier `uid` is not an integer.")

        try:
            res: ty.Dict[str, ty.Any] = self.execute(
                method="HEAD" if "only_meta_please" in kwargs else "GET",
                path=f"/downloadFile/{uid}",
            )
        except RequestUnhandledException as e:
            if "unknown error (500)" in str(e).lower():
                raise UnableGetFileException(f"The file `{uid=!s}` is unavailable.")
            else:
                raise
        else:
            return File.from_response(raw=res)

    def get_meta_from_file(self, uid: int) -> File:
        """Retrieve file metadata: just syntactic sugar for aesthetics"""

        return self.get_file(uid=uid, **{"only_meta_please": True})

    def create_documents(self):
        """Creation of task for document preparation"""

        pass
