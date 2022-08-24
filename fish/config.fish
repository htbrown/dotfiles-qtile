# Environment Variables
set -gx linux_version (uname -r)
set -gx fish_greeting "Fish v$FISH_VERSION on $hostname ($linux_version)"

# Interactive Sessions
if status is-interactive
    # Commands to run in interactive sessions can go here
end

# Starship Init
starship init fish | source
