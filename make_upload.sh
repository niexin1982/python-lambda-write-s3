rm upload.zip
rm -r upload/

mkdir upload
cp app/lambda_function.py upload/
pip install -r app/requirements.txt -t upload/
cd upload/
zip -r ../upload.zip --exclude=__pycache__/* .
cd ../

rm -r upload/
