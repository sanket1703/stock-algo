

from jobs.clean_json import clean_order_jsons_job
from jobs.mo_login_check_job import check_login_job


def pre_order_executor_job():
    check_login_job()
    clean_order_jsons_job()
    
