"""
Utilities for DICOMweb URI manipulation.
"""
import enum
import re
from typing import Optional
import urllib.parse as urlparse
from dataclasses import dataclass


class WrongTypeError(Exception):
    pass


@dataclass
class Document:
    root_url: str
    aimId: str

    def url(self):
        return f"{self.root_url}/document/{self.aimId}.download"


@dataclass
class File:
    root_url: str
    aimId: str

    def url(self):
        return f"{self.root_url}/file/{self.aimId}.download"


@dataclass
class Dicom:
    root_url: str
    aimId: str

    def url(self):
        return f"{self.root_url}/image/{self.aimId}.download"


@dataclass
class XmlHeader:
    root_url: str
    aimId: str

    def url(self):
        return f"{self.root_url}/image/{self.aimId}.xml"


@dataclass
class DicomDump:
    root_url: str
    refPtr: str

    def url(self):
        return f"{self.root_url}/refptr/{self.refPtr}.xml?dicom_dump=1&no_pixel_data=1"


class URIType(enum.Enum):
    """
    Type of DICOM resource the URI points to.
    """
    SERVICE = 'service'
    STUDY = 'study'
    SERIES = 'series'
    INSTANCE = 'instance'


class URISuffix(enum.Enum):
    """
    Optional suffixes for a DICOM resource.
    """
    XML = 'xml'


# For DICOM Standard spec validation of UID components in `URI`.
_MAX_UID_LENGTH = 64
_REGEX_UID = re.compile(r'[0-9]+([.][0-9]+)*')


@dataclass
class URI:

    _base_url: str
    _study_instance_uid: Optional[str] = None
    _series_instance_uid: Optional[str] = None
    _sop_instance_uid: Optional[str] = None
    _suffix: Optional[URISuffix] = None

    def __post_init__(self):
        _validate_base_url(self._base_url)
        _validate_resource_identifiers_and_suffix(
            self._study_instance_uid,
            self._series_instance_uid,
            self._sop_instance_uid,
            self._suffix
        )

    def __str__(self) -> str:
        """
        Returns the object as a DICOMweb URI string.
        """
        parts = (self.study_instance_uid, self.series_instance_uid, self.sop_instance_uid)
        dicomweb_suffix = ''.join(f'{part}-' for part in parts if part is not None).rstrip('-')

        if self.suffix is not None:
            dicomweb_suffix = f"{dicomweb_suffix}.{self.suffix.value}"

        return f'{self.base_url}{dicomweb_suffix}'

    @property
    def base_url(self) -> str:
        """Returns the Base URL."""
        return self._base_url

    @property
    def study_instance_uid(self) -> Optional[str]:
        """Returns the Study UID, if available."""
        return self._study_instance_uid

    @property
    def series_instance_uid(self) -> Optional[str]:
        """Returns the Series UID, if available."""
        return self._series_instance_uid

    @property
    def sop_instance_uid(self) -> Optional[str]:
        """Returns the Instance UID, if available."""
        return self._sop_instance_uid

    @property
    def suffix(self) -> Optional[URISuffix]:
        """Returns the DICOM resource suffix, if available."""
        return self._suffix

    @property
    def type(self) -> URIType:
        """The `URIType` of DICOM resource referenced by the object."""
        if self.study_instance_uid is None:
            return URIType.SERVICE
        elif self.series_instance_uid is None:
            return URIType.STUDY
        elif self.sop_instance_uid is None:
            return URIType.SERIES
        return URIType.INSTANCE

    def base_uri(self) -> 'URI':
        """
        Returns URI for the DICOM Service within this object.
        """
        return URI(self.base_url, self.suffix)

    def study_uri(self) -> 'URI':
        """
        Returns URI for the DICOM Study within this object.
        """
        if self.type == URIType.SERVICE:
            raise ValueError('Cannot get a Study URI from a Base URL.')
        return URI(self.base_url, self.study_instance_uid, self.suffix)

    def series_uri(self) -> 'URI':
        """
        Returns URI for the DICOM Series within this object.
        """
        if self.type in (URIType.SERVICE, URIType.STUDY):
            raise ValueError(f'Cannot get a Series URI from a {self.type!r} URI.')
        return URI(self.base_url, self.study_instance_uid, self.series_instance_uid, self.suffix)

    def instance_uri(self) -> 'URI':
        """
        Returns URI for the DICOM Instances within this object.
        """
        if self.type is not URIType.INSTANCE:
            raise ValueError(f'Cannot get an Instance URI from a {self.type!r} URI.')
        return URI(self.base_url, self.study_instance_uid,
                   self.series_instance_uid, self.sop_instance_uid, self.suffix)


def _validate_base_url(url: str) -> None:
    """
    Validates the Base URL supplied to URI.
    """
    parse_result = urlparse.urlparse(url)
    if parse_result.scheme not in ('http', 'https'):
        raise ValueError(f'Only HTTP[S] URLs are permitted. Actual URL: {url!r}')
    if url.endswith('/'):
        raise ValueError(f'Base URL cannot have a trailing forward slash: {url!r}')


def _validate_resource_identifiers_and_suffix(study_instance_uid: Optional[str],
                                              series_instance_uid: Optional[str],
                                              sop_instance_uid: Optional[str],
                                              suffix: Optional[URISuffix]
                                              ) -> None:
    """
    Validates UID, frames, and suffix params for the URI constructor.
    """
    # Note that the order of comparisons in this method is important.
    if series_instance_uid is not None and study_instance_uid is None:
        raise ValueError(f'study_instance_uid missing with non-empty '
                         f'series_instance_uid: {series_instance_uid!r}')

    if sop_instance_uid is not None and series_instance_uid is None:
        raise ValueError(f'series_instance_uid missing with non-empty '
                         f'sop_instance_uid: {sop_instance_uid!r}')

    for uid in (study_instance_uid, series_instance_uid, sop_instance_uid):
        if uid is not None:
            _validate_uid(uid)

    if (suffix is URISuffix.XML) and (study_instance_uid is None):
        raise ValueError(
            f'{suffix!r} suffix requires a DICOM resource pointer, '
            f'cannot be set for a Service URL alone.')


def _validate_uid(uid: str) -> None:
    """
    Validates a DICOM UID.
    """
    if len(uid) > _MAX_UID_LENGTH:
        raise ValueError(f'UID cannot have more than 64 chars. '
                         f'Actual count in {uid!r}: {len(uid)}')


if __name__ == '__main__':

    from _paths import BASE_URL
    study_uid_ = '1.2.840.113619.6.95.31.0.3.4.1.24.13.5097093'
    series_uid_ = None  #'1.2.40.0.13.0.144.200.126.197.1189109196.1502754214796.32768'
    sop_uid_ = None  #'1.2.40.0.13.0.144.200.126.197.1189109196.1502754214796.32770'

    uri_ = URI(BASE_URL, study_uid_, series_uid_, sop_uid_, URISuffix.XML)

    print(uri_)
