default_config = """
[Logging]

; Set the threshold level for the logger,
; anything less severe will be ignored
; for example if set to warning, info and debug messages
; won't be logged.
; Allowed values: debug, info, warning, error, critical
min_log_level = debug

; Set the minimum level for the console handler
console_min_log_level = debug

; Set the minimum level for the file handler
file_min_log_level = error
"""