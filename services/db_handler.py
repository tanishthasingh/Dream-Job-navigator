import streamlit as st
import boto3
import json
import time
import hashlib
from botocore.exceptions import ClientError

def get_db_client():
    """
    Initializes and returns a DynamoDB client using credentials from secrets.toml.
    Returns None if secrets are missing.
    """
    if "aws" not in st.secrets:
        return None
    
    try:
        session = boto3.Session(
            aws_access_key_id=st.secrets["aws"]["aws_access_key_id"],
            aws_secret_access_key=st.secrets["aws"]["aws_secret_access_key"],
            region_name=st.secrets["aws"]["region_name"]
        )
        return session.resource('dynamodb')
    except Exception as e:
        st.error(f"AWS Connection Error: {e}")
        return None

def create_table_if_missing():
    """
    Checks if the table exists, creates it if not.
    Returns the Table resource or None on failure.
    """
    dynamodb = get_db_client()
    if not dynamodb:
        return None
        
    table_name = st.secrets["aws"].get("dynamo_table_name", "user_profiles")
    table = dynamodb.Table(table_name)
    
    try:
        table.load()
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            try:
                # Create the table
                table = dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
                    AttributeDefinitions=[{'AttributeName': 'user_id', 'AttributeType': 'S'}],
                    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                )
                # Wait until the table exists.
                table.wait_until_exists()
                return table
            except ClientError as create_error:
                st.error(f"Failed to create table: {create_error}")
                return None
        else:
            st.error(f"Database Error: {e}")
            return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password):
    """
    Creates a new user with email and hashed password.
    Returns (Success, Message).
    """
    table = create_table_if_missing()
    if not table:
        return False, "Database connection failed."

    # Check if user exists
    try:
        response = table.get_item(Key={'user_id': email})
        if 'Item' in response:
            return False, "User already exists. Please login."
    except ClientError:
        pass # Proceed

    # Create user
    try:
        item = {
            'user_id': email,
            'password': hash_password(password),
            'created_at': int(time.time()),
            'data': "{}" # Empty profile data initially
        }
        table.put_item(Item=item)
        return True, "Account created successfully!"
    except ClientError as e:
        return False, f"Error creating account: {e}"

def verify_user(email, password):
    """
    Verifies user credentials.
    Returns (Success, Message/Data).
    """
    table = create_table_if_missing()
    if not table:
        return False, "Database connection failed."

    try:
        response = table.get_item(Key={'user_id': email})
        if 'Item' not in response:
            return False, "User not found."
        
        saved_pass = response['Item'].get('password')
        if saved_pass == hash_password(password):
            # Load stored profile data too
            profile_data_str = response['Item'].get('data', '{}')
            try:
                profile_data = json.loads(profile_data_str)
            except:
                profile_data = {}
            return True, profile_data
        else:
            return False, "Incorrect password."
    except ClientError as e:
        return False, f"Login error: {e}"

def save_profile(user_id, analysis_data):
    """
    Saves the user's analysis result to DynamoDB.
    """
    table = create_table_if_missing()
    if not table:
        return False
    
    try:
        # Preserve existing password/created_at if simple put overwrite (DynamoDB PUT replaces whole item)
        # Better: UpdateItem. But for simplicity, we get then put, or just update 'data' attribute.
        # Let's use UpdateItem to only update 'data'
        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="set #d = :v",
            ExpressionAttributeNames={'#d': 'data'},
            ExpressionAttributeValues={':v': json.dumps(analysis_data)}
        )
        return True
    except ClientError as e:
        st.error(f"Failed to save to database: {e}")
        return False

def load_profile(user_id):
    """
    Loads a user's profile from DynamoDB.
    """
    table = create_table_if_missing()
    if not table:
        return None
    
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            # Parse the JSON string back to a dict
            data_str = response['Item'].get('data', '{}')
            return json.loads(data_str)
        else:
            return None
    except ClientError as e:
        st.error(f"Failed to load from database: {e}")
        return None
