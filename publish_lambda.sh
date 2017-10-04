cd ${1}

cd lib/python2.7/site-packages/
zip -r ../../../${1}.zip .

cd ../../../
cd lib64/python2.7/site-packages/
zip -r ../../../${1}.zip .

cd ../../../
zip -u ${1}.zip *.py 

aws s3 cp ${1}.zip s3://${2}

aws lambda update-function-code \
  --function-name ${1} \
  --s3-bucket ${2} \
  --s3-key ${1}.zip \
  --publish
