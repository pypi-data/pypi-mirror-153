if repo.system_source.dbdriver == "postgres":
    # the postgresql GROUP_CONCAT function has been changed.
    # we need to reset all the function so that change is taken into account
    install_custom_sql_scripts()
