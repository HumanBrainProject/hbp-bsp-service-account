from requests.auth import HTTPBasicAuth
from service_account.settings import NSG_APPKEY as APPKEY
from service_account.settings import NSG_USER as USER
from service_account.settings import NSG_PASSWORD as PASSWORD
from service_account.settings import UMBRELLA

import requests


# TODO: add META handler v2
# TODO: add error handler v2
# TODO: add parameters handler v2


URL_ROOT = 'https://nsgr.sdsc.edu:8443/cipresrest/v1'


def get_headers(eu, eu_mail, eu_institution, eu_country):
    headers = {"cipres-appkey": APPKEY}
    if eu and eu_mail and eu_institution and eu_country:
        headers.update(
            {
                "cipres-eu": eu,
                "cipres-eu-email": eu_mail,
                "cipres-eu-institution": eu_institution,
                "cipres-eu-country": eu_country
            }
        )
    return headers


def get_credential():
    return HTTPBasicAuth(USER, PASSWORD)


def get_root_url(eu=None):
    if not UMBRELLA:
        return URL_ROOT + '/job/' + USER
    return URL_ROOT + '/job/' + APPKEY.split('-')[0] + '.' + eu


def submit_job(payload, infile, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu)
    infile = {'input.infile_': infile}
    return requests.post(url, auth=get_credential(), headers=headers, data=payload, files=infile)


def job_status(jobid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid
    return requests.get(url, headers=headers, auth=get_credential())


def list_jobs(eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu)
    return requests.get(url, headers=headers, auth=get_credential())


def list_results(jobid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid
    return requests.get(url, headers=headers, auth=get_credential())


def list_job_files(jobid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid + '/output'
    return requests.get(url, headers=headers, auth=get_credential())


def list_workingdir_files(jobid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid + '/workingdir'
    return requests.get(url, headers=headers, auth=get_credential())


def download_job_file(jobid, fileid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid + '/output/' + fileid
    return requests.get(url, headers=headers, auth=get_credential())


def download_workingdir_file(jobid, filename, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid + '/workingdir/' + filename
    return requests.get(url, headers=headers, auth=get_credential())


def delete_job(jobid, eu=None, eu_mail=None, eu_institution=None, eu_country=None):
    headers = get_headers(eu, eu_mail, eu_institution, eu_country)
    url = get_root_url(eu) + '/' + jobid
    return requests.delete(url, headers=headers, auth=get_credential())
