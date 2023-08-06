MYSQL_PASSWORD=$1

while [[ $(mysql -h 34.89.189.11 -u github_actions -p$MYSQL_PASSWORD --skip-column-names -s -r -e "USE pypi_packages; SELECT is_published FROM alvin_integration ORDER BY id DESC LIMIT 1;") -ne 1 ]];
do
    semantic_version=$(mysql -h 34.89.189.11 -u github_actions -p$MYSQL_PASSWORD --skip-column-names -s -r -e "USE pypi_packages; SELECT semantic_version FROM alvin_integration ORDER BY id DESC LIMIT 1;")
    sleep 5
done

# This can be 0.1.0 or 0.1.0-rc.0
semantic_version=$(mysql -h 34.89.189.11 -u github_actions -p$MYSQL_PASSWORD --skip-column-names -s -r -e "USE pypi_packages; SELECT semantic_version FROM alvin_integration ORDER BY id DESC LIMIT 1;")

base_version=${semantic_version%%-*} 

semantic-release changelog > tmp.changes.md

sed -i -e '/^__base_version__/s/=.*$/="'"$base_version"'"/' setup.py

export release_candidate_version=$(semantic-release print-version --prerelease --define=prerelease_tag=rc)
export release_candidate_base_version=$(semantic-release print-version)

sed -i -e '/^__version__/s/=.*$/="'"$release_candidate_version"'"/' setup.py
sed -i -e '/^__base_version__/s/=.*$/="'"$release_candidate_base_version"'"/' setup.py
# semantic-release version --define=commit_subject="Upgrade integration to version $release_candidate_version"

CHANGES=$(awk '{printf "%s\\n", $0}' tmp.changes.md)

rm tmp.changes.md

awk 'NR==7{print "'"## [$release_candidate_version] --- $(date +%F)\n"'"}1' CHANGELOG.md > CHANGELOG.tmp.md

rm CHANGELOG.md && mv CHANGELOG.tmp.md CHANGELOG.md

awk 'NR==8{print "'"\n $CHANGES \n"'"}1' CHANGELOG.md > CHANGELOG.tmp.md

rm CHANGELOG.md && mv CHANGELOG.tmp.md CHANGELOG.md

mysql -h 34.89.189.11 -u github_actions -p$MYSQL_PASSWORD --skip-column-names -s -r -e "USE pypi_packages; INSERT INTO alvin_integration (semantic_version, is_published) VALUES('$release_candidate_version', false);"

echo "$release_candidate_version"

