import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as iam from 'aws-cdk-lib/aws-iam';

export class WebAppStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        const synthesizer = new cdk.DefaultStackSynthesizer({
            fileAssetsBucketName: "investigacionbucket-unique-123",
            bucketPrefix: "",
            cloudFormationExecutionRole: "arn:aws:iam::903044982918:role/LabRole",
            deployRoleArn: "arn:aws:iam::903044982918:role/LabRole",
            fileAssetPublishingRoleArn: "arn:aws:iam::903044982918:role/LabRole",
            imageAssetPublishingRoleArn: "arn:aws:iam::903044982918:role/LabRole"
        });

        super(scope, id, { synthesizer, ...props });

        // Crear la VPC
        const vpc = ec2.Vpc.fromLookup(this, 'MyVpc', { vpcId: 'vpc-0c8be769008e26f28' });

        // Rol de la instancia EC2
        const instanceRole = iam.Role.fromRoleArn(this, 'InstanceRole', 'arn:aws:iam::903044982918:role/LabRole');

        // AMI de Ubuntu
        const ubuntuAmi = new ec2.LookupMachineImage({
            name: 'ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*',
            owners: ['099720109477']
        });

        // Crear la instancia EC2
        const instance = new ec2.Instance(this, 'WebTypescript', {
            instanceType: new ec2.InstanceType('t2.micro'),
            machineImage: ubuntuAmi,
            vpc: vpc,
            role: instanceRole
        });

        // Comandos de UserData
        const userDataCommands = [
            "apt-get update -y",
            "apt-get install -y git",
            "git clone https://github.com/Hamilton001-siu/websimple1.git",
            "git clone https://github.com/Hamilton001-siu/webplantilla1.git",
            "cd websimple1",
            "nohup python3 -m http.server 8080 &",
            "cd ../webplantilla1",
            "nohup python3 -m http.server 8081 &"
        ];

        userDataCommands.forEach(cmd => instance.userData.addCommands(cmd));

        // Permitir tráfico en los puertos 8080 y 8081
        instance.connections.allowFromAnyIpv4(ec2.Port.tcp(8080), 'Allow HTTP traffic on port 8080');
        instance.connections.allowFromAnyIpv4(ec2.Port.tcp(8081), 'Allow HTTP traffic on port 8081');
    }
}
