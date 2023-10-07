# build_files.sh
 echo "BUILD START"
 python3.11 -m pip install -r requirements.txt
 python3.11 backend/manage.py collectstatic --noinput --clear
 echo "BUILD END"