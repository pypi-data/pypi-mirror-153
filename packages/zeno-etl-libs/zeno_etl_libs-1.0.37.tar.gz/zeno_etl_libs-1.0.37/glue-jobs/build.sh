#Build commands for merge glue job
set -ue

module_name="glue-jobs"
env=$1
echo "========================[ Build: $module_name ]========================="
src_base_path=$(find $CODEBUILD_SRC_DIR/$module_name/  -iname src -type d)
ml_src_base_path=$(find $CODEBUILD_SRC_DIR/sagemaker-jobs/  -iname src -type d)
templates_base_path=$(find $CODEBUILD_SRC_DIR/$module_name/  -iname templates -type d)
artifacts_base_path="s3://aws-$env-glue-assets-921939243643-ap-south-1/artifact/$module_name"
ml_artifact_base_path="s3://aws-$env-glue-assets-921939243643-ap-south-1/artifact/sagemaker-jobs"

# Packing with dependencies
yum install gcc-c++ python3-devel unixODBC-devel -y
ln -s /usr/libexec/gcc/x86_64-amazon-linux/7.2.1/cc1plus /usr/bin/
python3.6 -m pip install --upgrade pip
# creation of folder for extra dependencies
mkdir $src_base_path/etl_libs/
mkdir $src_base_path/etl_libs/google/
mkdir $src_base_path/zeno_etl_libs/

echo "========================[ Packaging etl libs ]========================="
cp $CODEBUILD_SRC_DIR/etl_libs/setup.py $src_base_path/etl_libs/setup.py
cp -R $CODEBUILD_SRC_DIR/extra_dependency/google/* $src_base_path/etl_libs/google
python3.6 -m pip install -r $CODEBUILD_SRC_DIR/requirements.txt --target $src_base_path/etl_libs/
cd $src_base_path/etl_libs/
python3.6 setup.py bdist_egg
cp ./dist/etl_pkg-0.0.6-py3.6.egg $src_base_path/
cd ..
rm -rf $src_base_path/etl_libs/

echo "========================[ Packaging Zeno etl libs ]========================="
mkdir $src_base_path/zeno_etl_libs/zeno_etl_libs
echo "copying files from zeno_etl_libs"
cp -R $CODEBUILD_SRC_DIR/zeno_etl_libs/* $src_base_path/zeno_etl_libs/zeno_etl_libs
cp $CODEBUILD_SRC_DIR/zeno_etl_libs/setup.py $src_base_path/zeno_etl_libs
cd $src_base_path/zeno_etl_libs/
python3.6 setup.py bdist_egg
cp ./dist/zeno_etl_pkg-0.0.6-py3.6.egg $src_base_path/
cd ..
rm -rf $src_base_path/zeno_etl_libs/

echo "========================[ Sagemaker Deployment ]========================="
#aws codebuild delete-project --name create-sagemaker-container-$env-notebook-runner
#python $CODEBUILD_SRC_DIR/setup.py sdist bdist_wheel
#nohup twine upload dist/* --verbose -u kuldeepsingh -p bEmham-6sonke-forcex &
#pip install zeno-etl-libs
#pip install https://github.com/aws-samples/sagemaker-run-notebook/releases/download/v0.20.0/sagemaker_run_notebook-0.20.0.tar.gz
#cp $CODEBUILD_SRC_DIR/extra_dependency/Dockerfile /root/.pyenv/versions/3.9.5/lib/python3.9/site-packages/sagemaker_run_notebook/container
#nohup run-notebook create-container $env-notebook-runner --requirements $CODEBUILD_SRC_DIR/requirements-ml.txt --no-logs &

echo "========================[ Syncing artifacts ]========================="
# Upload templates to artifacts-bucket
echo "Syncing the artifacts"
aws s3 sync $templates_base_path/  $artifacts_base_path/templates/
aws s3 sync $src_base_path/ $artifacts_base_path/src/
aws s3 sync $ml_src_base_path/ $ml_artifact_base_path
echo "Build.sh completed"