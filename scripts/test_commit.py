from commits import get_commit_info

commits, first, last = get_commit_info(
    "facebook",
    "react",
    "gaearon"
)

print("Commits:", commits)
print("First:", first)
print("Last:", last)
