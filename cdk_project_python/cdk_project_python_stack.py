from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    DefaultStackSynthesizer,
)
from constructs import Construct


class CdkProjectPythonStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        synthesizer = DefaultStackSynthesizer(
            file_assets_bucket_name="qweqwieiwuieoqwuierp",
            bucket_prefix="",
            cloud_formation_execution_role="arn:aws:iam::321991600320:role/LabRole",
            deploy_role_arn="arn:aws:iam::321991600320:role/LabRole",
            file_asset_publishing_role_arn="arn:aws:iam::321991600320:role/LabRole",
            image_asset_publishing_role_arn="arn:aws:iam::321991600320:role/LabRole"
        )

        super().__init__(scope, id, synthesizer=synthesizer, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-06b8591c9d7980047")
        instance_role = iam.Role.from_role_arn(
            self, "Role", role_arn="arn:aws:iam::321991600320:role/LabRole"
        )

        ubuntu_ami = ec2.LookupMachineImage(
            name="ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*",
            owners=["099720109477"]
        )

        instance = ec2.Instance(
            self, "EC2Python",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ubuntu_ami,
            vpc=vpc,
            role=instance_role
        )

        user_data_commands = [
            "sudo apt-get update -y",
            "sudo apt-get install -y apache2 git",
            "sudo systemctl start apache2",
            "sudo systemctl enable apache2",

            "sudo echo 'Listen 8080' >> /etc/apache2/ports.conf",
            "sudo echo 'Listen 8081' >> /etc/apache2/ports.conf",

            "sudo git clone https://github.com/zamir5895/web-simple.git /var/www/web-simple",
            "sudo git clone https://github.com/nataliawg/web-plantilla.git /var/www/web-plantilla",

            "echo '<VirtualHost *:8080>' | sudo tee /etc/apache2/sites-available/web-simple.conf",
            "echo '    DocumentRoot /var/www/web-simple' | sudo tee -a /etc/apache2/sites-available/web-simple.conf",
            "echo '    ErrorLog ${APACHE_LOG_DIR}/error.log' | sudo tee -a /etc/apache2/sites-available/web-simple.conf",
            "echo '    CustomLog ${APACHE_LOG_DIR}/access.log combined' | sudo tee -a /etc/apache2/sites-available/web-simple.conf",
            "echo '</VirtualHost>' | sudo tee -a /etc/apache2/sites-available/web-simple.conf",

            "echo '<VirtualHost *:8081>' | sudo tee /etc/apache2/sites-available/web-plantilla.conf",
            "echo '    DocumentRoot /var/www/web-plantilla' | sudo tee -a /etc/apache2/sites-available/web-plantilla.conf",
            "echo '    ErrorLog ${APACHE_LOG_DIR}/error.log' | sudo tee -a /etc/apache2/sites-available/web-plantilla.conf",
            "echo '    CustomLog ${APACHE_LOG_DIR}/access.log combined' | sudo tee -a /etc/apache2/sites-available/web-plantilla.conf",
            "echo '</VirtualHost>' | sudo tee -a /etc/apache2/sites-available/web-plantilla.conf",

            "sudo a2ensite web-simple",
            "sudo a2ensite web-plantilla",
            "sudo systemctl restart apache2"
        ]

        instance.user_data.add_commands(*user_data_commands)

       	instance.connections.allow_from_any_ipv4(ec2.Port.tcp(8080), "abrir el puerto 8080")
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(8081), "abrir el puerto 8081")
