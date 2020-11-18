echo "${green}>>> Setting up & activating venv..${reset}"

# create virtual environment & activate it
python3 -m venv ./myvenv --without-pip --system-site-packages
source my_venv/bin/activate

echo "${green}>>> Setting up django..${reset}"
# install django & run server
python3 -m pip install Django
# python manage.py runserver