# From Local to server
scp public.tar.gz rr-dash@157.245.97.181:/home/rr-dash/htdocs/

# From server to local
rsync -avz msgwapi-api@3.110.216.237:/home/msgwapi-api/htdocs/api.msgwapi.com/sessions_last.zip ~/Downloads

rsync -avz -e "ssh -i /Users/username/.ssh/id_rsa" msgwapi-api@3.110.216.237:/home/msgwapi-api/htdocs/api.msgwapi.com/sessions_last.zip ~/Downloads