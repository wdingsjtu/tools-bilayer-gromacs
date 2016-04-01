# Auto-completion for memgro toolkits
#
# Created: 30/Mar/2016
# Updated:
#

TOOLS_PATH="/home/weiding/WORK/Simulation/membraneGRO/tools" 

_memgro_compl()
{
  local cur prev opts

  COMPREPLY=()

  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  opts=$(ls --ignore="_*" ${TOOLS_PATH} )

  if [[ ${COMP_CWORD} == 1 ]]; then
    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
  else
    _filedir
  fi
}

complete -F _memgro_compl memgro
complete -F _memgro_compl memgro.sh
