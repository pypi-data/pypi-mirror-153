#!/usr/bin/env bash
set -o nounset
set -o pipefail
set -o errexit

echo "Starting service $*"
if [[ $# -ne 7 ]]; then
  echo "Wrong number of arguments: $#, expected 5"
  echo "-------------------------------------------------------------------------------"
  echo "Usage $0 listen_ip port web_api_port web_doc_root model_dir conda_env log_file"
  echo " where :"
  echo "listen_ip: like 0.0.0.0 for all interfaces, or 127.0.0.1 for local-host only"
  echo "port: port for py/c++ api clients"
  echo "web_api_port: port for web/web-socket requests api"
  echo "model_dir: where to stash model-files for the service"
  echo "conda_env: '' or name of conda env to activate"
  echo "-----------------------------"
  echo "note1: If no conda-env activate wanted, pass empty empty quotes"
  echo "note2: ctrl-c to terminate(SIGTERM) to terminate services"
  exit 1
fi
web_ip=$1
port_num=$2
api_port_num=$3
web_doc_root=$4
model_root=$5
conda_env=$6
log_file=$7

if [[ ${port_num} -lt 1024 ]]; then
  echo "Base port should be larger than 1024, typical value would be 30000"
  exit 1
fi

if [[ ! -d ${web_doc_root} ]]; then
  echo "Model root dir ${web_doc_root} is missing, exit"
  exit 1
fi

if [[ -n "${conda_env}" ]]; then
  SHYFT_CONDA_ROOT=${SHYFT_CONDA_ROOT:=$HOME}
  conda_src="${SHYFT_CONDA_ROOT}/miniconda/etc/profile.d/conda.sh"
  if [[ -e ${conda_src} ]]; then
    set +o nounset
    source "${conda_src}"
    conda activate "${conda_env}"
  else
    echo "Missing required conda installation? no file ${conda_src}"
    exit 1
  fi
fi

python -u -c "from shyft.energy_market.service.stm_task_boot import start_service; start_service(web_ip='${web_ip}',port_num=${port_num},api_port_num=${api_port_num}, doc_root='${web_doc_root}', model_root='${model_root}', log_file='${log_file}')"
