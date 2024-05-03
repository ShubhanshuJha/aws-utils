import boto3
import json
import argparse


def read_kinesis_stream(kds_stream_name, stream_shard_id, kds_region, max_records, display_data, filter_value, get_records):
    kinesis_client = boto3.client('kinesis', region_name=kds_region)
    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=kds_stream_name,
        ShardId=stream_shard_id,
        ShardIteratorType='TRIM_HORIZON'  # Read from the beginning of the shard
    )['ShardIterator']
    display_data = display_data.lower() == 'true'
    data_collection = []
    if not get_records:
        record_counter = 0

    while True:
        records_response = kinesis_client.get_records(
            ShardIterator=shard_iterator,
            Limit=100  # Adjust batch size as needed
        )

        records = records_response.get('Records', [])
        for record in records:
            data = record['Data'].decode('utf-8')
            if filter_value and filter_value not in data:
                continue
            if get_records:
                data_collection.append(data)
            else:
                record_counter += 1
            if display_data:
                print(data)
            if max_records and ((get_records and len(data_collection) >= max_records) or (not get_records and record_counter == max_records)):
                return data_collection
        shard_iterator = records_response.get('NextShardIterator')
        if not shard_iterator:
            break
    return data_collection


def write_to_file(file_name, stream_data):
    if not stream_data:
        print('No Data To Be Saved.')
        return
    try:
        stream_data_json = [json.loads(item) for item in stream_data]
        with open(file_name, 'w') as f:
            json.dump(stream_data_json, f)
        print('*' * 100)
        print('Data Saved Successfully.')
        print('*' * 100)
    except Exception as e:
        print('Data Saving Failed:', str(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyse latency of a Kinesis stream')
    parser.add_argument('--stream_name', type=str, default='kds_name', help='Name of the Kinesis stream')  # Change kds name
    parser.add_argument('--shard_id', type=str, help='ID of the shard to read from')  # Change shard id
    parser.add_argument('--region', type=str, default='us-south-1', help='AWS region where the Kinesis stream is located')  # Adjust region as needed
    parser.add_argument('--display', type=str, default='false', help='Display data: true or false [By default false]')
    parser.add_argument('--max_records', type=int, help='Maximum number of records to collect (optional)')
    parser.add_argument('--filter', type=str, help='Enter the property/word for filtering (optional)')
    parser.add_argument('--save_data', type=str, help='Want to save the result: true/false (optional)')
    parser.add_argument('--output_file', type=str, default='kds_data_points.json', help='Enter the output file name (optional)')
    args = parser.parse_args()

    write_output = args.save_data.lower() == 'true' if args.save_data else (True if args.output_file else False)
    data = read_kinesis_stream(kds_stream_name=args.stream_name, stream_shard_id=args.shard_id, kds_region=args.region,
                               max_records=args.max_records, display_data=args.display, filter_value=args.filter, get_records=write_output)
    if write_output:
        write_to_file(file_name=args.output_file, stream_data=data)
