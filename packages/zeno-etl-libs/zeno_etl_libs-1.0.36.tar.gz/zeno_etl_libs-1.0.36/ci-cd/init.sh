#Please select following modules you want to build
#	1 ) 	glue-conn
#	2 ) 	glue-triggers
#	3 ) 	param-store
#	4 ) 	secrets
#	5 )		glue-jobs

buildModules="glue-jobs"
echo "in init.sh"
environment=$1
for module in $(echo $buildModules | sed "s/,/ /g")
do
    find $CODEBUILD_SRC_DIR/$module/ -iname build.sh -type f -exec sh {} "$environment" \;
done
