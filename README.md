# API-access-Hadoop-github-repo-contributors-using-Beautiful-Soup
Built a tool using Beautiful Soup library in Python to extract the first 100 contributors response json from the API https://api.github.com/repos/apache/hadoop/contributors which contains hadoop github repo contributors’ urls endpoint.
This script then  extracts the number of repos for each of the contributor and his/her number of contributions. Post
that it access the commits endpoint for the repo apache/hadoop and print the difference between the timestamp of last 
commit and the (last-100)th commit.
