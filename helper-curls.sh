# enqueue job
curl --location 'localhost:8080/uploadfile' \
--form 'file=@"./taskflowapi/data/brca2_2rec.csv"'


# get result
curl --location 'localhost:8080/getResult?task_id=4dadabc5-736d-4c04-83ce-bbaa131581af'

curl --location 'localhost:8080/getResult?task_id=4dadabc5-736d-4c04-83ce-bbaa131581af'

curl --location 'localhost:8080/createOuput?id=d3aa15e9-89cd-4cbf-aed9-ed7db8c40c0a'
