import os
import sys
import uuid
import boto3
import botocore
import sagemaker
import json
import yaml
import time
import pickle
import shutil
import tarfile
import zipfile
import pandas as pd
from typing import Union, List
from tqdm.auto import tqdm
from time import sleep
from io import BytesIO
from yaspin import yaspin
from yaspin.spinners import Spinners
from urllib.parse import urlparse
from boto3.s3.transfer import TransferConfig
from concurrent.futures import ThreadPoolExecutor, as_completed
from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput


default_session = boto3.Session()

class Settings:
    spinner_type = Spinners.clock
    spinner_color = 'blue'
    spinner_ok = '✅'
    spinner_fail = '💥'

def create_or_update_iam_role(role_name: str, role_desc: str, asume_role_policy_document: dict, policy_name: str, policy_document: dict, session = default_session) -> str:
    '''
    Given a role name, roles description, a policy document and asume role policy document, creates or updates an IAM role
    
    Args:
        role_name (str): IAM role name
        role_desc (str): role description
        asume_role_policy_document (dict): policy document that grants an IAM entity permission to assume the role
        policy_name (str): name of the policy document
        policy_document (dict): the policy document
        
    Returns:
        The arn of the role created or updated
    '''
    
    iam = session.client('iam')
    
    response = None
    try:
        role_response = iam.get_role(RoleName=role_name)                 
        
        print('INFO: Role already exists, updating it...')
        role_arn = role_response['Role']['Arn']
        
        iam.update_role(RoleName=role_name, Description=role_desc)
                        
        iam.update_assume_role_policy(RoleName=role_name, PolicyDocument=json.dumps(asume_role_policy_document))
                        
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document))
        
        print('INFO: Role updated: {}'.format(role_name))
        
        response = role_arn
        
    except iam.exceptions.NoSuchEntityException as e:
        print('INFO: Role does not exist, creating it...')
        try:
            create_role_response = iam.create_role(           
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(asume_role_policy_document),
                Description=role_desc)                     
            
            role_arn = create_role_response['Role']['Arn']

            iam.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document))
            
            print('INFO: Role created: {}'.format(role_arn))
            
            response = role_arn
            
        except Exception as e:
            print('ERROR: Failed to create role: {}'.format(role_name))
            print(e)
            
    except Exception as e:
        print('ERROR: Failed to update role: {}'.format(role_name))
        print(e)
        
    return response

def create_codebuild_execution_role(role_name: str, policy_document: dict) -> str:
    '''
    Given a role name, and a policy document creates or updates an IAM role for CodeBuild jobs
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        The arn of the role created or updated
    '''
    
    
    
    assume_role_document={
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "codebuild.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for CodeBuild', 
                                         asume_role_policy_document = assume_role_document,
                                         policy_name = 'CodeBuildExecutionPolicy',
                                         policy_document = policy_document)
    
    # Wait for role to propagate
    sleep(60)
    
    return response

def create_lambda_execution_role(role_name: str, policy_document: dict) -> str:    
    '''
    Given a role name, and a policy document creates or updates an IAM role for Lambda functions
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        The arn of the role created or updated
    '''
    lambda_asume_role_document = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for Lambda functions', 
                                         asume_role_policy_document = lambda_asume_role_document,
                                         policy_name = 'LambdaExecutionPolicy',
                                         policy_document = policy_document)
    
    # Wait for role to propagate
    sleep(60)
    
    return response
    

def create_pipeline_execution_role(role_name: str, policy_document: dict) -> str:    
    '''
    Given a role name, and a policy document creates or updates an IAM role for SageMaker Pipelines
    
    Args:
        role_name (str): IAM role name
        policy_document (dict): Policy document
        
    Returns:
        The arn of the role created or updated
    '''
    assume_role_document={
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": "events.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }]
        }

    response = create_or_update_iam_role(role_name = role_name, 
                                         role_desc = 'Execution role for EventBridge', 
                                         asume_role_policy_document = assume_role_document,
                                         policy_name = 'CodeBuildExecutionPolicy',
                                         policy_document = policy_document)

    # Wait for role to propagate
    sleep(60)
    
    return response
    


def create_secret(secret_name: str, username: str, password: str, session = default_session) -> None:
    '''
    Given a secret name, user name and a password creates or updates Secret on Secrets Manager
    
    Args:
        secret_name (str): Secret name to create or update
        username (str): User name to store on the secret
        password (str): Password to store on the secret
        
    '''
    secretsmanager = session.client('secretsmanager')
    secret_string = f'{{"username":"{username}","password":"{password}"}}'
    description = 'Docker hub credentials'

    try:
        secretsmanager.create_secret(Name=secret_name,
                                     Description=description,
                                     SecretString=secret_string)
        print('INFO: Secret created')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            print('INFO: Secret already exists, updating it...')
            try:
                secretsmanager.update_secret(SecretId=secret_name,
                                             Description=description,
                                             SecretString=secret_string)
                print(f'INFO: Secret {secret_name} updated')
            except Exception as e:
                print(f'ERROR: Failed to create secret: {secret_name}')
                print(e)
        else:        
            print('ERROR: Failed to create secret')
            print(e) 

def create_image_repository(repository_name: str, session = default_session) -> None:
    '''
    Given a repository name creates a repository on ECR if it doesn't exist
    
    Args:
        repository_name (str): Repository name to be created
        
    '''
    ecr = session.client('ecr')
    try:
        repositories = ecr.describe_repositories(repositoryNames=[repository_name])['repositories']
        if len(repositories) > 0:
            print(f'INFO: Repository {repository_name} already exists')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'RepositoryNotFoundException':
            ecr.create_repository(repositoryName=repository_name)
        else:
            print('ERROR: Failed to describe repository: {}'.format(repository_name))
            print(e)

def _remove_path_prefix(path: str) -> str:
    prefixes = './,../,/'.split(',')
    to_remove = list(filter(path.startswith, prefixes))
    return path if len(to_remove)==0 else path.replace(to_remove[0],'',1)  

def _add_path_sufix(path: str) -> str:
    if os.path.isdir(path) and path[-1]!='/':
        path += '/'
    return path
        
def _fix_path(path: str) -> str:
    return _add_path_sufix(_remove_path_prefix(path))
    
def build_and_publish_docker_image(image_name: str, working_directory: str, docker_file: str, s3_path: str, role: str, **kwargs) -> str: 
    #Create build spec
    build = {'version':0.2,
             'phases':{'pre_build':{'commands':[
                 'echo Logging in to Amazon ECR...',
                 'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com',
                 'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin 763104351884.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com']},
                       'build':{'commands':[
                 'echo Build started on `date`',
                 'echo Building the Docker image...',
                 'docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .',
                 'docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG']},
                       'post_build':{'commands':[
                 'echo Build completed on `date`',
                 'echo Pushing the Docker image...',
                 'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG',                 
                 'echo Pushing completed on `date`',]}
                      }
            }
    
    if 'secret' in kwargs:
        build['phases']['pre_build']['commands'].append('docker login -u $dockerhub_username -p $dockerhub_password')
    
    with open(os.path.join(working_directory,'buildspec.yml'), 'w') as f:
        yaml.dump(build, f)
        
    
    zip_file_name = os.path.join(working_directory, f'{image_name}.zip')
    
    #Remove file if already exists
    if os.path.exists(zip_file_name):
        os.remove(zip_file_name)
    
    #Create source package
    def zipdir(path, ziph):
        #base=path.split('/')[0]
        base='/'.join(path.split('/')[:-1])
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),os.path.join(root, file).replace(f'{base}/',''))
                replace = os.path.join(root, file).replace(f'{base}/','')
        
    with zipfile.ZipFile(zip_file_name, mode='w') as zf:
        zf.write(os.path.join(working_directory,'Dockerfile'),'Dockerfile')
        zf.write(os.path.join(working_directory,'buildspec.yml'),'buildspec.yml')
    
        #Copy dependencies
        for dependency, _ in kwargs.get('dependencies',[]):
            if os.path.isdir(dependency):
                shutil.copytree(dependency, os.path.join(working_directory, _remove_path_prefix(dependency)))                
                zipdir(os.path.join(working_directory, dependency.split('/')[-1]), zf)
                
            elif os.path.isfile(dependency):
                dest = os.path.join(working_directory,_remove_path_prefix(dependency))
                dest_folder = os.path.dirname(dest)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                shutil.copy(dependency, dest)
                zf.write(dest,_remove_path_prefix(dependency))
                
            else:
                print(f'ERROR: unable to copy dependency: {dependency}')
                

    #Upload to S3
    source_location = upload(zip_file_name,s3_path,show_progress=False).replace('s3://','')

    if 'session' in kwargs:
        codebuild = kwargs.pop('session').client('codebuild')
    else:
        codebuild = default_session.client('codebuild')
                         
    region = sagemaker.Session().boto_region_name
    account_id = sagemaker.Session().account_id()
    project_name = f'{image_name}-build-image'
    parameters = {'name': project_name,
                  'description':'Builds a docker image to be used with SageMaker',
                  'source':{'type':'s3', 'location':source_location},
                  'artifacts':{'type':'NO_ARTIFACTS'},
                  'environment':{'type':'LINUX_CONTAINER',
                                 'image':'aws/codebuild/standard:4.0',
                                 'computeType':'BUILD_GENERAL1_SMALL',
                                 'environmentVariables':[{'name':'AWS_DEFAULT_REGION',
                                                          'value':region},
                                                         {'name':'AWS_ACCOUNT_ID',
                                                          'value':account_id},
                                                         {'name':'IMAGE_REPO_NAME',
                                                          'value':image_name},
                                                         {'name':'IMAGE_TAG',
                                                          'value':'latest'}],
                                 'privilegedMode':True},
                  'serviceRole':role}
    
    if 'secret' in kwargs:
        secret_name = kwargs['secret']
        parameters['environment']['environmentVariables'].append({'name':'dockerhub_username',
                                                                  'value':f'{secret_name}:username',
                                                                  'type':'SECRETS_MANAGER'})
        parameters['environment']['environmentVariables'].append({'name':'dockerhub_password',
                                                                  'value':f'{secret_name}:password',
                                                                  'type':'SECRETS_MANAGER'})
    try:
        codebuild.create_project(**parameters)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            codebuild.update_project(**parameters)
        else:
            print('ERROR: Failed to create codebuild project')
            print(e)                  
                         
    try:
        build_id = codebuild.start_build(projectName=project_name)['build']['id']   
        
        if kwargs.get('wait',True):                         
            with yaspin(Settings.spinner_type , text='Building docker image', color=Settings.spinner_color) as sp:         
                while True:            
                    build_response = codebuild.batch_get_builds(ids=[build_id])
                    status = build_response['builds'][0]['buildStatus']            
                    if status != 'IN_PROGRESS':
                        sp.write(f'{image_name.ljust(48,".")}{status}')
                        if status == 'SUCCEEDED':
                            sp.ok(Settings.spinner_ok)                                                                                    
                            return f'{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest'
                        else:                            
                            sp.fail(Settings.spinner_fail)
                            raise Exception(f'{image_name} {status} ')                        
                    else:                        
                        time.sleep(10)
        else:
            return build_id

    except botocore.exceptions.ClientError as e:
        print('ERROR: Failed to start codebuild project')
        print(e) 

def wait_for_build(codebuild_ids: list, session = default_session) -> None:
    '''
    Given a code build ids list creates waits for those builds on Code Build to finish
    
    Args:
        codebuild_ids (str): Code build ids
        
    '''
    codebuild = session.client('codebuild')

    region = sagemaker.Session().boto_region_name
    account_id = sagemaker.Session().account_id()
                         
    finished = True
    latest_status = {}          

    with yaspin(Settings.spinner_type , text="Building docker images", color=Settings.spinner_color) as sp:
        while True:
            build_response = codebuild.batch_get_builds(ids=codebuild_ids)
            for response in build_response['builds']:  
                if response['buildStatus'] != 'IN_PROGRESS':                    
                    if response['id'] not in latest_status:
                        sp.write(f'{response["id"].split(":")[0].ljust(48,".")}{response["buildStatus"]}!')
                        latest_status[response['id']] = response['buildStatus']
                else:
                    finished = False
                
                            
            if finished:                  
                if len([latest_status[status] for status in latest_status if latest_status[status] == 'SUCCEEDED']) == len(latest_status):
                    sp.ok(Settings.spinner_ok)
                    break
                else:
                    sp.fail(Settings.spinner_fail)
                    raise Exception('Building some images failed!')                
            else:
                finished = True
                time.sleep(10)
    
    image_uris = {}
    for codebuild_id in codebuild_ids:
        image_name = codebuild_id.split(":")[0].replace("-build-image","")
        image_uris[codebuild_id] = f'{account_id}.dkr.ecr.{region}.amazonaws.com/{image_name}:latest'
                      
    return image_uris                   
       
def create_docker_file(file_name, base_image, libraries, **kwargs):
    with open(file_name,'w') as f:
        f.write(f'FROM {base_image}')
        f.write('\n\n')
        f.write('RUN rm -rf /usr/share/man/man1/; mkdir /usr/share/man/man1/ \n')
        f.write('\n')
        f.write('RUN apt-get update -y && apt-get -y install python3-dev gcc --no-install-recommends default-jdk \n')
        f.write('\n')
        
        f.write('RUN pip3 install --no-cache-dir --upgrade pip \n')
        f.write('\n') 
        
        f.write('RUN pip3 install retrying')
        for library in libraries:
            f.write(f' \\\n    {library}=={libraries[library]}')
        f.write('\n\n')            
        
        for dependency in kwargs.get('dependencies',[]):
            f.write(f'COPY {_fix_path(dependency[0])} {dependency[1]}\n')
        f.write('\n')        
        
        for cmd in kwargs.get('others',[]):
            f.write(f'{cmd} \n')
            f.write('\n')
        
        f.write('ENV PYTHONDONTWRITEBYTECODE=1 \\\n')
        f.write('    PYTHONUNBUFFERED=1 \\\n')
        f.write('    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib" \\\n')
        f.write('    PYTHONIOENCODING=UTF-8 \\\n')
        f.write('    LANG=C.UTF-8 \\\n')
        f.write('    LC_ALL=C.UTF-8')
        env = kwargs.get('env',{})
        for variable in env:
            f.write(f' \\\n    {variable}={env[variable]}')
            
        if 'entrypoint' in kwargs:
            f.write('\n\n')
            f.write(f'ENTRYPOINT {json.dumps(kwargs["entrypoint"])}')
            
        if 'cmd' in kwargs:
            f.write('\n\n')
            f.write(f'CMD {json.dumps(kwargs["cmd"])}')
            
def create_docker_image(image_name: str, base_image: str = None, libraries: dict = {}, s3_path: str = None, role: str = None, **kwargs)->str:
    '''
    Creates a custom Docker image to be used with SageMaker using Code Build 
    
    Args:
        image_name (str): Docker image name
        base_image (str): base image to be used to build the new Docker image
        libraries (dict): set of libraries to install on the Docker image
        s3_path (str): S3 path where the Docker image files are going to be stored
        role (str): CodeBuild role to be used
        docker_file: docker file to be used instead of creating a new one
        working_directory: local path where Docker image files are going to be stored
        dependencies: files to include within the Docker image
        **kwargs: other parameters
            wait (bool): whether to wait for the build process to finish or not
            secret (str): secret name to be used to pull the base image
        
    Returns:
        The arn of the role created or updated
    '''
     #Create working directory
    if 'working_directory' not in kwargs:
        working_directory = os.path.join('docker_images', image_name)
    else:
        working_directory = os.path.join(kwargs.pop('working_directory'), image_name)

    if os.path.exists(working_directory):
        shutil.rmtree(working_directory)
    os.makedirs(working_directory)
    
    docker_file = os.path.join(working_directory,'Dockerfile')    
    if 'docker_file' in kwargs:        
        shutil.copy(kwargs.pop('docker_file'), docker_file)
    else:        
        create_docker_file(docker_file, base_image, libraries, **kwargs)

    create_image_repository(image_name)
    return build_and_publish_docker_image(image_name, working_directory, docker_file, s3_path, role, **kwargs)  
            
def wait_for_training_jobs(estimators):
    statuses = ['Completed','Failed','Stopped']

    with yaspin(Settings.spinner_type , text="Waiting for training jobs to finish", color=Settings.spinner_color) as sp:
        while True:
            finished = True        
            
            latest_status = {}
            for estimator in estimators:     
                latest_training_job = estimators[estimator].latest_training_job.describe()
                status = latest_training_job['TrainingJobStatus']
                job_name = latest_training_job['TrainingJobName']
                
                finished *= status in statuses

                if job_name not in latest_status and status in statuses:
                    latest_status[job_name]=status
                    sp.write(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')                      
                
            if finished:
                if len([latest_status[status] for status in latest_status if latest_status[status] == 'Completed']) == len(latest_status):
                    sp.ok(Settings.spinner_ok)
                    break
                else:
                    sp.fail(Settings.spinner_fail)
                    raise Exception('Some training jobs have failed!')   
                
                     
                
            else:
                time.sleep(10)
        
def wait_for_optmimization_jobs(tuners):
    statuses = ['Completed','Failed','Stopped']

    with yaspin(Settings.spinner_type , text="Waiting for optimization jobs to finish", color=Settings.spinner_color) as sp:
        while True:
            finished = True        
            
            latest_status = {}
            for tuner in tuners:
                optimization_job = tuners[tuner].describe()
                status = optimization_job['HyperParameterTuningJobStatus']
                job_name = optimization_job['HyperParameterTuningJobName']
                
                finished *= status in statuses    

                if job_name not in latest_status and status in statuses:
                    latest_status[job_name]=status    
                    sp.write(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')                          
                
            if finished:
                if len([latest_status[status] for status in latest_status if latest_status[status] == 'Completed']) == len(latest_status):
                    sp.ok(Settings.spinner_ok)
                    break
                else:
                    sp.fail(Settings.spinner_fail)
                    raise Exception('Some optimization jobs have failed!')   

            else:
                time.sleep(10)

def wait_for_transform_jobs(transformers, session = default_session):
    sm_client = session.client('sagemaker')

    statuses = ['Completed','Failed','Stopped']    

    with yaspin(Settings.spinner_type , text="Waiting for transform jobs to finish", color=Settings.spinner_color) as sp:
        while True:
            finished = True        
            
            latest_status = {}
            for transform in transformers:
                job_name = transformers[transform].latest_transform_job.job_name
                status = sm_client.describe_transform_job(TransformJobName=job_name)['TransformJobStatus']
                
                finished *= status in statuses       

                if job_name not in latest_status and status in statuses:
                    latest_status[job_name]=status    
                    sp.write(f'{job_name.ljust(70,".")}{latest_status[job_name]}!')                       
                
            if finished:
                if len([latest_status[status] for status in latest_status if latest_status[status] == 'Completed']) == len(latest_status):
                    sp.ok(Settings.spinner_ok)
                    break
                else:
                    sp.fail(Settings.spinner_fail)
                    raise Exception('Some transform jobs have failed!')   

            else:
                time.sleep(10)


def create_lambda_function(**kwargs): 
    if 'session' in kwargs:
        lambda_client = kwargs.pop('session').client('lambda')
    else:
        lambda_client = default_session.client('lambda')
    
    
    response = {None}
    try:
        function_name = kwargs['FunctionName']
        response = lambda_client.get_function(FunctionName=function_name)  
                    
        #Update function, because it was found. So, it does already exist
        code = None
        if 'Code' in kwargs:
            code = kwargs.pop('Code')
            
        kwargs.pop('PackageType')

        response = lambda_client.update_function_configuration(**kwargs)        
              

        if code != None:
    
            update_parameters = {
                'FunctionName':function_name,
                'Publish':True}

            update_parameters.update(code)
            response = lambda_client.update_function_code(**update_parameters)
        
        
    except lambda_client.exceptions.ResourceNotFoundException as e:
        try:
            #Create function, because it doesn't exist
            response = lambda_client.create_function(**kwargs)
          
        except botocore.exceptions.ClientError as e:
            print('Failed to create function: {}'.format(kwargs['FunctionName']))
            print(e)            
    except botocore.exceptions.ClientError as e:
        print('Failed to update function: {}'.format(kwargs['FunctionName']))
        print(e)   
        
    return response

def list_model_packages(model_package_group_name, session = default_session):
    sm_client = session.client('sagemaker')
    model_packages_paginator = sm_client.get_paginator('list_model_packages')
    model_packages_iterator = model_packages_paginator.paginate(ModelPackageGroupName=model_package_group_name)
    return [model_package for model_packages_page in model_packages_iterator for model_package in model_packages_page['ModelPackageSummaryList']]


def delete_model_package(mdel_package_name, session = default_session):
    sm_client = session.client('sagemaker')
    sm_client.delete_model_package(ModelPackageName=mdel_package_name)
    

def delete_model_packages(model_package_group_name):
    model_packages = list_model_packages(model_package_group_name)
    for model_package in model_packages:
        delete_model_package(model_package['ModelPackageArn'])
        
def delete_project(project_name, session = default_session):
    sm_client = session.client('sagemaker')
    sm_client.delete_project(ProjectName=project_name)

def get_processor_output_path(processor, output_name):
    return next((output.destination 
               for output in processor.latest_job.outputs 
                   if output.output_name == output_name),
           None) 

def get_tuner_best_model_artifacts_path(tuner: sagemaker.tuner.HyperparameterTuner, session = default_session) -> str:
    '''
    Gets best training job of a given tuner to then get its model artifacts S3 path

    Args:
        model artifacts s3 path
    '''
    sm = session.client('sagemaker')
    best_training_job = tuner.describe()['BestTrainingJob']['TrainingJobName']
    return sm.describe_training_job(TrainingJobName=best_training_job)['ModelArtifacts']['S3ModelArtifacts']

def upload(files: Union[str, List[str]], s3_path: str, show_progress=True, session = default_session) -> Union[str, None]:
    '''
    Uploads files or directories to S3
    
    Args:
        files (list|str): file|dir name or list of files or directories to upload to S3
        s3_path (str): S3 path where the files are going to be uploaded
        show_progress (bool): whether to show the progress of the upload
        
    Returns:
        The s3 path where the file was uploaded, if was given a list of files, it doesn't return anything
    '''
    GB = 1024 ** 3
    MULTIPART_THRESHOLD = GB/200
    MAX_CONCURRENCY = 10
    NUM_DOWNLOAD_ATTEMPTS = 10
    USE_THREADS = True

    s3 = session.client('s3')

    path_parts = [part for part in s3_path.replace('s3://','').split('/') if part]
    bucket = path_parts.pop(0)
    prefix = '/'.join(path_parts)    

    files = [files] if isinstance(files,str) else files if isinstance(files, list) else None

    if files == None:
        raise Exception(f"You have to specify the file or files you want to upload to S3.")

    def get_total_size(files):
        total_size = 0
        for path in files:                
            if os.path.isfile(path):                                                        
                total_size += os.stat(path).st_size
            elif os.path.isdir(path):        
                for (root,dirs,files) in os.walk(path, topdown=True):
                    for file in files:    
                        file_path = os.path.join(root,file)                                                                            
                        total_size += os.stat(file_path).st_size
        return total_size 

    def upload_file(bucket, prefix, file_name, dirname, callback):
        try: 
            key = f'{prefix}/{file_name.replace(dirname,"")}'
            params = {
                    'Filename': file_name,
                    'Bucket': bucket, 
                    'Key': key,                                     
                    'Config': TransferConfig(multipart_threshold = MULTIPART_THRESHOLD, 
                                        max_concurrency = MAX_CONCURRENCY,
                                        use_threads = USE_THREADS,
                                        num_download_attempts = NUM_DOWNLOAD_ATTEMPTS)}

            if callable(callback):
                params['Callback'] = callback

            s3.upload_file(**params)

            return f's3://{bucket}/{key}'

        except botocore.exceptions.ClientError as error:            
            raise Exception(f"Unable to upload file: {file_name}")    
    
    def upload_files(files, pbar):        
        update = getattr(pbar, 'update', None)
        update = update if callable(update) else lambda x: None

        futures = {}            
        with ThreadPoolExecutor() as executor: 
            for path in files:                
                if os.path.isfile(path):                         
                    dirname = os.path.dirname(path) + '/'
                    futures[executor.submit(upload_file, bucket, prefix, path, dirname, update)] = path                                                                      
                        
                elif os.path.isdir(path):   
                    path = path[:-1] if path[-1] == '/' else path  
                    dirname = os.path.dirname(path) + '/'  
                    for (root,dirs,files) in os.walk(path, topdown=True):
                        for file in files:                                                    
                            file_path = os.path.join(root,file)                                                    
                            futures[executor.submit(upload_file, bucket, prefix, file_path, dirname, update)] = file_path                            
                else:
                    raise Exception('File not found or not supported')
            
            pending_files = []
            files_sent = []
            for future in as_completed(futures):
                path = futures[future]
                try: 
                    result = future.result()                    
                except Exception as error:                                
                    pending_files.append(path) 
                    print(error)                   
                else:      
                    files_sent.append(result)   
        
        return pending_files, files_sent     

    if show_progress:
        pbar = tqdm(total=get_total_size(files), unit='B', unit_scale=True, desc='Uploading')
    else:
        pbar = None

    pending_files, all_files_sent = upload_files(files, pbar)

    while len(pending_files)>0:            
        pending_files, files_sent = upload_files(pending_files, pbar)
        all_files_sent.extend(files_sent)

    if callable(getattr(pbar,'close',None)):
        pbar.close()

    return all_files_sent[0] if len(all_files_sent) == 1 else None

def read_csv(s3_path: str, compression=None, session = default_session)->pd.core.frame.DataFrame:  
    '''
    Reads a CSV file from a S3 path
    
    Args:
        s3_path (str): S3 path of the file to read
        
    Returns:
        pandas dataframe
    '''      
    s3 = session.resource('s3')    
    
    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    obj = s3.Object(bucket, key)
    f = BytesIO(obj.get()['Body'].read())    

    return pd.read_csv(f, compression=compression)

def read_pkl(s3_path: str, session = default_session):  
    '''
    Reads a PKL file from a S3 path
    
    Args:
        s3_path (str): S3 path of the file to read
        
    Returns:
        pandas dataframe
    '''      
    s3 = session.resource('s3')    
    
    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    obj = s3.Object(bucket, key)
    f = BytesIO(obj.get()['Body'].read())    

    extension = key.split('/')[-1].split('.')[-1]
    if extension == 'tar' or extension == 'gz':        
        with tarfile.open(fileobj=f) as tar:
            return pickle.load(tar.extractfile(tar.getmembers()[0]))
    else:        
        return pickle.load(f)

def read_json(s3_path: str, session = default_session)->dict:  
    '''
    Reads a JSON file from a S3 path
    
    Args:
        s3_path (str): S3 path of the file to read
        
    Returns:
        json file as dict
    '''   
    s3 = session.resource('s3')    
    
    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    obj = s3.Object(bucket, key)
    
    return json.loads(obj.get()['Body'].read())

def read_jsonl(s3_path: str, session = default_session)->List[dict]:  
    '''
    Reads a JSONL file from a S3 path
    
    Args:
        s3_path (str): S3 path of the file to read
        
    Returns:
        json file as dict
    '''   
    s3 = session.resource('s3')    
    
    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    obj = s3.Object(bucket, key)
    
    return [json.loads(jline) for jline in obj.get()['Body'].read().splitlines()]
    
def make_dirs(local_path: str):
    dirname = os.path.dirname(local_path)
    if len(dirname)>0 and not os.path.exists(dirname):
        os.makedirs(dirname)
        
def create_tar_gz(files: Union[str, List[str]], tar_file_name: str, )->str:
    '''
    Creates a .tar.gz (aka .tgz) file with the files or direcotires especified
    
    Args:
        tar_file_name (str): file name for the .tar.gz file to be created
        files (list): list of files or directories to include
        
    Returns:
        file name created
    '''     

    files = [files] if isinstance(files,str) else files if isinstance(files, list) else None

    if files == None:
        raise Exception(f"You have to specify the file or files you want to add to the .tar.gz file.")    

    make_dirs(tar_file_name)

    with tarfile.open(tar_file_name, 'w:gz') as tar:
        for path in files:
            dirname = os.path.dirname(path)
            tar.add(path, arcname=path.replace(dirname,''))

    return tar_file_name

def create_zip(files: Union[str, List[str]], zip_file_name: str, )->str:
    '''
    Creates a zip file (aka .zip) file with the files or direcotires especified
    
    Args:
        zip_file_name (str): file name for the .tar.gz file to be created
        files (list): list of files or directories to include
        
    Returns:
        file name created
    '''     

    files = [files] if isinstance(files,str) else files if isinstance(files, list) else None

    if files == None:
        raise Exception(f"You have to specify the file or files you want to add to the .tar.gz file.")    

    make_dirs(zip_file_name)

    with zipfile.ZipFile(zip_file_name, 'w') as zip:
        for path in files:
            dirname = os.path.dirname(path)
            
            if os.path.isdir(path):                
                for folderName, subfolders, filenames in os.walk(path):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)
                        zip.write(filePath, filePath.replace(dirname,''))
                
            elif os.path.isfile(path):                
                zip.write(path, path.replace(dirname,''))
                
            else:
                print(f'ERROR: unable to add file: {path}')
            

    return zip_file_name

            
def list_s3(s3_path: str, session = default_session)->List[dict]:
    '''
    List objects of a given S3 path
    
    Args:
        s3_path (str): S3 path
        
    Returns:
        list of objects
    '''   

    path_parts = s3_path.replace('s3://','').split('/')
    bucket = path_parts.pop(0)
    key = '/'.join(path_parts)

    s3 = session.client('s3') 
    
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(
        Bucket=bucket,
        Prefix=key)

    return [f"{bucket}/{object['Key']}" for page in page_iterator if 'Contents' in page for object in page['Contents']]

def get_job_logs(log_group_name: str, log_stream_name_prefix: str, session = default_session)->str:
    import textwrap

    prefix = '    '
    preferred_width = 160
    wrapper = textwrap.TextWrapper(
        initial_indent=prefix, 
        width=preferred_width,
        subsequent_indent=' '*len(prefix))

    logs = session.client('logs')

    try:
        log_streams_response = logs.describe_log_streams(
            logGroupName = log_group_name,
            logStreamNamePrefix = log_stream_name_prefix)    

        if 'logStreams' in log_streams_response and len(log_streams_response['logStreams'])>0:
            for log_stream in log_streams_response['logStreams']:
                log_stream_name = log_stream['logStreamName']

                print(f'{log_stream_name}:')

                logs_response = logs.get_log_events(
                    logGroupName = log_group_name,
                    logStreamName = log_stream_name)

                if 'events' in logs_response:
                    for event in logs_response['events']:
                        print(wrapper.fill(event['message']))
    
    except botocore.exceptions.ClientError as error: 
        print(error)
        raise Exception('Unable to read logs')

def get_processing_job_logs(job_name: str, session = default_session)->str:
    get_job_logs('/aws/sagemaker/ProcessingJobs', job_name, session = session)  

def get_trainin_job_logs(job_name: str, session = default_session)->str:
    get_job_logs('/aws/sagemaker/TrainingJobs', job_name, session = session)  

def get_endpoint_logs(endpoint_name: str, session = default_session)->str:
    sm = session.client('sagemaker')

    response = sm.describe_endpoint(EndpointName = endpoint_name)
    if 'ProductionVariants' in response:
        for variant in response['ProductionVariants']:
            get_job_logs(f'/aws/sagemaker/Endpoints/{endpoint_name}', variant['VariantName'], session=session) 

def get_model_monitor_container_uri(region):
    container_uri_format = '{0}.dkr.ecr.{1}.amazonaws.com/sagemaker-model-monitor-analyzer'
    
    regions_to_accounts = {
        'eu-north-1': '895015795356',
        'me-south-1': '607024016150',
        'ap-south-1': '126357580389',
        'us-east-2': '680080141114',
        'us-east-2': '777275614652',
        'eu-west-1': '468650794304',
        'eu-central-1': '048819808253',
        'sa-east-1': '539772159869',
        'ap-east-1': '001633400207',
        'us-east-1': '156813124566',
        'ap-northeast-2': '709848358524',
        'eu-west-2': '749857270468',
        'ap-northeast-1': '574779866223',
        'us-west-2': '159807026194',
        'us-west-1': '890145073186',
        'ap-southeast-1': '245545462676',
        'ap-southeast-2': '563025443158',
        'ca-central-1': '536280801234'
    }
    
    container_uri = container_uri_format.format(regions_to_accounts[region], region)
    return container_uri

def _get_file_name(url):
    a = urlparse(url)
    return os.path.basename(a.path)

def run_model_monitor_job_processor(region: str, instance_type: str, role: str, data_capture_path: str, statistics_path: str, 
                                    constraints_path: str, reports_path: str, instance_count=1, preprocessor_path=None, postprocessor_path=None, publish_cloudwatch_metrics='Disabled'):
    
    data_capture_sub_path = data_capture_path[data_capture_path.rfind('datacapture/') :]
    data_capture_sub_path = data_capture_sub_path[data_capture_sub_path.find('/') + 1 :]
    processing_output_paths = reports_path + '/' + data_capture_sub_path
    
    input_1 = ProcessingInput(input_name='input_1',
                          source=data_capture_path,
                          destination='/opt/ml/processing/input/endpoint/' + data_capture_sub_path,
                          s3_data_type='S3Prefix',
                          s3_input_mode='File')

    baseline = ProcessingInput(input_name='baseline',
                               source=statistics_path,
                               destination='/opt/ml/processing/baseline/stats',
                               s3_data_type='S3Prefix',
                               s3_input_mode='File')

    constraints = ProcessingInput(input_name='constraints',
                                  source=constraints_path,
                                  destination='/opt/ml/processing/baseline/constraints',
                                  s3_data_type='S3Prefix',
                                  s3_input_mode='File')

    outputs = ProcessingOutput(output_name='result',
                               source='/opt/ml/processing/output',
                               destination=processing_output_paths,
                               s3_upload_mode='Continuous')

    env = {'baseline_constraints': '/opt/ml/processing/baseline/constraints/' + _get_file_name(constraints_path),
           'baseline_statistics': '/opt/ml/processing/baseline/stats/' + _get_file_name(statistics_path),
           'dataset_format': '{"sagemakerCaptureJson":{"captureIndexNames":["endpointInput","endpointOutput"]}}',
           'dataset_source': '/opt/ml/processing/input/endpoint',
           'output_path': '/opt/ml/processing/output',
           'publish_cloudwatch_metrics': publish_cloudwatch_metrics }
    
    inputs=[input_1, baseline, constraints]
    
    if postprocessor_path:
        env['post_analytics_processor_script'] = '/opt/ml/processing/code/postprocessing/' + _get_file_name(postprocessor_path)
        
        post_processor_script = ProcessingInput(input_name='post_processor_script',
                                                source=postprocessor_path,
                                                destination='/opt/ml/processing/code/postprocessing',
                                                s3_data_type='S3Prefix',
                                                s3_input_mode='File')
        inputs.append(post_processor_script)

    if preprocessor_path:
        env['record_preprocessor_script'] = '/opt/ml/processing/code/preprocessing/' + _get_file_name(preprocessor_path)
         
        pre_processor_script = ProcessingInput(input_name='pre_processor_script',
                                               source=preprocessor_path,
                                               destination='/opt/ml/processing/code/preprocessing',
                                               s3_data_type='S3Prefix',
                                               s3_input_mode='File')
        
        inputs.append(pre_processor_script) 
    
    processor = Processor(image_uri = get_model_monitor_container_uri(region),
                          instance_count = instance_count,
                          instance_type = instance_type,
                          role=role,
                          env = env)

    return processor.run(inputs=inputs, outputs=[outputs])