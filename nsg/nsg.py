import xml.etree.ElementTree as ElTree
import logging

from utils.params import *
from utils import api


logger = logging.getLogger(__name__)


def get_enduser(meta):

    return {
        'eu': meta.get('HTTP_EU'),
        'email': meta.get('HTTP_EU_MAIL'),
        'institution': meta.get('HTTP_EU_INSTITUTION'),
        'country': meta.get('HTTP_EU_COUNTRY')
    }


def list_jobs(enduser):
    r = api.list_jobs(eu=enduser['eu'], eu_mail=enduser['email'], eu_institution=enduser['institution'],
                      eu_country=enduser['country'])
    return r.content, r.status_code


def submit_job(enduser, payload, infile):
    try:
        check_payload(payload)
        payload = transform_payload(payload)
    except ValueError:
        return 'Wrong value!', 400

    r = api.submit_job(payload=payload, infile=infile, eu=enduser['eu'], eu_mail=enduser['email'],
                       eu_institution=enduser['institution'], eu_country=enduser['country'])

    if r.status_code == 200:
        xml_root = ElTree.fromstring(r.content)
        data = {
            'job_id': xml_root.find('jobHandle').text,
            'init_date': xml_root.find('dateSubmitted').text,
            'stage': xml_root.find('jobStage').text,
            'terminal_stage': False if xml_root.find('terminalStage').text == 'false' else True,
            'failed': False if xml_root.find('failed').text == 'false' else True,
        }
        return data, r.status_code

    return r.content, r.status_code


def get_job_status(enduser, jobid):
    logger.debug('get_job_status() called by user: ' + enduser['id'] + ' for job: ' + jobid + '.')

    r = api.job_status(jobid=jobid, eu=enduser['eu'], eu_mail=enduser['email'],
                       eu_institution=enduser['institution'], eu_country=enduser['country'])
    if r.status_code == 200:
        logger.debug('job_status response status_code: 200 OK!')

        xml_root = ElTree.fromstring(r.content)

        data = {
            'stage': xml_root.find('jobStage').text,
            'terminal_stage': False if xml_root.find('terminalStage').text == 'false' else True,
            'failed': xml_root.find('failed').text
        }

        if xml_root.find('jobStage').text == 'COMPLETED':
            logger.debug('job [' + jobid + '] completed. Updating info.')
            end_date = xml_root.find('messages').findall('message')[-1].find('timestamp').text
            data.update({'end_date': end_date})

        return data, r.status_code
    return r.content, r.status_code


def delete_job(enduser, jobid):
    r = api.delete_job(jobid=jobid, eu=enduser['eu'], eu_mail=enduser['email'], eu_institution=enduser['institution'],
                       eu_country=enduser['country'])
    if r.status_code == 204:
        return 'Job ' + jobid + ' was deleted', r.status_code
    return r.content, r.status_code


def get_job_files_list(enduser, jobid):
    r = api.list_job_files(jobid=jobid, eu=enduser['eu'], eu_mail=enduser['email'],
                           eu_institution=enduser['institution'], eu_country=enduser['country'])
    if r.status_code == 200:
        files = []
        xml_root = ElTree.fromstring(r.content)
        for f in xml_root.find('jobfiles').findall('jobfile'):
            data = {
                'fileid': f.find('outputDocumentId').text,
                'filename': f.find('filename').text,
                'length': f.find('length').text
            }
            files.append(data)
        return files, r.status_code
    return r.content, r.status_code


def list_workingdir_files(enduser, jobid):
    r = api.list_workingdir_files(jobid=jobid, eu=enduser['eu'], eu_mail=enduser['email'],
                                  eu_institution=enduser['institution'], eu_country=enduser['country'])
    if r.status_code == 200:
        files = []
        xml_root = ElTree.fromstring(r.content)
        for f in xml_root.findall('jobfile'):
            data = {
                'filename': f.find('filename').text,
                'length': f.find('length').text,
                'modified': f.find('dateModified').text
            }
            files.append(data)
        return files, r.status_code
    return r.content, r.status_code


# noinspection PyTypeChecker
def download_output_file(enduser, jobid, fileid=None):
    if not fileid:
        files = get_job_files_list(enduser=enduser, jobid=jobid)
        fileid = files[-1]['fileid']
    r = api.download_job_file(jobid=jobid, fileid=fileid, eu=enduser['eu'], eu_mail=enduser['email'],
                              eu_institution=enduser['institution'], eu_country=enduser['country'])
    return r.content, r.status_code


def download_working_directory_file(enduser, jobid, filename):
    r = api.download_workingdir_file(jobid=jobid, filename=filename, eu=enduser['eu'], eu_mail=enduser['email'],
                                     eu_institution=enduser['institution'], eu_country=enduser['country'])
    return r.content, r.status_code
