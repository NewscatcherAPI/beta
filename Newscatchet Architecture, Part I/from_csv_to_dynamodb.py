import boto3
import os
import csv
import tempfile
import json

def read_csv(file):
    items = []
    with open(file, encoding='mac_roman') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            items.append(json.loads(json.dumps(row)))
    return items


if __name__ == '__main__':

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLE_NAME')

    s3 = boto3.client('s3')
    source_bucket = 'BUCKET_NAME_ON_S3'
    key = 'CSV_FILE_NAME.csv'

    with tempfile.TemporaryDirectory() as tmpdir:
        download_path = os.path.join(tmpdir, key)
        s3.download_file(source_bucket, key, download_path)
        items = read_csv(download_path)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)