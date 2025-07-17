import json
import os
import uuid
import boto3
from datetime import datetime


TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'todos') 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Handles incoming API Gateway requests and writes data to DynamoDB.
    """
    try:
        
        print(f"Received event: {json.dumps(event)}")

    
        if 'body' not in event:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Missing request body'})
            }

        body = json.loads(event['body'])

       
        task = body.get('task')
        completed = body.get('completed', False) # Default to false if not provided

        if not task:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Missing "task" in request body'})
            }

       
        todo_id = str(uuid.uuid4())
        
        created_at = datetime.utcnow().isoformat() + 'Z' # ISO 8601 format

        item = {
            'taskId': todo_id,
            'task': task,
            'completed': completed,
            'createdAt': created_at
           
        table.put_item(Item=item)

        return {
            'statusCode':
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Todo item created successfully',
                'item': item
            })
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Invalid JSON in request body'})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': f'Internal server error: {str(e)}'})
        }
