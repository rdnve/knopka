from __future__ import annotations

import datetime as dt
import io
import re
import typing as ty
from copy import deepcopy

import attr


class AbstractModel:
    def to_dict(self) -> ty.Dict[str, ty.Any]:
        return deepcopy(self.__dict__)

    @classmethod
    def from_response(cls, raw: ty.Dict[str, ty.Any], **kwargs) -> ty.Any:
        raise NotImplemented


@attr.s(auto_attribs=True)
class Document(AbstractModel):
    """Model of typical document"""

    guid: str
    type: str
    number: str
    date: dt.date
    is_earlier: bool = False
    file_url: ty.Optional[str] = None

    @property
    def file_uid(self) -> ty.Optional[int]:
        """Relevant for future file downloads"""

        if self.file_url is not None:
            return int(self.file_url.split("/")[-1])

        return None

    def to_dict(self) -> ty.Dict[str, ty.Any]:
        """Convert obj to dict w/ some modifications"""

        raw: ty.Dict[str, ty.Any] = super().to_dict()
        raw.update(date=self.date.isoformat(), file_uid=self.file_uid)
        return raw

    @classmethod
    def from_response(
        cls, raw: ty.Dict[str, ty.Any], file_url: ty.Optional[str] = None, **kwargs
    ) -> Document:
        """Create obj from response"""

        params: ty.Dict[str, ty.Any] = dict(
            guid=raw["guid1C"],
            type=raw["type"],
            number=raw["number"],
            date=dt.datetime.strptime(raw["date"], "%d.%m.%Y %H:%M:%S").date(),
            is_earlier=raw["done_earlier"],
        )

        if file_url is not None:
            params["file_url"] = file_url.strip()

        return cls(**params)


@attr.s(auto_attribs=True)
class File(AbstractModel):
    """Model of typical file"""

    name: str
    type: str
    size: ty.Optional[int] = None
    object: ty.Optional[io.BytesIO] = None

    def to_dict(self) -> ty.Dict[str, str]:
        """Convert obj to dictionariy without body"""

        res: ty.Dict[str, str] = dict()
        for k, v in self.__dict__.items():
            if k == "object":
                continue
            else:
                res[k] = v

        return res

    @classmethod
    def from_response(
        cls, raw: ty.Dict[str, ty.Any], uid: ty.Optional[int] = None, **kwargs
    ) -> File:
        """Create obj from response"""

        content_type: str = raw["Content-Type"]
        matches: ty.List[str] = re.findall(
            r"filename\*?=([^;]+)", raw["Content-Disposition"]
        )

        if len(matches) > 0:
            name = matches[0]
        else:
            name = f"{uid}.{content_type.split('/')[-1]}"

        params: ty.Dict[str, ty.Any] = dict(name=name, type=content_type)

        if "body" in raw:
            params.update(
                object=io.BytesIO(raw["body"]),
                size=len(raw["body"]),
            )

        return cls(**params)

    def save(self, path: str) -> str:
        """Helper for save file"""

        if self.size is None:
            ValueError("The file is empty, nothing to save.")

        path = f"{path}/{self.name}"
        with open(path, "wb") as f:
            f.write(self.object.read())  # type: ignore[union-attr]

        return path
