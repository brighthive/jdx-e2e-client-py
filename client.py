from __future__ import print_function
import argparse
import time
import openapi_client
import os
import sys
from openapi_client.rest import ApiException
from pprint import pprint


# Argument parsing stuff
parser = argparse.ArgumentParser(description='End to end test for JDX API.')
parser.add_argument(
    '--server',
    choices=['production'],
    help='Select the server you want to use (only production is enabled currently).',
    default='production'
)
parser.add_argument(
    '-d',
    '--directory-or-file',
    default='./files',
    help='Path to a directory or a single file that contains job description(s).'
)
parser.add_argument(
    '-f',
    '--framework',
    help='Provide a single UUID for a framework that you want to use. JDX API currently can handle multiple frameworks being selected but that is not supported in this E2E client.'
)
parser.add_argument(
    '-l',
    '--loop',
    action='store_true',
    help='If provided this will loop through all files in the directory forever.'
)

args = parser.parse_args()

urls = {
    'production': 'https://jdx-api.brighthive.net'
}

HOST = urls[args.server]


# Printing Utils
import functools
import json
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def print_response(resp):
    resp, status, headers = resp
    
    _formatted_print = lambda text: pprint(f'{text}')

    _formatted_print(f'Status: {status}')

    for key, value in headers.items():
        _formatted_print(f'{key}: {value}')

    _formatted_print(f'Response:')

    print(json.dumps(resp.to_dict(), indent=4, default=json_serial))


def pp(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        response = fn(*args, **kwargs)
    
        try:
            print_response(response)
        except:
            print('Failed to print request/response!')
            raise
        
        return response

    return wrapper


def print_x_empty_lines(count):
    for _ in range(count):
        print('\n')


# The main workhorse class
class ProcessThroughJDX():

    def __init__(self, host, given_file):
        self.given_file = given_file
        config = openapi_client.Configuration()
        config.host = host
        self.api_instance = openapi_client.DefaultApi(openapi_client.ApiClient(config))


    def go(self):
        self.health()
        print_x_empty_lines(1)

        self.upload_file()
        print_x_empty_lines(1)

        # self.preview()
        # print_x_empty_lines(1)

        # self.get_score()
        # print_x_empty_lines(1)
        
        self.upload_context() # Send all job context at once instead of partials
        print_x_empty_lines(1)

        self.framework_recommendations()
        print_x_empty_lines(1)
        
        self.framework_selections()
        print_x_empty_lines(1)

        self.match_table()
        print_x_empty_lines(1)

        self.user_actions()
        print_x_empty_lines(1)

        # self.get_score()
        # print_x_empty_lines(1)
        
        # self.upload_context() 
        # print_x_empty_lines(1)

        self.generate_file()
        print_x_empty_lines(1)


    @pp
    def health(self):
        print('HEALTH')
        try:
            resp_obj = self.api_instance.health_get_with_http_info()
            resp, status, headers = resp_obj
            
            assert(resp.api == 200)
            assert(status == 200)
        except ApiException as e:
            print("Exception when calling DefaultApi->health_get: %s\n" % e)
        
        return resp_obj


    @pp
    def upload_file(self):
        print('UPLOAD FILE')
        try:
            resp_obj = self.api_instance.upload_job_description_file_post_with_http_info(
                file=self.given_file
            )
            resp, status, headers = resp_obj

            self.pipeline_id = resp.pipeline_id
            assert(self.pipeline_id != None)        
            assert(status == 200)
        except ApiException as e:
            print("Exception when calling DefaultApi->upload_job_description_file_post: %s\n" % e)
    
        return resp_obj

    @pp
    def preview(self):
        request = openapi_client.Request(self.pipeline_id) # Request | Get preview of job description wth tagged matches. (optional)

        try:
            # Get preview of job description with tagged matches.
            resp_obj = self.api_instance.preview_post_with_http_info(request=request)
            resp, status, headers = resp_obj
        except ApiException as e:
            print("Exception when calling DefaultApi->preview_post: %s\n" % e)

        return resp_obj

    @pp
    def upload_context(self):
        print('UPLOAD CONTEXT')
        job_description_context_request = openapi_client.JobDescriptionContextRequest(
            pipeline_id = self.pipeline_id,
            employer_name = "BrightHive",
            employer_overview = "BrightHive is a data technology company. We work with data so you don't have to!",
            employer_email = "hiring@brighthive.io",
            employer_website = "https://brighthive.io",
            employer_address = "Chicago, IL",
            employer_phone = "1231231234",
            job_title = "Wordpress Developer",
            job_summary = "As a BrightHive wordpress developer you will be managing, extending, and building or Wordpress extensions.",
            primary_economic_activity = "Web Development", # this is for the position
            industry_code = "811192",
            occupation_code = "15-1134.00",
            job_location = "Rockford, IL",
            job_location_type = "This is an in-person position.",
            employment_unit = "Product Team",
            employer_identifier = "Wordpress-Developer-526a",
            assessment = "You will be required to complete the Wordpress Developer Associate Level 2 test.",
            employment_agreement = "Employee not eligible for overtime",
            job_term = "Regular",
            job_schedule = "Full-time",
            work_hours = "Flexible work hours (set your own schedule)",

            # credential requirements
            requirements = "You must have at least a Bachelors or relevant work experience.",
            application_location_requirement = "All Locations",
            citizenship_requirement = "US Citizen",
            physical_requirement = "No Physical Requirement",
            sensory_requirement = "No Sensory Requirements",
            security_clearance_requirement = "No Security Clearance",
            special_commitment = "No Special Commitments",
            salary_currency = "USD",
            salary_minimum = "20000",
            salary_maximum = "80000",
            salary_frequency = "Per Year",
            incentive_compensation = "No Incentive Compensation",
            job_benefits = [
                "Health Insurance",
                "Dental Insurance",
                "Vision Insurance",
                "Life Insurance",
                "PTO",
                "401(k)",
                "Workplace perks such as recreation activities, food and coffee"
            ],
            date_posted = "2019-08-01",
            valid_through = "2019-08-15",
            job_openings = "1"
        ) # JobDescriptionContextRequest | job description context (optional)

        try:
            # Provide job description context (e.g metadata) on the job description
            resp_obj = self.api_instance.upload_job_description_context_post_with_http_info(
                job_description_context_request=job_description_context_request
            )
            resp, status, headers = resp_obj
            print(resp.salary_currency)
        except ApiException as e:
            print("Exception when calling DefaultApi->upload_job_description_context_post: %s\n" % e)

        return resp_obj

    @pp
    def framework_recommendations(self):
        print('FRAMEWORK RECOMMENDATIONS')
        
        request = openapi_client.Request(self.pipeline_id)
        pprint(request)

        try:
            # Get framework recommendations based on the uploaded job descripton and context.
            resp_obj = self.api_instance.framework_recommendations_post_with_http_info(request=request)
            resp, status, headers = resp_obj

        except ApiException as e:
            print("Exception when calling DefaultApi->framework_recommendations_post: %s\n" % e)
            
        self.framework_selection = resp.framework_recommendations[0].framework_data.uuid

        return resp_obj

    @pp
    def framework_selections(self):
        print('FRAMEWORK SELECTIONS')

        framework_uuid = args.framework if args.framework else self.framework_selection
        chosen_framework = openapi_client.Framework(framework_uuid)
        frameworks = openapi_client.Frameworks([chosen_framework], None, None)
        
        framework_selection_request = openapi_client.FrameworkSelectionRequest(
            self.pipeline_id,
            frameworks
        ) # FrameworkSelectionRequest | framework selections (optional)

        try:
            # The user indicates what frameworks they selected
            resp_obj = self.api_instance.framework_selections_post_with_http_info(
                framework_selection_request=framework_selection_request
            )
            resp, status, headers = resp_obj
            
        except ApiException as e:
            print("Exception when calling DefaultApi->framework_selections_post: %s\n" % e)
    
        return resp_obj

    @pp
    def match_table(self):
        print('MATCH TABLE')
        match_table_request = openapi_client.MatchTableRequest(self.pipeline_id) # MatchTableRequest | Get framework-recommendations for a given Pipeline ID. (optional)

        try:
            # Get the match table associated with the provided `pipelineID`
            resp_obj = self.api_instance.match_table_post_with_http_info(match_table_request=match_table_request)
            resp, status, headers = resp_obj
            self.match_table = resp.match_table

        except ApiException as e:
            print("Exception when calling DefaultApi->match_table_post: %s\n" % e)

        return resp_obj


    def convert_match_table_to_user_actions(self):
        """ 
        This will deal with the match table results and follow a pattern
        to accept, reject, and replace matches in the table that are then
        converted into user actions.


        The pattern is as follows;
        If a competency has no matches then we issue
        a replace action and use the full text of the original competency.

        Accept and rejects occur based on if the counter is even or odd.
        The counter begins at 0 and increments by 1 for every competency
        which means the count is 1 for the first competency.

        If the counter is even we issue a reject.
        If the counter is odd we issue an accept.
        """
        match_table_list = self.match_table

        match_table_selections = []
        reject_accept_counter = 0

        for item in match_table_list:
            reject_accept_counter += 1

            if len(item.matches) == 0:
                # replace
                replace_action = openapi_client.MatchTableSelection(
                    item.substatement_id,
                    None,
                    openapi_client.Replace(
                        item.substatement
                    )
                )
                match_table_selections.append(replace_action)

            elif reject_accept_counter % 2 == 0:
                # reject
                reject_action = openapi_client.MatchTableSelection(
                    item.substatement_id
                )
                match_table_selections.append(reject_action)

            else:
                # accept
                accept_action = openapi_client.MatchTableSelection(
                    item.substatement_id,
                    openapi_client.Accept(
                        item.matches[0].recommendation_id
                    )
                )

                match_table_selections.append(accept_action)

        return match_table_selections


    @pp
    def user_actions(self):
        print('USER ACTIONS')

        match_table_selections = self.convert_match_table_to_user_actions()
        
        user_action_request = openapi_client.UserActionRequest(
            self.pipeline_id,
            match_table_selections
        ) # UserActionRequest | Contains a list of user responses (optional)

        try:
            # Provide the user responses as a list of user actions
            resp_obj = self.api_instance.user_actions_post_with_http_info(
                user_action_request=user_action_request
            )
            resp, status, headers = resp_obj

        except ApiException as e:
            print("Exception when calling DefaultApi->user_actions_post: %s\n" % e)
        
        return resp_obj


    @pp
    def get_score(self):
        print('GET SCORE')

        request = openapi_client.Request(
            self.pipeline_id
        ) # Request | Get score for a given Pipeline ID. (optional)

        try:
            # Provides a scored based on how much metadata you provide and the quality of that data.
            resp_obj = self.api_instance.get_score_post_with_http_info(
                request=request
            )
            resp, status, headers = resp_obj
            
        except ApiException as e:
            print("Exception when calling DefaultApi->get_score_post: %s\n" % e)
        
        return resp_obj


    @pp
    def generate_file(self):
        print('GENERATE FILE')
        request = openapi_client.Request(
            self.pipeline_id
        ) # Request | Generate JobSchema+ from a given pipeline_id (optional)

        try:
            # Generate JobSchema+
            resp_obj = self.api_instance.generate_job_schema_plus_post_with_http_info(
                request=request
            )
            resp, status, headers = resp_obj

        except ApiException as e:
            print("Exception when calling DefaultApi->generate_job_schema_plus_post: %s\n" % e)

        return resp_obj


# Runner utils
def is_not_a_valid_file_type(filename):
    accepted_types = ['.txt','.doc','.docx']

    file_type = os.path.splitext(filename)[1]
    return file_type not in accepted_types


def process_file(directory, filename):
    print(f'--File: {filename}')

    if is_not_a_valid_file_type(filename):
        print('Unsupported file type for "{filename}", skipping.')
        return

    full_path = f'{directory}/{filename}'

    fileProcessor = ProcessThroughJDX(HOST, full_path)
    fileProcessor.go()


def get_directory_and_file_list(directory_or_file):
    directory = None
    file_list = []

    if os.path.isdir(directory_or_file):
        directory = directory_or_file
        file_list = os.listdir(directory_or_file)

    elif os.path.isfile(directory_or_file):
        directory = '.'
        file_list = [directory_or_file]

    else:
        raise BaseException('Provided file is not a file or a directory.')

    return directory, file_list


# Runner
while True:
    directory, file_list = get_directory_and_file_list(
        args.directory_or_file)
    
    for filename in file_list:
        process_file(directory, filename)
        print_x_empty_lines(4)

    if args.loop is not True:
        sys.exit(0)
