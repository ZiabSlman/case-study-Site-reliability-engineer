# case-study-Site-reliability-engineer

This repository was created as part of a case study for site reliability engineer.

# Requirements

Required libraries can be found in requirements.txt file. 

# configure the script: 
In config.ini file, set the desired configuration.

[GitHub]

	token = GitHub token, can be generated per user [here](https://github.com/settings/tokens)
  
	repository = name of the repo, ex. RockstarLang/rockstar
  
	branch = branch, currently supported is main

[ElasticSearch]

	cloud_id = CLOUD_ID
  
	elastic_password = PASS***
  
  #target_index = index,  will be the index if specified, otherwise, it will be from the shape (name-of-repo-branchs-commits).
  
# Run the script: 
  
  Execute the command.
  
	python main.py 
