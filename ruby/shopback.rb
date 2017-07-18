require 'github_api'
require 'aws-sdk'
#org_name = "shopback"
#repo_name="feature"
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

current_date=DateTime.parse(Time.now)
token = "xxxxx"
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
tag_names=dd.instances[0].tags[0]
if tag_names.key="Branch"
puts tag_names.value
commit_date=DateTime.parse(find_commit_date(org_name,repo_name,tag_names.value))
	diff = (current_date-commit_date).to_i
	if diff > 3
		to_delete= dd.instances[0].instance_id
	end
end
end


