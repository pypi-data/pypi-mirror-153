import os
import time
import datetime
import logging
from io import BytesIO
from datetime import datetime
import json
import traceback

from urllib.request import urlopen
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from croniter import croniter
from flask.wrappers import Response

import jwt
import boto3
from botocore.exceptions import NoCredentialsError
import flask
import requests

from .constants import DATETIME_FORMAT
logger = logging.getLogger(__name__)

BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
API_RETRY = int(os.getenv('API_RETRY', 3))
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_API_URL = os.getenv('DATA_API_BASE_URL', '')
PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE")
APP_ID = os.getenv('APP_ID')
API_TIME_STACKS = int(os.getenv('API_TIME_STACKS', 5))

from .renderer.excel import ExcelRenderer
storage_name = os.getenv('STORAGE_NAME')

global ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION_NAME, BUCKET_NAME

if storage_name == 's3':
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    REGION_NAME = os.getenv('REGION_NAME')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
elif storage_name == 'ceph':
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    ENDPOINT_URL = os.getenv('ENDPOINT_URL')
else:
    logger.info("No storages are found")


def get_token():
    headers = {"Content-Type" : "application/x-www-form-urlencoded" , "Accept" : "application/json"};
    post_data = {"grant_type": "client_credentials", "client_id" : API_KEY, "client_secret" : API_SECRET};
    token_url = BASE_API_URL + "/auth/oauth/token";
    response = requests.post(token_url,data=post_data,headers=headers,verify=False);
    json = response.json();
    auth = str(json["access_token"])
    return auth


def get_jwt_token():
    try:
        jwt_token = flask.request.cookies.get('OPSRAMP_JWT_TOKEN', '')
    except:  # outside Flask
        jwt_token = os.getenv('OPSRAMP_JWT_TOKEN', '')

    return jwt_token


def get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_token()}'
    }

    return headers


def login_get_headers():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {get_jwt_token()}'
    }

    return headers


def call_requests(method, url, params=None, data=None, json=None, verify=True):
    headers = get_headers()
    retry = 1
    resp = None
    while retry <= API_RETRY:
        try:
            resp = requests.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue

        return resp
    
    return resp


def login_call_requests(method, url, params=None, data=None, json=None, verify=True):
    headers = login_get_headers()
    retry = 1
    resp = None
    while retry <= API_RETRY:
        try:
            resp = requests.request(method, url, params=params, data=data, json=json, headers=headers, verify=verify)
            if not resp.ok:
                time.sleep(retry * 2)
                retry+=1
                continue
        except requests.exceptions.ConnectionError:
            time.sleep(retry * 2)
            retry+=1
            continue

        return resp
    
    return resp


def call_get_requests(url, params=None, verify=True):
    return call_requests('GET', url, params, verify=verify)


def call_post_requests(url, params=None, data=None, verify=True):
    return call_requests('POST', url, params, data, verify=verify)


def call_put_requests(url, params=None, data=None, verify=True):
    return call_requests('PUT', url, params, data, verify=verify)


def login_call_get_requests(url, params=None, verify=True):
    return login_call_requests('GET', url, params, verify=verify)


def is_authenticated():
    REQUIRE_AUTH_REDIRECT = os.getenv('REQUIRE_AUTH_REDIRECT') == 'true'
    if not REQUIRE_AUTH_REDIRECT:
        return True

    url = f'{BASE_API_URL}/api/v2/users/me'
    res = login_call_get_requests(url)
    return res.status_code == 200


def login_required(view):
    '''Decorator that check authentication'''
  
    def wrap(*args, **kwargs):
        if not is_authenticated():
            return Response('Not authorized', status=401)
        result = view(*args, **kwargs)
        return result
    return wrap


def get_epoc_from_datetime_string(str_datetime):
    timestamp = datetime.strptime(str_datetime, DATETIME_FORMAT).timestamp()
    return timestamp


def get_result_by_run(run_id, field=None, default_value=None):
    try:
        run_id= f'{PLATFORM_ROUTE}/{run_id}/json/{run_id}'
        if storage_name == 's3':
            s3 = get_s3_client()
            res_object = s3.get_object(Bucket=BUCKET_NAME,Key=run_id)
            serializedObject = res_object['Body'].read()
            result = json.loads(serializedObject)
            if field:
                result = result.get(field, default_value)
            return result
        elif storage_name == 'ceph':
            s3 = get_s3_ceph()
            data = BytesIO()
            res_object = s3.Bucket(BUCKET_NAME).download_fileobj(Fileobj=data,Key=run_id)   
            res_object = data.getvalue()
            result = json.loads(res_object)
            if field:
                result = result.get(field, default_value)
            return result
        else:
            logger.info("No storages are found")
    except Exception:
        logger.error('An error occurred (NoSuchKey) when calling the GetObject operation: The specified key does not exist')
        pass


def get_response(url, type, params=None):
    start_time = int(time.time())
    logging.info(f'api type: {type}, : url : {url}')
    res = call_get_requests(url, params=None, verify=True)
    duration = int(time.time()) - start_time
    if duration > API_TIME_STACKS:
        logging.info(f'Get {type} API response took %d (greater than %d) seconds, url : {url}', duration, API_TIME_STACKS)
    return res


def get_ses_client():
    return boto3.client('ses',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)


def get_s3_client():
    return boto3.client('s3',
                        region_name=REGION_NAME,
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
    

def get_s3_ceph():
    return boto3.resource('s3',
                            endpoint_url=ENDPOINT_URL,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY)


def send_email(subject, from_email, to_emails, body, attachment=None):
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_emails

    # message body
    part = MIMEText(body, 'html')
    message.attach(part)

    if attachment:
        attachment_body = urlopen(attachment).read()
        part = MIMEApplication(attachment_body)
        part.add_header('Content-Disposition', 'attachment', filename=attachment)
        message.attach(part)

    resp = get_ses_client().send_raw_email(
        Source=message['From'],
        Destinations=to_emails.split(','),
        RawMessage={
            'Data': message.as_string()
        }
    )

    return resp


def upload_to_storage(content, location):
    '''
    :param: content: bytes
    :param: location: str
    '''
    if storage_name == 's3':
        s3 = boto3.resource('s3',
                            region_name=REGION_NAME,
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=SECRET_ACCESS_KEY)
        object_url = f'https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{location}'
        try:
            s3.Bucket(BUCKET_NAME).put_object(Body=content,
                                                 Key=location)
            #return object_url
            return location
        except Exception:
            pass
    elif storage_name == 'ceph':
        try:
            s3 = boto3.resource('s3',
                                endpoint_url=ENDPOINT_URL,
                                aws_access_key_id=ACCESS_KEY_ID,
                                aws_secret_access_key=SECRET_ACCESS_KEY)
            s3.Bucket(BUCKET_NAME).put_object(Bucket=BUCKET_NAME,
                                            Key=location,
                                            Body=content)
            #return object_url
            return location
        except Exception:
            pass
    else:
        logger.info("No storages are found")
        

def generate_pdf(analysis_run):
    logger.info('Entered into pdf generation process')
    url = os.getenv("PDF_SERVICE")
    # analysis_run = json.dumps(analysis_run)
    data = {
        'domain': BASE_API_URL,
        'report': PLATFORM_ROUTE,
        'run': analysis_run,
        'route': '/full-view',
        'token': get_token(),
        'app_id': APP_ID,
        'size': 'A4'
    }

    api_proce_before_time = time.time()
    res = requests.post(url, data=data).json()
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Pdf response is took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Pdf response is: %s', res['key'])
    return res['key']



def generate_excel(analysis_run, orgId, excel_data, report_gen_start_time, report_gen_completed_time, file_name=None):
    try:
        excel_renderer = ExcelRenderer(analysis_run, orgId, excel_data, report_gen_start_time, report_gen_completed_time)
        workbook = excel_renderer.render()
    except Exception as ex:
        raise ex

    if file_name:
        output = None
        workbook.save(file_name)
    else:
        output = BytesIO()
        workbook.save(output)

    return output


def diff_sec(st, et):
    difference = int(et - st)
    return difference


def update_status_url(analysisRunId, tenantId, genStime, genEtime, status=None):

    url = BASE_API_URL + f'/analytics/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    data={
            "status" : status,
            "runDurStartDate" : genStime,
            "runDurEndDate" : genEtime
        }
    
    api_proce_before_time = time.time()
    res = call_put_requests(url , data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Status update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Status update response is %s', res)


def update_results_url(gen_start_time, analysisRunId, tenantId, json_result_url=None, gen_completed_time=None, excel_result_url=None, pdf_result_url=None, failure_reason=None, status=None):

    url = BASE_API_URL + f'/analytics/api/v3/tenants/{tenantId}/runs/{analysisRunId}'
    
    if pdf_result_url == None:
        data={
                "status" : status,
                "resultUrl" : json_result_url,
                "xlsxFilePath" : excel_result_url,
                "repGenStartTime" : gen_start_time,
                "repGenEndTime" : gen_completed_time,
                "failureReason" : failure_reason
        }
    elif excel_result_url == None:
        data={
                "status" : status,
                "resultUrl" : json_result_url,
                "pdfFilePath" : pdf_result_url,
                "repGenStartTime" : gen_start_time,
                "repGenEndTime" : gen_completed_time,
                "failureReason" : failure_reason
        }
    else:
        data={
                "status" : status,
                "resultUrl" : json_result_url,
                "pdfFilePath" : pdf_result_url,
                "xlsxFilePath" : excel_result_url,
                "repGenStartTime" : gen_start_time,
                "repGenEndTime" : gen_completed_time,
                "failureReason" : failure_reason
        }

    api_proce_before_time = time.time()
    res = call_put_requests(url , data=json.dumps(data), verify=False);
    api_proce_after_time = time.time()
    api_proce_diff = diff_sec(api_proce_before_time, api_proce_after_time)
    if api_proce_diff > API_TIME_STACKS:
        logging.info('Database update response took %d (greater than %d) seconds', api_proce_diff, API_TIME_STACKS)
    logger.info('Database update response is %s', res)


#Upload excel file to s3
def upload_excel_s3(local_file, bucket, s3_file):
    s3 = get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_file)
        url = f'https://{bucket}.s3.{REGION_NAME}.amazonaws.com/{s3_file}'
        logger.info('Upload successful, result url is %s', url)
        
        delete_excel_file(local_file)
        return s3_file
    except FileNotFoundError:
        logger.info('File was not found')
        return False
    except NoCredentialsError:
        logger.info('Invalid credentials')
        return False


#Upload excel file to ceph
def upload_excel_ceph(local_file, bucket, s3_file):
    try:
        s3 = get_s3_ceph()
        s3.Bucket(BUCKET_NAME).upload_file(Filename = local_file, Key = s3_file)
        logger.info('Upload successful')
        delete_excel_file(local_file)
        return s3_file
    except FileNotFoundError:
        logger.info('File was not found')
        return False
    except NoCredentialsError:
        logger.info('Invalid credentials')
        return False


#Delete excel_file from local path
def delete_excel_file(source_path):
    try:
        os.remove(source_path)
        logger.info('Excel file successfully deleted')
    except OSError as e:
        logger.info(f'Failed to delete: %s : %s % {file_path, e.strerror}')


#Generate excel file
def generate_excel_file(run_id, orgId, report_gen_start_time, report_gen_completed_time):
    logger.info('Entered into excel generation process')
    excel_data=get_result_by_run(run_id, 'excel-data', {})
    reportname = f"{APP_ID.lower()}" + '-' + datetime.now().strftime('%Y-%m-%d-%I-%M-%S') + '.xlsx'
    filepath = './' + reportname
    generate_excel(run_id, orgId, excel_data, report_gen_start_time, report_gen_completed_time, filepath)
    excel_file_location = f'{PLATFORM_ROUTE}/{run_id}/xls/' + reportname
    if storage_name == 's3':
        excel_url = upload_excel_s3(filepath, BUCKET_NAME, excel_file_location)
    elif storage_name == 'ceph':
        excel_url = upload_excel_ceph(filepath, BUCKET_NAME, excel_file_location)
    else:
        logger.info("No storages are found")
    return excel_url


def init_mail(org_id, run_id):
    logger.info('Entered into init_mail method')
    try:
        url = BASE_API_URL + f'/analytics/api/v3/tenants/{org_id}/sends'
        data={
                "runId" : run_id
            }
        t1 = int(time.time())
        res = call_post_requests(url , data=json.dumps(data), verify=False);
        t2 = int(time.time())
        duration = t2-t1
        if duration > API_TIME_STACKS:
            logging.info('Status update response took %d (greater than %d) seconds', duration, API_TIME_STACKS)
        logger.info('Status update response is %s', res)
    except Exception as e:
        logger.error("Exception raised due to : " + repr(e))
        traceback.print_exc()
    logger.info('finished init_mail method')


def upload_excel(analysis_run, excel_file):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    s3_path = f'{analysis_run.analysis.app.slug}/excel/{timestamp}.xlsx'

    return upload_to_storage(excel_file, s3_path)
