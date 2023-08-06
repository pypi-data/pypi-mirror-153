
# Installs git-conventional-commits https://github.com/qoomon/git-conventional-commits
sudo npm install --global git-conventional-commits

#--
# Configures git to use a pre-receive client side hook to verify commit messages
# Needs to be setup only once upon cloning the repository since pre-receive server
# side hooks are only available on GitHub Enterprise servers 
# https://docs.github.com/en/enterprise-server@3.2/admin/policies/enforcing-policy-with-pre-receive-hooks/about-pre-receive-hooks
# --
git config core.hooksPath .git-hooks

