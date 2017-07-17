require 'github_api'
require 'aws-sdk'
ec2 = Aws::EC2::Client.new(
  region: 'us-east-1'
)
client = Aws::EC2::Client.new(region: 'us-east-1')
resp = client.describe_instances({
  filters: [
    {
      name: "tag:Branch",
      values: ["*"],
    },
    {
    	name: "instance-state-name",
    	values: ["running"],
    }
 ],

})

token = ""
GithubObject = Github.new do |config|
  config.oauth_token = token
  config.adapter     = :net_http
end

def find_commit_date(org_name,repo_name,branch)
  result = GithubObject.repos.commits.get org_name,repo_name,branch
  result.body.commit.author.date
end


resp.reservations.each do |dd|
 puts "**************"
 puts dd.instances[0].tags
end


def find_github_sha(org_name,repo_name)
  results = GithubObject.repos.commits.all org_name,repo_name
  results.body[0].commit.author.sha
end
