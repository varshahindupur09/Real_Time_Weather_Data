# %%
import os
import boto3
import boto3.s3
import botocore
import re
from dotenv import load_dotenv
from data.sql_aws_metadata import Metadata
from awscloud.cloudwatch.logger import write_goes_log
from utils.logger import Log
from utils import status_checker as status_check

# %%
load_dotenv()

# %%
goes_source_bucket = 'noaa-goes18'
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
src_bucket = s3.Bucket(goes_source_bucket)
target_bucket = s3.Bucket(team_source_bucket)

Log().i('Connected to AWS S3 bucket.')

# %%
def get_all_geos_file_name_by_filter(station, year, day, hour):
    Log().i(f"User requested the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {hour}")
    write_goes_log(f"User requested the files for, Station: {station}, Year: {year}, Day: {day}, Hour: {hour}")
    files_available=[]
    
    for object_summary in src_bucket.objects.filter(Prefix=  f'{station}/{year}/{day}/{hour}/'):
        file_name = object_summary.key.split('/')[-1]
        files_available.append(file_name)

    write_goes_log(f"File fetched: \n{files_available}")

    return files_available


# %%
def get_geos_aws_link(station, year, day, hour, filename):
    # Stations, Year, Day, Hour
    copy_source = {
        'Bucket': goes_source_bucket,
        'Key': f'{station}/{year}/{day}/{hour}/{filename}'
    }

    target_bucket.copy(copy_source, station + '/' + str(year) + '/' + day +'/' + hour + '/' + filename)

    metadata = Metadata()
    metadata.insert_data_into_goes(station=station, year=year, day=day, hour=hour)

    generate_link = f'https://damg7245-team-5.s3.amazonaws.com/{station}/{year}/{day}/{hour}/{filename}'
    source_link = f'https://noaa-goes18.s3.amazonaws.com/{station}/{year}/{day}/{hour}/{filename}'

    write_goes_log(f"File requested: {filename}\nGenerate link: {generate_link}\nSource link: {source_link}")
    
    Log().i(f'File requested: {filename}')
    Log().i(f'Generate link: {generate_link}')
    Log().i(f'Source link: {source_link}')

    return generate_link, source_link


def get_aws_link_by_filename(filename):
    Log().i(f"User requested  file: {filename}")
    write_goes_log(f"User requested  file: {filename}")

    y = filename.split('_')
    # print(y)
    filename_pattern = r'(.*)-(.*)'
    regex_pattern = re.compile(filename_pattern)
    res_fn = regex_pattern.findall(y[1])
    res = str(res_fn[0][0])
    end = res[-1]
    if end.isnumeric():
        res = res[:-1]
            # print(res)
            # get timestamp
    time = y[3]
    year = time[1:5]
    day = time[5:8]
    date = time[8:10]

    #combining all pieces of url
    output = "https://noaa-goes18.s3.amazonaws.com/" + res + '/' + year + '/' + day + '/' + date + '/' + filename

    if(status_check.getStatuscode(output) != 200):
        Log().i('File do not exists')
        write_goes_log(f"File requested: {filename}\nFile do not exists in GOES S3 Bucket")
        return None

    write_goes_log(f"File requested: {filename}\nGOES Bucket link: {output}")
   
    Log().i(f"File requested: {filename}")
    Log().i(f'GOES Bucket link: {output}')

    return output