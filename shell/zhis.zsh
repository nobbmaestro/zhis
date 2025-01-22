# Source this in your ~/.zshrc
autoload -U add-zsh-hook

zmodload zsh/datetime 2>/dev/null

ZHIS_HISTORY_ID=""

_zhis_preexec() {
	local id
	id=$(zhis history add --id -- "$1")
	export ZHIS_HISTORY_ID="$id"
	__zhis_preexec_time=${EPOCHREALTIME-}
}

_zhis_precmd() {
	local EXIT="$?" __zhis_precmd_time=${EPOCHREALTIME-}

	[[ -z "${ZHIS_HISTORY_ID:-}" ]] && return

	local duration=""
	if [[ -n $__zhis_preexec_time && -n $__zhis_precmd_time ]]; then
		printf -v duration %.0f $(((__zhis_precmd_time - __zhis_preexec_time) * 1000000))
	fi

	(
		zhis history edit \
			--exit-code $EXIT \
			${duration:+--duration=$duration} \
			-- $ZHIS_HISTORY_ID &
	) >/dev/null 2>&1

	export ZHIS_HISTORY_ID=""
}

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
