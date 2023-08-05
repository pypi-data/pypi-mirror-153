import os
import tempfile

from rich.console import Console

console = Console()


class ModelRepository:
    def __init__(self, url, branch=None, hash=None, access_token=None, check=False):
        self.url = url
        self.branch = branch if branch is not None else "main"
        self.hash = hash
        self.access_token = access_token

        if check:
            self._check()

    def _check(self):
        class Progress(RemoteProgress):
            def update(self, op_code, cur_count, max_count=None, message=""):
                print(f"Git clone: {self._cur_line}")

        with tempfile.TemporaryDirectory() as dir_name:
            try:
                url = furl(self.url)
                url.username = self.access_token
                url.password = "x-oauth-basic"
                repo = Repo.clone_from(
                    url.tostr(),
                    dir_name,
                    branch=self.branch,
                    depth=1,
                    single_branch=True,
                )
            except git.exc.GitError as e:
                message = f"Unable to clone repository at '{self.url}'"
                console.print(f":poop: {message}", style="red")
                raise ValueError(message)

            try:
                if self.hash is None:
                    self.hash = repo.head.commit.hexsha

                repo.commit(self.hash)
            except git.exc.GitError as e:
                message = f"Commit '{self.hash}' does not exist."
                console.print(f":poop: {message}", style="red")
                raise ValueError(message)

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n      url={self.url}"
        res += f"\n      branch={self.branch}"
        res += "\n    )"
        return res


class ModelFile:
    def __init__(self, name, url, upload=False, credentials=None, check=False):
        self.name = name
        self.url = url
        self.upload = upload
        self.credentials = credentials

        if check:
            self._check()

    def _check(self):
        if self.upload and not os.path.exists(self.url):
            message = f"Path '{self.url}' does not exist."
            console.print(f":poop: {message}", style="red")
            raise ValueError(message)

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n      name={self.name}"
        res += f"\n      url={self.url}"
        res += f"\n      upload={self.upload}"
        res += f"\n    )"
        return res


class Model:
    """
    Provides model related functionality.

    It should be created through the :class:`efemarai.project.Project.create_model` method.

    Example:

    .. code-block:: python
        :emphasize-lines: 2

        import efemarai as ef
        ef.Session().project("Name").create_model(...)
    """

    @staticmethod
    def create(project, name, description, version, repository, files, check=False):
        """
        Creates a model.

        You should use :func:`project.create_model` instead.
        """
        if name is None:
            raise ValueError("Missing model name")

        if repository is None:
            raise ValueError("Missing model repository")

        if files is None:
            files = []

        if not isinstance(repository, ModelRepository):
            repository = ModelRepository(**repository, check=check)

        files = [
            ModelFile(**f, check=check) if not isinstance(f, ModelFile) else f
            for f in files
        ]

        session = project._session
        response = session._put(
            f"api/model/undefined/{project.id}",
            json={
                "name": name,
                "description": description,
                "version": version,
                "repository": {
                    "url": repository.url,
                    "branch": repository.branch,
                    "hash": repository.hash,
                    "access_token": repository.access_token,
                },
                "files": [
                    {
                        "name": f.name,
                        "url": f.url,
                        "upload": f.upload,
                        "credentials": f.credentials,
                    }
                    for f in files
                ],
            },
        )
        model_id = response["id"]

        for f in files:
            if f.upload:
                session._upload(f.url, f"api/model/{model_id}/upload")

        return Model(project, model_id, name, description, version, repository, files)

    def __init__(self, project, id, name, description, version, repository, files):
        self.project = project
        self.id = id
        self.name = name
        self.description = description
        self.version = version
        self.repository = repository
        self.files = files

    def __repr__(self):
        res = f"{self.__module__}.{self.__class__.__name__}("
        res += f"\n  id={self.id}"
        res += f"\n  name={self.name}"
        res += f"\n  description={self.description}"
        res += f"\n  version={self.version}"
        res += f"\n  repository={self.repository}"
        res += f"\n  files={self.files}"
        res += f"\n)"
        return res

    def delete(self, delete_dependants=False):
        """
        Deletes the model.

        You cannot delete an object that is used in a stress test or a baseline
        (delete those first). Deletion cannot be undone.
        """
        self.project._session._delete(
            f"api/model/{self.id}/{self.project.id}/{delete_dependants}"
        )
