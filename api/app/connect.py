from minio import Minio
from minio.error import S3Error
from io import BytesIO


def saveFile(file: BytesIO, taskID: str):
    client = Minio(
        endpoint="127.0.0.1:9000",
        secure=False,
        access_key="ROOTUSER",
        secret_key="CHANGEME123",
    )

    # Make 'filesFromUser' bucket if not exist.
    found = client.bucket_exists("user-input")
    if not found:
        client.make_bucket("user-input")


    client.fput_object("user-input", "taskID", file)


def main():
    client = Minio(
        endpoint="127.0.0.1:9000",
        secure=False,
        access_key="ROOTUSER",
        secret_key="CHANGEME123",
    )

    # Make 'filesFromUser' bucket if not exist.
    found = client.bucket_exists("user-input")
    if not found:
        client.make_bucket("user-input")




if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)