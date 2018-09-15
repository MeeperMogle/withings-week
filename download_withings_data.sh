email=$1
userid=$2

if [[ "$email" == "" || "$userid" == "" ]];
then
	echo "Usage: $0 <email> <user_id>"
	exit 1
fi


echo "Enter password:"
read -s password;
wget --quiet --save-cookies cookies.txt --keep-session-cookies --post-data "email=$email&password=$password" --delete-after https://account.health.nokia.com/connectionwou/account_login
password=""

request_url="https://account.health.nokia.com/export/my_data?selecteduser=$userid"
wget --quiet --load-cookies cookies.txt "$request_url"

name_value=$(grep "input type" *my_data* | grep -o -E "(name=|value=)\"[^\"]+")
cleaned=$(echo "$name_value" | gawk '{gsub(/(name|value)=\"/, "")}; {print}')

rm *my_data*

constructed=""
for i in $name_value; do
	if [[ $i == *"name="* ]]; then
	  without_name_var=$(echo "$i" | gawk '{gsub(/(name|value)=\"/, "")}; {print}')
	  constructed="$constructed$without_name_var="
	elif [[ $i == *"value="* ]]; then
	  without_value_var=$(echo "$i" | gawk '{gsub(/(name|value)=\"/, "")}; {print}')
	  string="${without_value_var}"
	  strlen=${#string}
	  encoded=""

	  for (( pos=0 ; pos<strlen ; pos++ )); do
	  c=${string:$pos:1}
	  case "$c" in
		[-_.~a-zA-Z0-9] ) o="${c}" ;;
		* )               printf -v o '%%%02x' "'$c"
		esac
		encoded+="${o}"
	  done
	  constructed="$constructed$encoded&"
	fi
done

wget --quiet --load-cookies cookies.txt --post-data "$constructed" "$request_url"

./handle_withings_data.py
