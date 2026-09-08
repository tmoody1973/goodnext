# Triage Labels

Matt Pocock's skills speak in five triage roles. This repo maps them to
Linear statuses that already exist on team MOO. No new labels are created.

| Role in mattpocock/skills | In our Linear | How to apply |
| --- | --- | --- |
| `needs-triage` | status **Backlog** | Default for a new, unreviewed issue |
| `needs-info` | status **Backlog** plus a `Needs info:` line at the top of the description | Remove the line when the question is answered |
| `ready-for-agent` | status **Todo** | Issue has the full contract; an agent may start it |
| `ready-for-human` | status **Todo** plus assignee set to Tarik | Requires human implementation |
| `wontfix` | status **Canceled** | Reason recorded in a comment |

Existing labels Feature, Improvement, and Bug describe the kind of work, not
triage state, and may be added on top.

If the `Needs info:` convention proves awkward, the fallback is to create
`needs-info` and `ready-for-human` labels during a later linear-build kickoff.
