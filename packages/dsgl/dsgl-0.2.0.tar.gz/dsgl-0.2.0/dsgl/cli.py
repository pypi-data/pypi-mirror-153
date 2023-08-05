# cli.py
# CLI application for DSGL
import re
import inquirer
import boto3
import argparse


class text_color:
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    nc = "\033[0m"


def create_sagemaker_instance():
    """Creates a standardised notebook environment"""
    print(text_color.yellow + "DSGL: Create a new Sagemaker Notebook" + text_color.nc)

    # Prompt the user for specifics of instance
    # name - name of instance
    # size - instance size
    #

    client = boto3.client("sagemaker", region_name="eu-west-2")

    questions = [
        inquirer.Text("name", message="Name of Sagemaker Notebook"),
        inquirer.List(
            "size",
            message="What size instance do you need?",
            choices=["ml.m5d.large", "ml.m5d.xlarge", "ml.m5d.2xlarge"],
        ),
    ]

    # Stores the answers from prompt
    answers = inquirer.prompt(questions)

    # Create the instance
    response = client.create_notebook_instance(
        NotebookInstanceName=answers["name"] + "-DSGL",
        InstanceType=answers["size"],
        RoleArn="arn:aws:iam::601163517885:role/terraform-20220302122237146100000001",
        Tags=[
            {"Key": "dsgl", "Value": "true"},
        ],
        # LifecycleConfigName='string',   ## Add Lifecycle Config
        # DefaultCodeRepository='string', ## Add git repositories
        RootAccess="Enabled",
        PlatformIdentifier="notebook-al2-v1",
    )

    print(response)

    return response


def main():
    # Create Parser object
    parser = argparse.ArgumentParser()

    # Set arguments and parse
    parser.add_argument("create_notebook", help="Create a new Sagemaker notebook")
    args = parser.parse_args()

    if args.create_notebook:
        create_sagemaker_instance()

    return 0
