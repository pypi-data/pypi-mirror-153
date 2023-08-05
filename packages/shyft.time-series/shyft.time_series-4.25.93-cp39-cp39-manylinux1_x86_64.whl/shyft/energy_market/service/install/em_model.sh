#!/usr/bin/env bash
set -o nounset
set -o pipefail
set -o errexit

echo "Starting service $*"
if [[ $# -ne 5 ]]; then
  echo "Wrong number of arguments: $#, expected 5"
  echo "Usage $0 web_ip base_port model_root log_file conda_env"
  echo "note1: If no conda-env activate wanted, pass empty empty quotes"
  echo "note2: ctrl-c to terminate(SIGTERM) to terminate services"
  exit 1
fi

web_ip=$1
base_port=$2
model_root=$3
log_file=$4
conda_env=$5


if [[ ${base_port} -lt 1024 ]]; then
  echo "Base port should be larger than 1024, typical value would be 30000"
  exit 1
fi

if [[ ! -d ${model_root} ]]; then
  echo "Model root dir ${model_root} is missing, exit"
  exit 1
fi

if [[ -z "${web_ip}" ]]; then
  echo "Web listening ip for the ui-layout server  must be specified"
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

python -u -c "from shyft.energy_market.service import boot; boot.start_service(model_root=r'${model_root}', log_file=r'${log_file}',port_base=${base_port},web_ip='${web_ip}')"
