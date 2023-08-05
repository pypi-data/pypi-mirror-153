# Zephyr Scale API - Automation Results Publisher


## Overview
The tool provides an opportunity to update test cases status and publish automation test results into Zephyr Scale Cloud.  
Detailed Automation API requests and properties can be found here: [Zephyr Scale API](https://support.smartbear.com/zephyr-scale-cloud/api-docs/#tag/Automations)    


## Usage of the tool in the project

**Install zephyr-results-publisher library**

```
pip install zephyr-results-publisher
```

**Use the library**

```
from zephyr_results_publisher import publisher
```

**Set environment variable Zephyr Scale API_KEY:**  
How to generate API KEY: [Generating API Access Tokens](https://support.smartbear.com/zephyr-scale-cloud/docs/rest-api/generating-api-access-tokens.html)  

For UNIX like platforms:
```
export API_KEY=XXXXXXXXX
```

For Windows platforms:
```
set API_KEY=XXXXXXXXX
```

**To publish automation results into Zephyr Test Cycle root folder**

```
# Key name of the Jira project  
project_key = <PROJECT_KEY>

# Absolute path to the report file. E.g. "/Users/user/Project/report/cucumber.json"  
source_report_file = <REPORT_FILE_PATH>
    
# Report format. Possible values: "cucumber", "junit", "behave", "custom"  
report_format = "cucumber"
    
# Automatically create test cases if they are absent in Zephyr Scale. Possible values: true, false  
auto_create_test_cases = "true"    

# Execute
publisher.publish(project_key, source_report_file, report_format, auto_create_test_cases)
```

**To publish automation results into a specific Zephyr Test Cycle folder and customize Test Cycle properties**

```
# Key name of the Jira project  
project_key = <PROJECT_KEY>

# Absolute path to the report file. E.g. "/Users/user/Project/report/cucumber.json"  
source_report_file = <REPORT_FILE_PATH>
    
# Report format. Possible values: "cucumber", "junit", "behave", "custom".  
report_format = "cucumber"
    
# Automatically create test cases if they are absent in Zephyr Scale. Possible values: "true", "false". Default: "true"   
auto_create_test_cases = "true"    

# Customized test cycle name. Default: "Automated Build"  
test_cycle_name = "Automated Build"

# Set test cycle folder to publish the results. Default: "All test cycles"  
# IMPORTANT: the folder should be already created manually in Zephyr Scale "Test Cycles"  
test_cycle_folder_name = "All test cycles"
    
# Customized test cycle description. Default: ""  
test_cycle_description = "Test Cycle description"

# Set project version. Default: 1  
test_cycle_jira_project_version = 1

# Set test cycle custom fields. E.g {"Sprint": 23}. Default: {}  
test_cycle_custom_fields = {}

publisher.publish_customized_test_cycle(project_key, 
                              source_report_file, 
                              report_format, 
                              auto_create_test_cases
                              test_cycle_name,
                              test_cycle_folder_name,
                              test_cycle_description,
                              test_cycle_jira_project_version,
                              test_cycle_custom_fields)
```

**IMPORTANT:**
Publisher tool should be executed after the test report is fully generated.  
The best solution would be to create a function in one of the existing *.py files in the test project with 
```@atexit.register``` annotation. E.g.:

To publish results into Test Cycle root folder use function:

```
@atexit.register
def publish_report():  
    if os.environ.get("API_KEY") is not None:
        project_key = "PROJECT_KEY"  
        source_report_file = "/Users/user/Project/report/cucumber.json"  
        report_format = "behave"   
        auto_create_test_cases = "true"  
        publisher.publish(project_key, source_report_file, report_format, auto_create_test_cases)
```

or to publish automation results into a specific Zephyr Test Cycle folder and customize Test Cycle properties:

```
@atexit.register
def publish_report():
    if os.environ.get("API_KEY") is not None:
        project_key = "PROJECT_KEY"
        source_report_file = "report/behave-report.json"
        report_format = "behave"
        auto_create_test_cases = "true"
        test_cycle_name = "Test Cycle Description"
        test_cycle_folder_name = "Already created folder name"
        test_cycle_description = "Test Cycle description"
        test_cycle_jira_project_version = 1
        test_cycle_custom_fields = {}
        publisher.publish_customized_test_cycle(project_key,
                                                source_report_file,
                                                report_format,
                                                auto_create_test_cases,
                                                test_cycle_name,
                                                test_cycle_folder_name,
                                                test_cycle_description,
                                                test_cycle_jira_project_version,
                                                test_cycle_custom_fields)
```