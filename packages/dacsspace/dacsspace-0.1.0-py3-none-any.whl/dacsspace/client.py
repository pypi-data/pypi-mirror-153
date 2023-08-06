from asnake.aspace import ASpace


class ASnakeConfigError(Exception):
    pass


class ArchivesSpaceClient:
    """Handles communication with ArchivesSpace."""

    def __init__(self, baseurl, username, password, repo_id):
        self.aspace = ASpace(
            baseurl=baseurl,
            username=username,
            password=password)
        self.repo = self.aspace.repositories(repo_id)
        if isinstance(self.repo, dict):
            raise ASnakeConfigError(
                "Error getting repository: {}".format(
                    self.repo.get("error")))

    def get_resources(self, published_only):
        """Returns data about resource records from AS.
        Args:
          published_only (boolean): Fetch only published records from AS
        Returns:
          resources (list): Full JSON of AS resource records
        """
        if published_only:
            search_query = "publish:true AND primary_type:resource"
        else:
            search_query = "primary_type:resource"
        for resource in self.repo.search.with_params(q=search_query):
            resource_json = resource.json()
            yield resource_json
