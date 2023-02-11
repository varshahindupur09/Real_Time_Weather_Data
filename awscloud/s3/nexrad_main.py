# %%
import os
import boto3
import boto3.s3
import botocore
from dotenv import load_dotenv
import re
from data.sql_aws_metadata import Metadata
from awscloud.cloudwatch.logger import write_nexrad_log
from utils.logger import Log
from utils import status_checker as status_check

# %%
load_dotenv()

# %%
Log().i('Connecting... to AWS S3 bucket.')

nexrad_source_bucket = 'noaa-nexrad-level2'
team_source_bucket = os.environ.get('TARGET_BUCKET_NAME')

# %%
session = boto3.Session(
    region_name='us-east-1',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET')
)

# %%
s3 = session.resource('s3')

# %%
src_bucket = s3.Bucket(nexrad_source_bucket)
target_bucket = s3.Bucket(team_source_bucket)

Log().i('Connected to AWS S3 bucket.')


# %%
def get_all_nexrad_file_name_by_filter(year, month, day, station):
    
    Log().i(f"User requesting the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {station}")

    write_nexrad_log(f"User requested the files for, Year: {year}, Month: {month}, Day: {day},  Station: {station}")
    files_available = []

    for object_summary in src_bucket.objects.filter(Prefix=f'{year}/{month}/{day}/{station}/'):
        files_available.append(object_summary.key.split('/')[-1])

    write_nexrad_log(f"File fetched: \n{files_available}")

    return files_available


# %%
def get_nexrad_aws_link(year, month, day, station_id, filename):
    # Stations, Year, Day, Hour
    Log().i(f'Requesting file: {filename}')

    copy_source = {
        'Bucket': nexrad_source_bucket,
        'Key': f'{year}/{month}/{day}/{station_id}/{filename}'
    }

    target_bucket.copy(copy_source, str(year) + '/' + str(month) + '/' + str(day) + '/' + str(station_id) + '/' + str(filename))

    metadata = Metadata()
    metadata.insert_data_into_nexrad(station_id=station_id, year=year, month=month, day_of_year=day)

    generated_link = f'https://damg7245-team-5.s3.amazonaws.com/{year}/{month}/{day}/{station_id}/{filename}'
    source_link = f'https://noaa-nexrad-level2.s3.amazonaws.com/{year}/{month}/{day}/{station_id}/{filename}'

    write_nexrad_log(f"File requested: {filename}\nGenerate link: {generated_link}\nSource link: {source_link}")
    
    Log().i(f'File requested: {filename}')
    Log().i(f'Generate link: {generated_link}')
    Log().i(f'Source link: {source_link}')

    return generated_link, source_link


def get_nexrad_aws_link_by_filename(filename):
    write_nexrad_log(f"User requested  file: {filename}")
    y = filename.split('_')[0]
    # print(y)
    res = y[:4]
    year = y[4:8]
    day = y[8:10]
    date = y[10:12]
    # print(res, year, day, date)

    # combining all pieces of url
    output = "https://noaa-nexrad-level2.s3.amazonaws.com/" + year + '/' + day + '/' + date + '/' + res + '/' + filename

    if(status_check.getStatuscode(output) != 200):
        Log().i('File do not exists')
        write_nexrad_log(f"File requested: {filename}\nFile do not exists in NEXRAD S3 Bucket")
        return None
    

    write_nexrad_log(f"File requested: {filename}\nGOES Bucket link: {output}")
    
    Log().i(f"File requested: {filename}")
    Log().i(f'GOES Bucket link: {output}')

    return output