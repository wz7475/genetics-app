from taskflowapi.orchestrator.app.main import remove_other_columns
import os
import shutil
PATH_TO_ORCH_DATA = os.path.join('tests', 'data', 'orch')

def test_removing_columns():
    """
    doesnt work - no logger package due to the way of mounting modules
    :return:
    """
    source = os.path.join(PATH_TO_ORCH_DATA, "orginal-tsv.tsv")
    tmp_copy = os.path.join(PATH_TO_ORCH_DATA, "copy_tmp-tsv.tsv")
    shutil.copy2(source, tmp_copy)

    with open(source, 'r', encoding='utf-8') as file1, open(tmp_copy, 'r', encoding='utf-8') as file2:
        content1 = file1.read()
        content2 = file2.read()
        assert content1 == content2

    remove_other_columns(tmp_copy)
    os.remove(tmp_copy)