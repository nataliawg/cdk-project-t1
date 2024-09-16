#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_project_python.cdk_project_python_stack import CdkProjectPythonStack


app = cdk.App()
CdkProjectPythonStack(app, "CdkProjectPythonStack",


 env={
        'account': '321991600320',
        'region': 'us-east-1'
    }
    )

app.synth()
