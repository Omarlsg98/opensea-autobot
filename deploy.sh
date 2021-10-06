environment=$1
case $environment in
 colab)
  installation_path="/content/opensea-autobot"
  driver_path="$installation_path/driver/chromedriver"

  config_path="$installation_path/config.py"
  sed -i "s|^INSTALLATION_DIR =.*$|INSTALLATION_DIR = $installation_path|g" $config_path
  sed -i "s|^DRIVER_PATH =.*$|DRIVER_PATH = $driver_path|g" $config_path
  sed -i "s|^chrome_arguments =.*$||g" $config_path
  sed -i "s|^# For colaboratory_env chrome_arguments =|chrome_arguments =|g" $config_path

  pip install -r /content/opensea-autobot/requirements.txt
  apt-get update
  apt install chromium-chromedriver
  cp /usr/lib/chromium-browser/chromedriver /usr/bin
  ln -fs /usr/lib/chromium-browser/chromedriver /content/opensea-autobot/driver/chromedriver
  cp /content/opensea-autobot/secret_config.py.template /content/opensea-autobot/secret_config.py
 ;;
 local)
  cp secret_config.py.template secret_config.py
 ;;
 *)
  echo "ERROR: $environment environment not supported"
  exit 1
 ;;
esac

