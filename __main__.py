"""A Python Pulumi program"""

import os
import pulumi
import pulumi_docker as docker

#create stack
stack = pulumi.get_stack()


#get configuration
config = pulumi.Config()
frontend_port = config.require_int("frontend_port")
backend_port = config.require_int("backend_port")
mongo_port = config.require_int("mongo_port")

#create image for backend
backend_image_name = "backend"
backend = docker.RemoteImage(
    backend_image_name,
    name="pulumi/tutorial-pulumi-fundamentals-backend:latest"

)

#create image for frontend
frontend_image_name = "frontend"
frontend = docker.RemoteImage(
    "fronend",
    name = "pulumi/tutorial-pulumi-fundamentals-frontend:latest"
)

#create image for mongo database
mongo_image = docker.RemoteImage(
    "mongo",
    name = "pulumi/tutorial-pulumi-fundamentals-database-local:latest"
)

