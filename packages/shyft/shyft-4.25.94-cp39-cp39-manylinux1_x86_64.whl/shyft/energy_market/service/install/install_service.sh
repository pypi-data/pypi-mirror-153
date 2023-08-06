#!/usr/bin/env bash
set -o nounset
set -o pipefail
#set -o errexit

install_systemd() {
  # install_systemd service_name service_file opt_file exec_file user group
  local service_name=$1
  local service_file=$2
  local opt_file=$3
  local exec_file=$4
  local user=$5
  local group=$6
  local running=0
  if [[ $# -ne 6 ]]; then
    echo "Usage:$0 service_name service_file opt_file exec_file user group"
  fi
  if systemctl is-active --quiet "${service_name}" ; then
    running=1;
  else
    running=0
  fi

  if [[ ${running} -ne 0 ]]; then
      echo Stop the running service
      systemctl stop ${service_name}
  fi

  echo Install service file
  install -o "${user}" -g "${group}" -m 0644 "${service_file}" /etc/systemd/system/

  echo  Install executable
  install -o "${user}" -g "${group}" -m 0755 "${executable}" /usr/local/bin/

  install -D -o "${user}" -g "${group}" -m 0644 "${opt_file}" /etc/systemd/system/${service_name}.service.d/options0.conf

  echo Notify that the service file has changed
  systemctl daemon-reload

  echo Register for start on boot
  systemctl enable ${service_name}

  if [[ ${running} -eq 1 ]]; then
      echo Restart
      systemctl start ${service_name}
  fi
}

install_model_service() {
  if [[ $# -ne 9 ]]; then
    #                  1           2       3       4         5    6     7        8             9
    echo "Usage: $0 service_name web_ip base_port root_dir user group log_file conda_env_name py_path"
    exit 1
  fi
  local service_name=$1
  local web_ip=$2
  local base_port=$3
  local root_dir=$4
  local user=$5
  local group="$6"
  local log_file="$7"
  local conda_env="$8"
  local py_path=$9
  echo "Install ${service_name} ui/web-api ip= ${web_ip}, base_port= ${base_port}, rood_dir=${root_dir}, u=${user},g=${group},log=${log_file}, conda_env='${conda_env}', py_path='${py_path}}"
  local options0_file_name=options0.conf
  local script_path="${0%/*}"
  local service_file=${script_path}/${service_name}.service
  local executable=${script_path}/${service_name}.sh
  local opt0_file=/tmp/"${options0_file_name}"

  echo Install/update options file
cat >"${opt0_file}" <<END
[Service]
User=${user}
Environment=web_ip=${web_ip}
Environment=port_base=${base_port}
Environment=model_root=${root_dir}
Environment=log_file=${log_file}
Environment=conda_env=${conda_env}
END
  if [[ -n ${py_path} ]]; then
    echo "Environment=PYTHONPATH=${py_path}" >>"${opt0_file}"
  fi

  install_systemd "${service_name}" "${service_file}" "${opt0_file}" "${executable}" "${user}" "${group}"
  (rm -f "${opt0_file}")
}

install_dstm_service() {
  if [[ $# -ne 11 ]]; then
    #               1      2         3       4     5        6     7      8     9     10      11
    echo "Usage $0 dstm web_api_ip port web_port web_dir log_dir user group conda py_path dtss_containers"
    exit 1
  fi

  local service_name=$1
  local web_ip=$2
  local base_port=$3
  local web_port=$4
  local root_dir=$5
  local log_dir=$6
  local user=$7
  local group=$8
  local conda_env=$9
  local py_path="${10}"
  local dtss_cfg="${11}"

  echo "Install ${service_name} web-api ip= ${web_ip}, port= ${base_port},web_port=${web_port},root_dir=${root_dir},log_dir= ${log_dir}, u=${user},g=${group},conda_env='${conda_env}', py_path='${py_path}',dtss_cfg='${dtss_cfg}'"
  local options0_file_name=options0.conf
  local script_path="${0%/*}"
  local service_file=${script_path}/${service_name}.service
  local executable=${script_path}/${service_name}.sh
  local opt0_file=/tmp/"${options0_file_name}"
  echo Install/update options file

  cat >"${opt0_file}" <<END
[Service]
User=${user}
Environment=web_ip=${web_ip}
Environment=port=${base_port}
Environment=web_port=${web_port}
Environment=web_root=${root_dir}
Environment=log_root=${log_dir}
Environment=conda_env=${conda_env}
Environment=dtss_config=${dtss_cfg}
END
  if [[ -n ${py_path} ]]; then
    echo "Environment=PYTHONPATH=${py_path}" >>"${opt0_file}"
  fi

  install_systemd ${service_name} "${service_file}" "${opt0_file}" "${executable}" "${user}" "${group}"
  (rm -f "${opt0_file}")
}


install_stm_task_service() {
  if [[ $# -ne 11 ]]; then
    #                 1      2         3       4     5        6     7      8    9    10      11
    echo  "Usage $0 dstm web_api_ip port web_port web_dir mdl_dir user group conda py_path log_file"
    exit 1
  fi;
  local service_name=$1
  local web_ip=$2
  local base_port=$3
  local web_port=$4
  local root_dir=$5
  local mdl_dir=$6
  local user=$7
  local group=$8
  local conda_env=$9
  local py_path="${10}"
  local log_file="${11}"

  echo "Install ${service_name} web-api ip= ${web_ip}, port= ${base_port},web_port=${web_port},root_dir=${root_dir}, u=${user},g=${group},conda_env='${conda_env}', py_path='${py_path}',mdl_dir='${mdl_dir}' log_file=${log_file}"
  local service_file_name=${service_name}.service
  local options0_file_name=options0.conf
  local script_path="${0%/*}"
  local service_file=${script_path}/${service_file_name}
  local executable=${script_path}/${service_name}.sh

  echo Install/update options file
  opt0_file=/tmp/"${options0_file_name}"
  cat >"${opt0_file}" <<END
[Service]
User=${user}
Environment=web_ip=${web_ip}
Environment=port=${base_port}
Environment=web_port=${web_port}
Environment=root_dir=${root_dir}
Environment=model_root=${mdl_dir}
Environment=conda_env=${conda_env}
Environment=log_file=${log_file}
END
  if [[ -n ${py_path} ]]; then
    echo "Environment=PYTHONPATH=${py_path}" >>"${opt0_file}"
  fi

  install_systemd ${service_name} "${service_file}" "${opt0_file}" "${executable}" "${user}" "${group}"
  (rm -f "${opt0_file}")
}

print_help() {
cat<<END
--------------------------------------------------------
Usage:$0 (model|dstm|stm_task) <args>
To install systemd services.

To get specific help for <args>, invoke:
$0 model help
$0 dstm help
$0 stm_task help
--------------------------------------------------------
END
}

# these are the variables we need to get from command-line

if [[ $# -lt 2 ]]; then
  print_help
  exit 1
fi;


case $1 in
  model)
    if [[ $# -ne 9 ]]; then
      echo "------------------------------------------------------------------------"
      echo "Usage $0 model web_api_ip port root_dir user group logfile conda py_path"
      exit 1
    fi
    #                      name     web_ip port root  user group logfile conda_env py_path
    install_model_service "em_model" $2     $3   $4   $5   $6      "$7" "$8" "$9"
    ;;
  dstm)
    if [[ $# -ne 11 ]]; then
      echo "-----------------------------------------------------------------------------------------"
      #                 1   2         3       4     5        6     7      8     9     10       11
      echo "Usage $0 dstm web_api_ip port web_port web_dir log_dir user group conda py_path  dtss_cfg"
      echo "Ensure to escape the quotes in dtss_cfg, like {\\\"test\\\":\\\"/tmp/test\\\"}"
      exit 1
    fi
    install_dstm_service dstm $2 $3   $4   $5   $6      "$7" "$8" "$9" "${10}" "${11}"
    ;;
  stm_task)
    if [[ $# -ne 11 ]]; then
      echo "------------------------------------------------------------------------------------------"
      #                 1     2         3       4     5        6      7      8    9     10      11
      echo "Usage $0 stm_task web_api_ip port web_port web_dir mdl_dir user group conda py_path log_file"
      exit 1
    fi
    install_stm_task_service stm_task $2 $3   $4   $5   $6      "$7" "$8" "$9" "${10}" "${11}"
    ;;
  *)
    print_help
    ;;
esac;
