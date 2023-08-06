from pathlib import Path
from tempfile import TemporaryDirectory

from moto import mock_s3


@mock_s3
def test_bucket_put(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_bucket_get(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    data, metadata = bucket.get("text.txt")
    assert data == b"test"


@mock_s3
def test_bucket_get_decode(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    data, metadata = bucket.get("text.txt", decode=True)
    assert data == "test"


@mock_s3
def test_bucket_delete(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    response = bucket.delete("text.txt")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 204


@mock_s3
def test_bucket_upload(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as upload:
        success = bucket.upload_file(upload.name, upload.name)

    assert success is True


@mock_s3
def test_bucket_download(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as upload:
        success = bucket.upload_file(upload.name, upload.name)

    assert success is True

    with create_tempfile("txt") as download:
        success = bucket.download_file(upload.name, download.name)
        assert success is True

        with open(download.name, encoding="UTF-8") as f:
            assert f.read() == "test"


@mock_s3
def test_list_all(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.txt"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_all()
    assert len(file_list) == 3


@mock_s3
def test_list_dir_root(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir()
    assert len(file_list) == 1


@mock_s3
def test_list_dir_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True)
    assert len(file_list) == 3


@mock_s3
def test_list_dir_ext_no_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(file_type="csv")

    assert file_list == []


@mock_s3
def test_list_dir_ext_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True, file_type="csv")

    assert len(file_list) == 1
    assert file_list[0] == "dir1/dir2/test.csv"


@mock_s3
def test_list_dir_ext_recursive_names_only(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test2.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True, file_type="csv", names_only=True)

    assert len(file_list) == 1
    assert file_list[0] == "test2"


@mock_s3
def test_list_dir_ext_path(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/test.csv", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(path="dir1", file_type="csv")

    assert len(file_list) == 1
    assert file_list[0] == "dir1/test.csv"


@mock_s3
def test_upload_dir(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        temp1 = create_tempfile("txt", temp_dir=temp_dir, delete=False)
        temp2 = create_tempfile("txt", temp_dir=temp_dir, delete=False)
        temp3 = create_tempfile("csv", temp_dir=temp_dir, delete=False)

        temp_subdir = TemporaryDirectory(dir=temp_dir)
        temp4 = create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)
        temp5 = create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir("/", temp_dir)

    name_list = [f.name for f in [temp1, temp2, temp3, temp4, temp5]]
    for name in name_list:
        assert status_dict[name] is True


@mock_s3
def test_upload_dir_with_file_type(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        csv = create_tempfile("csv", temp_dir=temp_dir, delete=False)

        temp_subdir = TemporaryDirectory(dir=temp_dir)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir("/testing", temp_dir, file_type="csv")

    assert status_dict[csv.name] is True


@mock_s3
def test_download_dir(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as upload_dir:

        temp1 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        temp2 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        temp3 = create_tempfile("csv", temp_dir=upload_dir, delete=False)

        upload_subdir = TemporaryDirectory(dir=upload_dir)
        temp4 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)
        temp5 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)

        status_dict = bucket.upload_dir("/", upload_dir)

    name_list = [f.name for f in [temp1, temp2, temp3, temp4, temp5]]
    for name in name_list:
        assert status_dict[name] is True

    with TemporaryDirectory() as download_dir:

        status_dict = bucket.download_dir("/", download_dir)

        for file in Path(download_dir).glob("**/*"):
            if file.is_file():
                with open(file, encoding="UTF-8") as f:
                    assert f.read() == "test"

    for name in name_list:
        key = Path(*Path(name).parts[2:])
        assert status_dict[str("/" / key)] is True


@mock_s3
def test_download_dir_with_file_type(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as upload_dir:

        txt1 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        txt2 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        csv = create_tempfile("csv", temp_dir=upload_dir, delete=False)

        upload_subdir = TemporaryDirectory(dir=upload_dir)
        txt3 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)
        txt4 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)

        status_dict = bucket.upload_dir("/", upload_dir)

    name_list = [f.name for f in [txt1, txt2, csv, txt3, txt4]]
    for name in name_list:
        assert status_dict[name] is True

    with TemporaryDirectory() as download_dir:

        status_dict = bucket.download_dir("/", download_dir, file_type="csv")

        for file in Path(download_dir).glob("**/*"):
            if file.is_file():
                with open(file, encoding="UTF-8") as f:
                    assert f.read() == "test"

    key = Path(*Path(csv.name).parts[2:])
    assert status_dict[str("/" / key)] is True
