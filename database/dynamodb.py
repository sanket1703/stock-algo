import boto3

def get_database():
    
    aws_access_key_id = 'AKIAW3MEAN3TBZIFTCE6'
    aws_secret_access_key = 'Ad2nS01Iioxl4cfqqDsXWBAoPd4SJRMqwdPpdFbj'

    # Create a DynamoDB resource object with your credentials
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='ap-south-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    
    return dynamodb