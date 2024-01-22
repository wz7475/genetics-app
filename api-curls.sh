curl --location 'localhost:8080/uploadFile' \
--form 'file=@"taskflowapi/data/100_2.tsv"' \
--form 'algorithms="pangolin,spip"'



curl -X POST 'http://localhost:8080/getResult' \
-H 'Content-Type: application/json' \
-d '"efa1d62e-f049-4d19-96b6-50d246250603"'




curl -X POST 'http://localhost:8080/getStatus' \
-H 'Content-Type: application/json' \
-d '"efa1d62e-f049-4d19-96b6-50d246250603"'


curl 'http://localhost:8080/availableAlgorithms'


curl -X POST 'http://localhost:8080/getDetailedStatus' \
-H 'Content-Type: application/json' \
-d '"efa1d62e-f049-4d19-96b6-50d246250603"'

