# build_files.sh
 echo "BUILD START"
 python3.9 -m pip install -r requirements.txt
 python3.9 backend/manage.py runserver
 echo "BUILD END"