"""A Python Pulumi program"""

import os
import pulumi
import pulumi_docker as docker

# create stack
stack = pulumi.get_stack()


# get configuration
config = pulumi.Config()
frontend_port = config.require_int("frontend_port")
backend_port = config.require_int("backend_port")
mongo_port = config.require_int("mongo_port")
mongo_host = config.require("mongo_host")
database = config.require("database")
node_enviroment = config.require("node_enviroment")
protocol = config.require("protocol")

# create image for backend
backend_image_name = "backend"
backend = docker.RemoteImage(
    backend_image_name,
    name="pulumi/tutorial-pulumi-fundamentals-backend:latest"

)

# create image for frontend
frontend_image_name = "frontend"
frontend = docker.RemoteImage(
    "fronend",
    name = "pulumi/tutorial-pulumi-fundamentals-frontend:latest"
)

# create image for mongo database
mongo_image = docker.RemoteImage(
    "mongo",
    name = "pulumi/tutorial-pulumi-fundamentals-database-local:latest"
)

# create a network 
network = docker.Network("network",name=f"services-{stack}")

# create a mongo container
mongo_container = docker.Container(
    "mongo_container",
    image=mongo_image.repo_digest,
    name=f"mongo-{stack}",
    ports=[docker.ContainerPortArgs(
    internal=mongo_port,
    external=mongo_port
    )],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
    name=network.name,
    aliases=["mongo"]
    )]
)

# create the backend conteiner
backend_container = docker.Container(
    "backend_container",
    name = f"backend-{stack}",
    image = backend.repo_digest,
    ports=[docker.ContainerPortArgs(
    internal=backend_port,
    external=backend_port)],
    envs=[
    f"DATABASE_HOST={mongo_host}",
    f"DATABASE_NAME={database}",
    f"NODE_ENV={node_enviroment}"
    ],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
    name=network.name
    )],
    opts=pulumi.ResourceOptions(depends_on=[mongo_container])
        
)

# create frontend container
frontend_container = docker.Container(
    "frontend_container",
    image=frontend.repo_digest,
    name=f"frontend-{stack}",
    ports=[docker.ContainerPortArgs(
    internal=frontend_port,
    external=frontend_port)],
    envs=[
    f"LISTEN_PORT={mongo_host}",
    f"HTTP_PROXY=backend-{stack}:{backend_port}",
    f"PROXY_PROTOCOL={protocol}"
    ],
    networks_advanced=[docker.ContainerNetworksAdvancedArgs(
    name=network.name
    )]
)