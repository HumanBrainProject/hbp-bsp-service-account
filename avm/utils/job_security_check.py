from difflib import SequenceMatcher
from shutil import rmtree
from subprocess import Popen, PIPE
import os

#from service_account.settings import JOB_SECURITY_FILE_CHECK as FILE_CHECK


TMP_DIR = '/mnt/sa-storage/job/temp'
FILE_CHECK = ['/mnt/sa-storage/job/sec/opt_neuron.py', '/mnt/sa-storage/job/sec/ipyparallel.sbatch'] 

OMITTED_CHAR = ['\n', '\t', '', ' ',]

malicious = [
    'rmtree',
    'rm'
]


def store_and_extract(user, job_file):
    user_dir = os.path.join(TMP_DIR, user.id)
    if os.path.exists(user_dir):
        rmtree(user_dir)
    os.mkdir(user_dir)
    with open(os.path.join(user_dir, job_file.name), 'wb') as fd:
        fd.write(job_file.read())
    p = Popen(['unzip', os.path.join(user_dir, job_file.name), '-d', user_dir], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print('unzipping process:\nstdout: %s\nstderr: %s' % (stdout, stderr)) 
    dir_name = None
    for d in os.listdir(user_dir):
        print(d)
        if os.path.isdir(os.path.join(user_dir, d)):
            dir_name = d
            print(dir_name)
    return os.path.join(user_dir, dir_name)


def check_job(user, job_file):
    sm = SequenceMatcher()

    #if job_file.split('.')[-1] == 'zip':
    #    job_dir = extract_job(job_file)
    job_dir = store_and_extract(user, job_file)

    with open(FILE_CHECK[0], 'r') as a, open(os.path.join(job_dir, 'opt_neuron.py'), 'r') as b:
        print('Check opt_neuron.py file...')
        sm.set_seqs(a.read(), b.read())
        ratio = sm.real_quick_ratio()
        if ratio < 0.99:
            print('Ratio %f < 0.99' % ratio) 
            #return False
        diff = sm.get_opcodes()
        for d in diff:
            print(d)
            if d[0] == 'equal':
                continue
            if d[0] != 'insert':
                return False
            b.seek(d[3])
            value = b.read(d[4] - d[3])
            print(value)
            if value not in OMITTED_CHAR and len(set(value.split(' ')).intersection(malicious)) > 0:
                return False

    with open(FILE_CHECK[1], 'r') as a, open(os.path.join(job_dir, 'ipyparallel.sbatch'), 'r') as b:
        print('Checking ipyparallel.sbatch file...')
        sm.set_seqs(a.read(), b.read())
        ratio = sm.real_quick_ratio()
        if ratio < 0.99:
            print('Ratio %f < 0.99' % ratio)
            #return False 
        diff = sm.get_opcodes()
        for d in diff:
            print(d)
            if d[0] == 'equal':
                continue
            if d[0] != 'insert':
                return False

            b.seek(d[3])
            value = b.read(d[4] - d[3])
            if value not in OMITTED_CHAR:
                try:
                    int(b.read(d[4] - d[3]))
                except ValueError:
                    return False

    return True
