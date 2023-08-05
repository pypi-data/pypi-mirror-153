<h1 align="center">{name-your-service}</h1>

<p align="center">project-description</p>

## Links

- [Github Repo](https://git.zoominfo.com/dozi/{name-your-service} "{name-your-service} Repo")

- [API](<API Link> "API")


## Prerequisites
Please run `pip install -r requirements_docker` in order to make sure that all needed libraries
are installed

## Available Commands

As this project has been built by the dsframework, 
it can run the following commands:

### `dsf-cli run-server`

Run a local sever (127.0.0.1:8080), encapsulating the pipeline. Can be either be used for
local testing by DSP, or for manual local testing.

### `dsf-cli generate documentation full/simple`

Create documentation of the entire project, including base classes inherited from dsframework
Please refer to the documentation for additional commands and abilities

### `dsf-cli cloud-eval`

Trigger cloud evaluation

### `dsf-cli evaluate input-csv-file batch-size`

Trigger local testing via a csv file

## Built With

- Python
- Docker
- Bash

## Future Updates

- [ ] Replace mock service
- [ ] Write proper evaluation
- [ ] Integrate with DSP
- [ ] Deploy to staging
- [ ] Deploy to production

## Author

**Developer - Name**

- [Email](mailto:yourname@zoominfo.com?subject=Hi "Hi!")


## 🤝 Support

Contributions, issues, and feature requests are welcome!
