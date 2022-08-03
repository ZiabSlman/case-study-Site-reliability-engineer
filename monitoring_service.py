import configparser
from github import Github
from elasticsearch import Elasticsearch
from github.PaginatedList import PaginatedList


class Monitor:

    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = self.get_configuration()
        self.commits = None
        self.elasticSearch = None
        self.client = None
        self.index = self.check_index()

    def get_configuration(self) -> configparser.ConfigParser:
        conf = configparser.ConfigParser()
        conf.read(self.config_file)
        return conf

    def check_index(self) -> str:
        try:
            self.index = self.config['ElasticSearch']['target_index']
        except:
            self.index = (self.config['GitHub']['repository']).replace("/", "-").lower() + '-' + \
                         self.config['GitHub']['branch'] + '-commits'
        return self.index

    def get_commits(self, token: str, repo: str, branch: str) -> PaginatedList:
        try:
            g = Github(token)
            repo_ = g.get_repo(repo)
            self.commits = repo_.get_commits(sha=branch)
        except Exception as e:
            print("Error have been encountered during connection to GitHub, " + str(e))
            exit(1)
        return self.commits

    def connect_elasticSearch(self, cloud_id: str, elastic_password: str) -> Elasticsearch:
        try:
            self.client = Elasticsearch(
                cloud_id=cloud_id,
                basic_auth=("elastic", elastic_password)
            )
        except Exception as e:
            print("Error have been encountered during connection to elasticSearch, " + str(e))
            exit(1)
        return self.client

    def index_doc(self, date: str, author: str, message: str):
        doc = {
            'author_name': author,
            'date': date,
            'commit_message': message
        }
        try:
            self.client.index(index=self.index, document=doc)
        except Exception as e:
            print("Error have been encountered during indexing, " + str(e))
            exit(1)

    def monitor(self):
        self.get_commits(self.config['GitHub']['token'],
                         self.config['GitHub']['repository'],
                         self.config['GitHub']['branch'])

        self.connect_elasticSearch(self.config['ElasticSearch']['cloud_id'],
                                   self.config['ElasticSearch']['elastic_password'])

        self.check_index()
        print("index: " + self.index)
        print("Document indexing started!")
        for commit in self.commits:
            if commit.commit is not None:
                self.index_doc(commit.commit.author.date,
                               commit.commit.author.name,
                               commit.commit.message)
        print("Document indexing finished successfully!")
