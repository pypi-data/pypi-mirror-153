#!/usr/bin/env bash
set -o nounset
set -o pipefail
set -o errexit

echo "Starting service $*"
if [[ $# -ne 7 ]]; then
  echo "Wrong number of arguments: $#, expected 7"
  echo "Usage $0 listen_ip port web_api_port web_doc_root log_dir conda_env dtts_container_cfg"
  echo " where :"
  echo "listen_ip: like 0.0.0.0 for all interfaces, or 127.0.0.1 for local-host only"
  echo "port: port for py/c++ api clients"
  echo "web_api_port: port for web/web-socket requests api"
  echo "log_dir: where to stash log-files for the service"
  echo "conda_env: '' or name of conda env to activate"
  echo "dtss_container_cfg: is a python dict"
  echo " like empty {}, or {'':'/mnt/dtss_root'}"
  echo "note1: If no conda-env activate wanted, pass empty empty quotes"
  echo "note2: ctrl-c to terminate(SIGTERM) to terminate services"
  exit 1
fi
web_ip=$1
port_num=$2
api_port_num=$3
web_doc_root=$4
log_dir=$5
conda_env=$6
container_cfg=$7

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

python -u -c "from shyft.energy_market.service.dstm_server_boot import start_service; start_service(web_ip='${web_ip}',port_num=${port_num}, doc_root='${web_doc_root}', api_port_num=${api_port_num}, log_file='${log_dir}/dstm0.log', server_log_root='${log_dir}',containers=${container_cfg})"
