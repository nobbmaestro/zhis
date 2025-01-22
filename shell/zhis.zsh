# Source this in your ~/.zshrc
autoload -U add-zsh-hook

zmodload zsh/datetime 2>/dev/null

_zhis_preexec() {
	(zhis history add -- "$1")
}
_zhis_precmd() {}

_zhis_search() {
	emulate -L zsh
	zle -I

	local output
	output=$(ZHIS_QUERY=$BUFFER zhis search $* -i </dev/tty)

	zle reset-prompt

	if [[ -n $output ]]; then
		RBUFFER=""
		LBUFFER=$output

		if [[ $LBUFFER == __zhis_accept__:* ]]; then
			LBUFFER=${LBUFFER#__zhis_accept__:}
			# zle accept-line # TODO: Make this configurable
		fi
	fi
}
_zhis_search_vicmd() {
	_zhis_search
}
_zhis_search_viins() {
	_zhis_search
}

add-zsh-hook preexec _zhis_preexec
add-zsh-hook precmd _zhis_precmd

zle -N zhis-search _zhis_search
zle -N zhis-search-vicmd _zhis_search_vicmd
zle -N zhis-search-viins _zhis_search_viins

bindkey -M emacs '^r' zhis-search
bindkey -M viins '^r' zhis-search-viins
bindkey -M vicmd '^r' zhis-search-vicmd
