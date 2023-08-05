from efemarai.dataset import Dataset
from efemarai.domain import Domain
from efemarai.model import Model, ModelFile, ModelRepository
from efemarai.problem_type import ProblemType
from efemarai.stress_test import StressTest


class Project:
    """
    Provides project related functionality.
    A project is the main building block around which an ML model evaluation is performed.

    A project is an association of a set of ML models, datasets and domains.
    """

    @staticmethod
    def create(session, name, description, problem_type, exists_ok=False):
        """
        Creates a project.

        You should use `ef.Session().create_project(...)` instead.
        """
        if name is None or not ProblemType.has(problem_type):
            raise ValueError(
                f"Project name '{name}' is not specified or problem type '{problem_type}' not recognized."
            )

        existing_project = next((p for p in session.projects if p.name == name), None)
        if existing_project:
            if exists_ok:
                return existing_project
            else:
                raise ValueError(f"Project {name} already exists and exists_ok=False.")

        response = session._put(
            "api/project",
            json={
                "name": name,
                "description": description,
                "problem_type": problem_type,
            },
        )
        return Project(session, response["id"], name, description, problem_type)

    def __init__(self, session, id, name, description, problem_type):
        self._session = session
        self.id = id
        self.name = name  #: (str) Name of the project.
        self.description = description  #: (str) Description of the project.
        self.problem_type = ProblemType(
            problem_type
        )  #: (:class:`efemarai.problem_type.ProblemType`) Project problem type.

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n  id={self.id}"
        res += f"\n  name={self.name}"
        res += f"\n  description={self.description}"
        res += f"\n  problem_type={self.problem_type}"
        res += f"\n)"
        return res

    @property
    def models(self):
        """Returns a list of the models associated with the project."""

        return [
            Model(
                project=self,
                id=model["id"],
                name=model["name"],
                description=model.get("description"),
                version=model.get("version"),
                repository=ModelRepository(
                    url=model["repository"]["url"],
                    branch=model["repository"].get("branch"),
                    hash=model["repository"].get("hash"),
                ),
                files=[
                    ModelFile(name=f["name"], url=f["url"], upload=f["upload"])
                    for f in model["files"]
                ],
            )
            for model in self._session._get(f"api/models/{self.id}")
        ]

    def model(self, model) -> Model:
        """Returns the model specified by the name.

        Args:
            model (str): A model identifier. It can either be the name of the model or its id.

        Returns:
            :class:`efemarai.model.Model`: A model object or `None` if it doesn't exist.
        """

        model = next((m for m in self.models if m.name == model or m.id == model), None)
        return model

    def create_model(
        self,
        name,
        description=None,
        version=None,
        repository=None,
        files=None,
        exists_ok=False,
        **kwargs,
    ) -> Model:
        """Creates a model.

        Args:
            name (str): Name of the model.
            description (str, optional): Free text description.
            version (str, optional): Free text description.
            repository (dict): Model repository info. See `ef.model.ModelRepository`.
            files (list[dict]): Files needed to load the model e.g. weights or config
                files. See `ef.model.ModelFile`.
            exists_ok (bool, optional): If the current named model exist, should it be
                returned or an exception raised.

        Raises:
            ValueError: If the model exists and `exists_ok` is set to `False`.

        Returns:
            :class:`efemarai.model.Model`: The created model.
        """

        existing_model = next((m for m in self.models if m.name == name), None)
        if existing_model:
            if exists_ok:
                return existing_model
            else:
                raise ValueError(f"Model {name} already exists and exists_ok=False.")

        model = Model.create(self, name, description, version, repository, files)
        return model

    @property
    def datasets(self):
        """
        Returns a list of the datasets associated with the project.

        Returns:
            list[:class:`efemarai.dataset.Dataset`]: A list of available datasets.
        """

        return [
            Dataset(
                self,
                dataset["id"],
                dataset["name"],
                dataset["format"],
                dataset["stage"],
                dataset["data_url"],
                dataset.get("annotations_url"),
                dataset["loaded"],
                Dataset._parse_classes(dataset["classes"]),
            )
            for dataset in self._session._get(f"api/datasets/{self.id}")
        ]

    def dataset(self, dataset) -> Dataset:
        """
        Returns the dataset specified by the name or id.

        Args:
            dataset (str): A dataset identifier. It can either be the name of the dataset or its id.

        Returns:
            :class:`efemarai.dataset.Dataset`: A dataset object or `None` if it doesn't exist.
        """

        dataset = next(
            (d for d in self.datasets if d.name == dataset or d.id == dataset), None
        )
        return dataset

    def create_dataset(
        self,
        name,
        format,
        stage,
        data_url,
        annotations_url=None,
        credentials=None,
        upload=False,
        num_datapoints=None,
        mask_generation=None,
        exists_ok=False,
        min_asset_size=15,
        **kwargs,
    ) -> Dataset:
        """Creates a dataset.

        Args:
            name (str): A dataset name.
            format (str): A format of the dataset. Possible formats are specified under `ef.dataset.DatasetFormat`.
            state (str): Dataset stage - one of [`training`, `validation`, `test`].
            data_url (str): A url to fetch data. Can be local or remote.
            annotations_url (str, optional): A url that specifies the annotation file. Can be local or remote.
            credentials (str, optional): If the dataset if remote, Specify the `access token` or `{username}:{password}` to access.
            upload (bool, optional): Should the data be uploaded to Efemarai? This would make evaluation and testing much faster.
            num_datapoints (int, optional): Should a subset of the datapoints be loaded as a dataset? Specify the number of dataponts. Useful for quick testing. Use `None` to load all.
            mask_generation (str): What strategy should be used for mask generation.
            exists_ok (bool, optional): If the current named dataset exist, should it be returned or an exception raised.
            min_asset_size (int, optional): Assets with width and hight smaller than this will be ignored. Default value of 15.

        Raises:
            ValueError: If the dataset exists and `exists_ok` is set to `False`.

        Returns:
            :class:`efemarai.dataset.Dataset`: The created dataset.
        """

        existing_dataset = next((d for d in self.datasets if d.name == name), None)
        if existing_dataset:
            if exists_ok:
                return existing_dataset
            else:
                raise ValueError(f"Dataset {name} already exists and exists_ok=False.")

        dataset = Dataset.create(
            self,
            name,
            format,
            stage,
            data_url,
            annotations_url,
            credentials,
            upload,
            num_datapoints,
            mask_generation,
            min_asset_size,
        )

        return dataset

    @property
    def domains(self):
        """
        Returns a list of the domains associated with the project.

        Returns:
            list [:class:`efemarai.domain.Domain`]: A list of available domains.
        """

        return [
            Domain(
                self,
                domain["id"],
                domain["name"],
                domain["transformations"],
                domain["graph"],
            )
            for domain in self._session._get(f"api/domains/{self.id}")
        ]

    def domain(self, domain) -> Domain:
        """
        Returns the domain specified by the name or id.

        Args:
            domain (str): A domain identifier. It can either be the name of the domain or its id.

        Returns:
            :class:`efemarai.domain.Domain`: A domain object or `None` if it doesn't exist.
        """

        domain = next(
            (d for d in self.domains if d.name == domain or d.id == domain), None
        )
        return domain

    def create_domain(
        self, name, transformations, graph, exists_ok=False, **kwargs
    ) -> Domain:
        """
        Creates a domain. **The recommended strategy** is to use the UI to build up the domain visually.
        The domain then can be exported to a yaml configuration file for storage and loaded/reused through `ef.Session().load(...)`.

        Args:
            name (str): The name of the domain.
            transformations (dict): A dictionary of the transformations and their params.
            graph (dict): How the transformations are paired.
            exists_ok (bool, optional): If the current named domain exist, should it be returned or an exception raised.

        Raises:
            ValueError: If the domain exists and `exists_ok` is set to `False`.

        Returns:
            :class:`efemarai.domain.Domain`: The created domain.
        """

        existing_domain = next((d for d in self.domains if d.name == name), None)
        if existing_domain:
            if exists_ok:
                return existing_domain
            else:
                raise ValueError(f"Domain {name} already exists and exists_ok=False.")

        domain = Domain.create(self, name, transformations, graph)
        return domain

    @property
    def stress_tests(self):
        """
        Returns a list of the stress tests associated with the project.

        Returns:
            list [:class:`efemarai.stress_test.StressTest`]: A list of available stress tests.
        """

        return [
            StressTest(
                self,
                test["id"],
                test["name"],
                test["model"]["id"],
                test["domain"]["id"],
                test["dataset"]["id"],
                test["states"][-1]["name"],
                test["reports"],
            )
            for test in self._session._get(f"api/getRuns/{self.id}")["objects"]
        ]

    def stress_test(self, test) -> StressTest:
        """
        Returns the stress test specified by the name or id.

        Args:
            test (str): A stress test identifier. It can either be the name of the stress test or its id.

        Returns:
            :class:`efemarai.stress_test.StressTest`: A stress test object or `None` if it doesn't exist.
        """
        test = next(
            (t for t in self.stress_tests if t.name == test or t.id == test), None
        )
        return test

    def create_stress_test(
        self,
        name,
        model,
        domain,
        dataset,
        num_samples=25,
        num_runs=40,
        concurrent_runs=4,
        **kwargs,
    ) -> StressTest:
        """
        Creates a stress test.

        Args:
            model (str, :class:`efemarai.model.Model`): The model to stress test.
            domain (str, :class:`efemarai.domain.Domain`): The domain from which to generate samples.
            dataset (str, :class:`efemarai.dataset.Dataset`): The dataset with which to generate samples.
            num_samples (int, optional): Sample count to generate.
            num_runs (int, optional): Number of searches to run.
            concurrent_runs (int, optional): Number of concurrent searches.

        Returns:
            :class:`efemarai.stress_test.StressTest`: A stress test object.
        """

        test = StressTest.create(
            self,
            name,
            model,
            domain,
            dataset,
            num_samples,
            num_runs,
            concurrent_runs,
        )

        return test

    def delete(self, delete_dependants=False):
        """
        Deletes a project, including the domains, datasets, models, stress tests. Cannot be undone.
        """

        self._session._delete(f"api/project/{self.id}/{delete_dependants}")
