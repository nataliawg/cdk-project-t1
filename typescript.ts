#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { WebAppStack } from '../lib/typescript-stack';

const app = new cdk.App();
new WebAppStack(app, 'WebAppStack', {
    env: {
        account: process.env.CDK_DEFAULT_ACCOUNT || '903044982918',
        region: process.env.CDK_DEFAULT_REGION || 'us-east-1'
    }
});

app.synth();
