import json
from cases.models import TestCase
from tasks.models import TestTask,TaskCaseRelevance
import os
from backend.settings import BASE_DIR
from tasks.task_running.test_result import save_test_result
import threading
import jmespath
data_dir = os.path.join(BASE_DIR,'tasks','task_running','test_data.json')
test_dir = os.path.join(BASE_DIR,'tasks','task_running','test_case.py')


def run_task(task_id):
    print("1.读取测试用例")
    relevance = TaskCaseRelevance.objects.get(task_id=task_id)
    relevance_list = relevance.case.replace("\'","\"")
    relevance_list = json.loads(relevance_list)
    case_ids = []
    for rel in relevance_list:
        case_ids = case_ids + rel["casesId"]
    print(case_ids)
    data = {}
    for cid in case_ids:
        try:
            case = TestCase.objects.get(id=cid,is_delete=False)
            # list.append(model_to_dict(case)
            params_body = case.params_body.replace("\'","\"")
            header = case.header.replace("\'","\"")
            header_dict = json.loads(header)
            params_body_dict = json.loads(params_body)
            data[case.name] = {
                "case_id":case.id,
                "url": case.url,
                "method": case.method,
                "header": header_dict,
                "params_type": case.params_type,
                "params_body": params_body_dict,
                "assert_type": case.assert_type,
                "assert_text":case.assert_text
            }
        except TestCase.DoesNotExist:
            pass
    #写入测试用例至test_data.json
    print("2.写入测试用例至test_data.json")
    with open(data_dir,"w") as f:
        f.write(json.dumps(data,ensure_ascii=False))
    #执行测试用例
    print("3.执行测试用例")
    os.system(f"python {test_dir}")
    #保存测试结果
    print("4.保存测试结果")
    save_test_result(task_id)
    task = TestTask.objects.get(id=task_id)
    task.status = 2
    task.save()

def run1(task_id):
    threads = []
    t = threading.Thread(target=run_task,args=(task_id,))
    threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()

def run2(task_id):
    threads = []
    t = threading.Thread(target=run1,args=(task_id,))
    threads.append(t)
    for i in threads:
        i.start()