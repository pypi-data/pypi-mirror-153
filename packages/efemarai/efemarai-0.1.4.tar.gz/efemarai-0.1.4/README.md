A CLI and SDK for interacting with the [Efemarai ML testing platform](https://efemarai.com).

## Setup

Install with
```
pip install -U efemarai
```
then run
```
$ efemarai init
```
and following the instructions to connect your account.

## Example Usage

Working with projects:
```
import efemarai as ef

session = ef.Session()

# List all projects
for project in session.projects:
    print(project.name)

# Create a new project
project = session.create_project(
    name="Aircraft Detection",
    description="Exmample object detection project",
    problem_type="ObjectDetection",
)

# Load an existing one
project = session.project("Aircraft Detection")

# List project models
for model in project.models:
    print(model.name)
```

Working with stress tests:
```
# Create a new stress test
test = project.create_stress_test(
    name="Test via SDK",
    model=project.model("COCO YOLOR-P6"),
    domain=project.domain("Aircraft Domain"),
    dataset="Aircraft Detection - Train", # Just a name also works
)

# Load an existing stress test
test = project.stress_test("Test via SDK")

# Download dataset with discovered vulnerabilities
dataset_filepath = test.vulnerabilities_dataset()

# Check test run state
print(f"Running: {test.running} Failed: {test.failed} Finished: {test.finished}")
```
Models, domains and datasets can be easily created programatically, but
they require quite a few configuration paramaters to be provided. That's
why the most convenient way to create a project with multiple models, domains
and datasets is to put everything into a config file (see e.g.
`examples/aircraft_project.yaml`) and then just load it with:

```
result = ef.Session().load("examples/aircraft_project.yaml")

# access the created entities
project = result["project"]
models = result["models"]
domains = result["domains"]
datasets = result["datasets"]
```
