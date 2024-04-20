# Kinesis Stream Reader

This Python script reads data from an Amazon Kinesis stream and provides options for displaying, filtering, and saving the data to a file.
___
## Prerequisites
* **Python 3.x**
* **AWS credentials configured**
___
## Usage
#### Run the script with the desired arguments:
`python kds_reader.py --stream_name YOUR_KDS_NAME --shard_id KDS_SHARD_ID --region KDS_REGION --display true --max_records 100 --filter "your_filter_value" --save_data true --output_file kds_data_points.json`

#### Example 1: Read from Kinesis Stream
`python kinesis_reader.py --stream_name my_kinesis_stream --shard_id shard-00001 --region us-west-2`

#### Example 2: Read and Display Data
`python kinesis_reader.py --stream_name my_kinesis_stream --shard_id shard-00001 --region us-west-2 --display true`

#### Example 3: Read, Filter, and Save Data
`python kinesis_reader.py --stream_name my_kinesis_stream --shard_id shard-00001 --region us-west-2 --filter keyword --save_data true --output_file filtered_data.json`
___
## Command Line Arguments
- `--stream_name`: Name of the Kinesis stream (default: `kds_name`)
- `--shard_id`: ID of the shard to read from (default: `12345678`)
- `--region`: AWS region where the Kinesis stream is located (default: `us-south-1`)
- `--display`: Display data (true/false) (default: `false`)
- `--max_records`: Maximum number of records to collect (optional)
- `--filter`: Property/word for filtering (optional)
- `--save_data`: Save the result to a file (true/false) (optional)
- `--output_file`: Output file name (default: `kds_data_points.json`)

> Note: To save data, either `--output_file` or `--save_data` must be passed.
___
## Author
#### Shubhanshu Jha
- GitHub: [ShubhanshuJha](https://github.com/ShubhanshuJha)
- LinkedIn: [Shubhanshu Jha](https://www.linkedin.com/in/shubhanshu-jha/)
___