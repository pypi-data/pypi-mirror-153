## Part 4 - Setting up a new batch project.{#quick_start4} 


### Step 1 - Setting up your environment

#### Install requirements:
After venv is ready, and the framework is installed, 
we can install batch related requirements:

    pip install -r batch_files/requirements.txt

#### Log in to gcloud
Make sure that you're logged in to gcloud, as many of the actions rely on that:

    gcloud auth application-default login

#### Update configuration file
Make sure that the project is configured adequately and that it suits your needs.
Please browse:

    <root_folder>/batch_files/batch_config.json

#### Monitor
Please note that any of the following stages can be monitored by visiting the GCP webpage and 
browsing through the different products (DataProc, Composer, Storage)

### Step 2 - Write your code

#### Creating new stages

3 Main stages are created upon project generation:
1. Get data - Used to fetch data (Initialy fetches an example .csv file and filters it a bit)
2. Run pipeline - Runs the project pipeline on the obtained data 
   (Make sure your pipeline runs properly).
   The current default stage assumes that the pipeline outputs a class with an out_text parameter.
3. Set data - Store the output of the 1st stage in a BigQuery table

For every new stage you wish to create, please add the appropriate library under
<root_dir>/batch_files/stages/<your_stage>.
Make sure that there's a main.py file. Please feel free to look at the existing
stages for reference.

#### Creating the workflow template (workflow.py)
A basic code for creating workflow template is provided upon project generation.
It includes the previous basic stages and assumes dependency among them. If you wish to 
add more stages, please edit the "create_stages" function

for example:
```
# stage new_stage - Let's assume that this stage relies on the "set_data" stage
  prerequisite_list = [self.project_name + '-stage_set_data']
  stage_new_stage_job = self.create_job("new_stage", prerequisite_list)
```

### Step 3 - Run your code

#### Setting up a cluster
The framework allows several actions regarding DataProc clusters:

    dsf-cli create-cluster # Create a DataProc cluster
    dsf-cli stop-cluster # Stop a running cluster
    dsf-cli start-cluster # Start a stopped cluster
    dsf-cli delete-cluster # Delete a cluster. (Used for configuration changes)

#### Uploading relevant files to appropriate buckets
In order to make sure that all needed files are present, please follow these steps:
1. Copy all relevant .jar files to batch_files/jars
2. Pack your project into a .whl file by running:


    python batch_files/setup.py bdist_wheel

3. Upload files to configured bucket by running:

    
    dsf-cli upload-batch-files <file_type> # options are: [all, jars, stages, whl]

#### Creating a workflow template
The framework allows several actions regarding DataProc Workflows:

    dsf-cli workflow-template <action> # Actions are [create, delete, instantiate]

Please use the "create" action and create your workflow template

#### Instantiating the workflow template - Dev mode
In order to go from template to an actual workflow and go through the stages, 
one should instantiate it. As a developer, you might want to do so immediately, 
rather than going through the DAG process. So, just run the command from the previous paragraph with 
the "instantiate" action. You should see your workflow running and the jobs being processed.

#### Instantiating the workflow template - DAG
The framework provides a basic DAG, which defaults to a daily activity and starts 
as paused, assuming that you're not under staging / production environments.

In order to create it, please run:

    dsf-cli create-dag

Please note that since this DAG starts as "paused", you would need to activate it first, either by
entering the Airflow GUI from the GCP Composer page, or any other way you can come up with...

# Good luck!
