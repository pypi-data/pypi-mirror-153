# Renovo Solutions Private Lambda Micro REST API (`proxy`) Infrastructure Library

[![build](https://github.com/RenovoSolutions/cdk-library-renovo-microapi/actions/workflows/build.yml/badge.svg)](https://github.com/RenovoSolutions/cdk-library-renovo-microapi/workflows/build.yml)

This infrastructure construct library implements a private lambda backed REST API on AWS API Gateway using `proxy+`.

## Features

* Utilizes an internal Micro API project to provide an api via Lambda ([with `proxy+`](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html)) and API Gateway
* Configures the required VPC endpoint attachment automatically
* Configures logging for API requests
* Configures the private gateways policy to restrict access to the VPC endpoint
* Exports the private DNS name to be used in the app

## What this construct does not do

* Provide the VPC endpoint with private DNS enabled. The user utilizing this construct should create a single VPC endpoint with private DNS enabled and share it across all projects utilizing this consturct.

## Private API Gateway traffic flow using VPC Endpoint

API gateways are a managed service that lives outside of our own VPC. Therefore when creating a private gateway this means that in order to access it additional configurations need to occur. Specifically a VPC endpoint must exist for traffic to route to the API Gateway. In addition the Lambda service itself also lives outside our VPC. This can seem a bit complex given that most of our Micro API projects then return to the VPC to route traffic to the database. To help visualize what this looks like here is a diagram of this traffic flow when routing through the api gateway for Micro APIs:

![private api traffic flow](docs/private_api_traffic.png)

## The old setup, using public traffic flow

We used to deploy API gateways as public endpoints. For the sake of comparison here is what the old traffic flow would have looked like:

![public api traffic flow](docs/public_api_traffic.png)

## References

* [Creating a private API in Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html)
