# Provider-backed A2 execution

The Factory now includes a first provider-backed runner for the A2 subprocess substrate:

`execution-surfaces/openai_responses_runner.py`

It uses the OpenAI Responses API and keeps the A2 authority boundary unchanged.

## Security / authority

The runner:

- receives one bounded execution packet on stdin;
- receives no GitHub write token;
- cannot merge, publish or modify authority;
- materializes only local UTF-8 context files declared in the packet;
- rejects path traversal outside `A2_REPOSITORY_ROOT`;
- records provider identity and exact usage when returned;
- returns `blocked` rather than pretending execution occurred when `OPENAI_API_KEY` is absent.

## Runtime configuration

Required outside the repository:

`OPENAI_API_KEY`

Optional:

- `A2_OPENAI_MODEL` — defaults to `gpt-5.3-codex`;
- `OPENAI_RESPONSES_URL` — defaults to `https://api.openai.com/v1/responses`;
- `A2_OPENAI_HTTP_TIMEOUT`;
- `A2_REPOSITORY_ROOT`.

The API key must remain in the execution environment / secret store. Never commit it.

## Binding

Use the existing `JsonSubprocessAdapter` with:

```python
JsonSubprocessAdapter(
    [sys.executable, "execution-surfaces/openai_responses_runner.py"],
    artifact_dir,
    cwd=repository_root,
)
```

The adapter continues to persist request/result evidence and unique execution IDs.

## Acceptance boundary

Code-level provider binding is implemented here. Issue #16 remains open until a real credentialed smoke run demonstrates:

1. provider-backed completion;
2. inspectable execution ID;
3. valid structured output;
4. exact/declared usage quality;
5. bounded permissions;
6. preserved human gate.

This separation prevents a configured adapter from being misreported as production evidence before an actual run exists.
