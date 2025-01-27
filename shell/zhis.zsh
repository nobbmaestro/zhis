# Source this in your ~/.zshrc
autoload -U add-zsh-hook

zmodload zsh/datetime 2>/dev/null

# If zsh-autosuggestions is installed, configure it to use Zhis's search. If
# you'd like to override this, then add your config after the $(zhis init zsh)
# in your .zshrc
_zsh_autosuggest_strategy_zhis() {
	suggestion=$(ZHIS_QUERY="$1" zhis search --limit 1)
}

if [ -n "${ZSH_AUTOSUGGEST_STRATEGY:-}" ]; then
	ZSH_AUTOSUGGEST_STRATEGY=("zhis" "${ZSH_AUTOSUGGEST_STRATEGY[@]}")
else
	ZSH_AUTOSUGGEST_STRATEGY=("zhis")
fi

ZHIS_HISTORY_ID=""
# ZHIS_HISTORY_OFFSET=""

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
	output=$(ZHIS_QUERY=$BUFFER zhis search $* "$@" </dev/tty)

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
	_zhis_search --interactive
}
_zhis_search_viins() {
	_zhis_search --interactive
}

_zhis_up_search() {
	# Only trigger if the buffer is a single line
	if [[ ! $BUFFER == *$'\n'* ]]; then
		_zhis_search "$@"
	else
		zle up-line
	fi
}
_zhis_up_search_vicmd() {
	_zhis_up_search --interactive-inline
}
_zhis_up_search_viins() {
	_zhis_up_search --interactive-inline
}

add-zsh-hook preexec _zhis_preexec
add-zsh-hook precmd _zhis_precmd

zle -N zhis-search _zhis_search
zle -N zhis-search-vicmd _zhis_search_vicmd
zle -N zhis-search-viins _zhis_search_viins
zle -N zhis-up-search _zhis_up_search
zle -N zhis-up-search-vicmd _zhis_up_search_vicmd
zle -N zhis-up-search-viins _zhis_up_search_viins

bindkey -M emacs '^r' zhis-search
bindkey -M viins '^r' zhis-search-viins
bindkey -M vicmd '^r' zhis-search-vicmd

bindkey -M emacs '^[[A' zhis-up-search
bindkey -M vicmd '^[[A' zhis-up-search-vicmd
bindkey -M viins '^[[A' zhis-up-search-viins
bindkey -M emacs '^[OA' zhis-up-search
bindkey -M vicmd '^[OA' zhis-up-search-vicmd
bindkey -M viins '^[OA' zhis-up-search-viins
bindkey -M vicmd 'k' zhis-up-search-vicmd
