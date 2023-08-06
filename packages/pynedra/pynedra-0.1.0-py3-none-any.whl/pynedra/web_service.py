"""
Pynedra

This module provides a set of functions to communicate with the
webservice of the long-term storage and archiving solution of Synedra.

The module requires valid certificate and certificate key *.pem files
to establish a connection to the server.
"""
import io
from dataclasses import dataclass, field
from typing import Optional, Tuple
import xmltodict
from pydicom import dcmread
from pydicom.dataset import Dataset
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session
from logdecoratorandhandler.log_decorator import LogDecorator
import logdecoratorandhandler.options as ld

# from .options import Options
# from .uri import URI, Dicom
from src.pynedra.options import Options
from src.pynedra.uri import URI, Dicom, URISuffix, DicomDump

ld.Options.log_level = Options.log_level


class AlreadyConnected(Exception):
    pass


class CannotConnectError(Exception):
    pass


@dataclass
class Pynedra:
    """
    Class for Synedra Webservice
    """
    uid_tuple: tuple
    url_tuple: tuple
    certificate_bundle: Optional[Tuple[str, str]]
    session: Session() = field(init=False, default=None)
    url: URI = field(init=False)

    def __post_init__(self):
        self._start_session()
        self.url = URI(f'{self.url_tuple[0]}/{self.url_tuple[1]}',
                       self.uid_tuple[0],
                       self.uid_tuple[1],
                       self.uid_tuple[2],
                       URISuffix.XML)

    @LogDecorator('INFO - start session')
    def _start_session(self):
        """
        Custom adapter with timeout properties / options - see implementation in class below

        Setup session and mount the adapter to both the http:// and https:// endpoint
        """
        if self.session is None:
            self.session = Session()
            self.session.cert = self.certificate_bundle
            self.session.verify = False       # should be True!!!
            self.session.stream = False

            try:
                if Options.total_retries > 0:
                    adapter = HTTPAdapter(
                        max_retries=Retry(total=Options.total_retries,
                                          backoff_factor=Options.backoff_factor,
                                          status_forcelist=[413, 429, 500, 502, 503, 504],
                                          allowed_methods=["HEAD", "GET", "OPTIONS"],
                                          ),
                    )
                    for prefix in "http://", "https://":
                        self.session.mount(prefix, adapter)
            except CannotConnectError as ex:
                raise CannotConnectError('Connection not possible!') from ex
        else:
            raise AlreadyConnected('Transport is already connected')

    @LogDecorator('INFO - get metadata')
    def get_metadata(self) -> dict:
        """
        Get meta data of dicom image as dictionary.
        """
        with self.session.get(str(self.url)) as results:
            if results.status_code == 200:
                dict_result = xmltodict.parse(results.text)
                return dict_result
            return {}

    @LogDecorator('INFO - get dicom')
    def get_dicom(self) -> Dataset:
        """
        Get dicom image.
        """
        aim_id = self.get_metadata()['aimInfo']['dicomStudy']['dicomSeries']['dicomImage']['@aimId']
        url = Dicom(self.url_tuple[0], aim_id).url()

        with self.session.get(str(url)) as results:
            if results.status_code == 200:
                for chunk in results.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        dicom_content = dcmread(io.BytesIO(chunk), force=True)
            return dicom_content
            # return Dataset

    @LogDecorator('INFO - get dicom dump (tags without pixel data)')
    def get_dicom_dump(self) -> dict:
        """
        Get meta data of dicom image as dictionary.
        """
        refptr = self.get_metadata()[
            'aimInfo']['dicomStudy']['dicomSeries']['dicomImage']['@refPtr']
        url = DicomDump(self.url_tuple[0], refptr).url()

        with self.session.get(f'{str(url)}?dicom_dump=1&no_pixel_data=1') as results:
            if results.status_code == 200:
                dict_result = xmltodict.parse(results.text)
                return dict_result
            return {}

    # # TODO: implement
    # def get_dicom_from_series(self) -> Dataset:
    #     """
    #     Get dicom image.
    #     """
    #     list_dicom = self.get_metadata()['aimInfo']['dicomStudy']['dicomSeries']['dicomImage']
    #     aim_ids = {i for i in list_dicom}
    #     for aim_id in aim_ids:
    #         url = Dicom(aim_id).url()
    #         # TODO: check - not correct or finished
    #         # for idx in (0, -1):
    #         #     return Pynedra(url=get_url(dicom[idx])).get_dicom()
    #         with self.session.get(str(url)) as results:
    #             if results.status_code == 200:
    #                 for chunk in results.iter_content(chunk_size=None, decode_unicode=True):
    #                     if chunk:
    #                         dicom_content = dcmread(io.BytesIO(chunk), force=True)
    #                 return dicom_content
    #
    # # TODO: implement
    # def get_first_and_last_image(self) -> Dataset:
    #     """
    #     Get dicom image.
    #     """
    #     list_dicom = self.get_metadata()['aimInfo']['dicomStudy']['dicomSeries']['dicomImage']
    #     aim_ids = {i for i in list_dicom}
    #     for aim_id in aim_ids:
    #         url = Dicom(aim_id).url()
    #         # TODO: check - not correct or finished
    #         with self.session.get(str(url)) as results:
    #             if results.status_code == 200:
    #                 for chunk in results.iter_content(chunk_size=None, decode_unicode=True):
    #                     if chunk:
    #                         dicom_content = dcmread(io.BytesIO(chunk), force=True)
    #                 return dicom_content


if __name__ == '__main__':

    from urllib3.exceptions import InsecureRequestWarning
    from urllib3 import disable_warnings

    root_url = 'https://aimserver:11513'
    base_url = 'refptr/1.0:aimserver:dcm::'
    certificate = '../../res/synedra_prod.crt.pem'
    certificate_key = '../../res/synedra_prod.key.pem'

    CERTIFICATE_BUNDLE = (certificate, certificate_key)

    disable_warnings(InsecureRequestWarning)

    study_uid_ = '1.2.840.113619.6.95.31.0.3.4.1.24.13.5097093'
    series_uid_ = '1.2.40.0.13.0.144.200.126.197.1189109196.1502754214796.32768'
    sop_uid_ = '1.2.40.0.13.0.144.200.126.197.1189109196.1502754214796.32770'

    print(Pynedra((study_uid_, series_uid_, sop_uid_), (root_url, base_url), CERTIFICATE_BUNDLE).get_metadata())
    print(Pynedra((study_uid_, series_uid_, sop_uid_), (root_url, base_url), CERTIFICATE_BUNDLE).get_dicom())
    print(Pynedra((study_uid_, series_uid_, sop_uid_), (root_url, base_url), CERTIFICATE_BUNDLE).get_dicom_dump())

