try:
    uri, newdn = __args__
except ValueError:
    print(
        "USAGE: cubicweb-ctl shell <instance> ldap_change_base_dn.py -- <ldap source uri> <new dn>"
    )
    print()
    print("you should not have updated your sources file yet")

olddn = repo.source_by_uri(uri).config["user-base-dn"]

assert olddn != newdn

input("Ensure you've stopped the instance, type enter when done.")

for eid, olduserdn in rql(
    "Any X, XURI WHERE X cwuri XURI, X cw_source S, S name %(name)s", {"name": uri}
):
    newuserdn = olduserdn.replace(olddn, newdn)
    if newuserdn != olduserdn:
        print(olduserdn, "->", newuserdn)
        sql(f"UPDATE cw_cwuser SET cw_cwuri='{newuserdn}' WHERE cw_eid={eid}")

commit()

print("you can now update the sources file to the new dn and restart the instance")
